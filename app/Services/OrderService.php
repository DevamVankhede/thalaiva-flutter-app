<?php

namespace App\Services;

use App\Models\Branch;
use App\Models\ModifierOption;
use App\Models\Order;
use App\Models\OrderItem;
use App\Models\OrderStatusLog;
use App\Models\Payment;
use App\Models\Product;
use App\Models\ProductVariant;
use App\Models\User;
use Carbon\Carbon;
use Exception;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class OrderService
{
    protected CouponService $couponService;

    public function __construct(CouponService $couponService)
    {
        $this->couponService = $couponService;
    }

    /**
     * Create an order transactionally with strict server-side validation & pricing.
     *
     * @param array $data
     * @param User|null $user
     * @return Order
     * @throws Exception
     */
    public function createOrder(array $data, ?User $user = null): Order
    {
        return DB::transaction(function () use ($data, $user) {
            // 1. Resolve Branch
            $branch = Branch::where('id', $data['branch_id'])
                ->where('is_active', true)
                ->first();

            if (!$branch) {
                throw new Exception("Branch with ID '{$data['branch_id']}' is not available.", 422);
            }

            // 2. Resolve User
            if (!$user) {
                if (!empty($data['delivery_phone'])) {
                    $user = User::firstOrCreate(
                        ['phone' => $data['delivery_phone']],
                        [
                            'name' => $data['delivery_name'] ?? 'Thalaivaa Customer',
                            'email' => $data['delivery_email'] ?? null,
                            'is_active' => true,
                        ]
                    );
                } else {
                    $user = User::first();
                }
            }

            // 3. Process Line Items & Compute Real Catalog Prices
            $subtotalPaise = 0;
            $preparedItems = [];

            if (empty($data['items']) || !is_array($data['items'])) {
                throw new Exception("Order must contain at least one item.", 422);
            }

            foreach ($data['items'] as $index => $itemInput) {
                $productId = $itemInput['product_id'] ?? null;
                $quantity = (int) ($itemInput['quantity'] ?? 1);

                if ($quantity < 1) {
                    throw new Exception("Quantity for item at index {$index} must be at least 1.", 422);
                }

                $product = Product::with(['variants'])->find($productId);
                if (!$product || !$product->is_available) {
                    throw new Exception("Product '{$productId}' is unavailable or inactive.", 422);
                }

                $unitPricePaise = (int) $product->base_price;
                $variantName = 'Regular';
                $variantId = $itemInput['variant_id'] ?? null;

                if ($variantId) {
                    $variant = ProductVariant::where('id', $variantId)
                        ->where('product_id', $productId)
                        ->where('is_available', true)
                        ->first();

                    if (!$variant) {
                        throw new Exception("Selected variant is invalid for product '{$product->name}'.", 422);
                    }

                    $unitPricePaise += (int) $variant->price_adjustment;
                    $variantName = $variant->name;
                }

                // Modifiers add-ons: resolve strictly from database
                $modifierTotalPaise = 0;
                $modifiersSnapshot = [];
                if (!empty($itemInput['modifiers']) && is_array($itemInput['modifiers'])) {
                    foreach ($itemInput['modifiers'] as $mod) {
                        $modId = $mod['id'] ?? null;
                        if ($modId) {
                            $dbMod = ModifierOption::find($modId);
                            if ($dbMod && $dbMod->is_available) {
                                $modPrice = (int) $dbMod->price_adjustment;
                                $modifierTotalPaise += $modPrice;
                                $modifiersSnapshot[] = [
                                    'id' => $dbMod->id,
                                    'name' => $dbMod->name,
                                    'price_paise' => $modPrice,
                                ];
                            }
                        }
                    }
                }

                $itemUnitPrice = $unitPricePaise + $modifierTotalPaise;
                $itemTotalPrice = $itemUnitPrice * $quantity;
                $subtotalPaise += $itemTotalPrice;

                $preparedItems[] = [
                    'product_id' => $product->id,
                    'variant_id' => $variantId,
                    'product_name_snapshot' => $product->name,
                    'quantity' => $quantity,
                    'unit_price' => $itemUnitPrice,
                    'line_total' => $itemTotalPrice,
                    'modifier_snapshot_json' => !empty($modifiersSnapshot) ? $modifiersSnapshot : null,
                ];
            }

            // 4. Discounts
            $discountPaise = 0;
            $appliedCouponCode = null;
            $discountType = 'none';
            $discountValue = 0;

            if (!empty($data['coupon_code'])) {
                $couponResult = $this->couponService->validateCoupon(
                    $data['coupon_code'],
                    $subtotalPaise,
                    $branch->id
                );
                $discountPaise = $couponResult['discount_paise'];
                $appliedCouponCode = $couponResult['code'];
                $discountType = $couponResult['type'];
                $discountValue = $couponResult['value'];
                $this->couponService->recordCouponUse($appliedCouponCode);
            }

            // 5. Taxes (5% GST in India for restaurant services)
            $taxableAmount = max(0, $subtotalPaise - $discountPaise);
            $taxPaise = (int) round($taxableAmount * 0.05);

            // 6. Delivery Charge (₹40 if subtotal < ₹1000, free delivery over ₹1000)
            $deliveryChargePaise = ($subtotalPaise >= 100000) ? 0 : 4000;

            // 7. Total Amount
            $totalPaise = $taxableAmount + $taxPaise + $deliveryChargePaise;

            // 8. Generate Unique Sequential Order Number
            $orderNumber = 'THL-' . date('Ymd') . '-' . strtoupper(Str::random(6));

            // 9. Persist Order (defaults payment_status to 'pending')
            $order = Order::create([
                'id' => (string) Str::uuid(),
                'order_number' => $orderNumber,
                'user_id' => $user->id,
                'branch_id' => $branch->id,
                'status' => 'pending',
                'payment_status' => 'pending',
                'delivery_name' => $data['delivery_name'] ?? $user->name ?? 'Valued Customer',
                'delivery_phone' => $data['delivery_phone'] ?? $user->phone ?? '+919217002598',
                'delivery_address_line' => $data['delivery_address_line'] ?? 'City Light Town, Surat',
                'delivery_city' => $data['delivery_city'] ?? 'Surat',
                'delivery_postal' => $data['delivery_postal'] ?? '395007',
                'subtotal' => $subtotalPaise,
                'discount_amount' => $discountPaise,
                'discount_type' => $discountType,
                'discount_value' => $discountValue,
                'tax_amount' => $taxPaise,
                'delivery_charge' => $deliveryChargePaise,
                'total_amount' => $totalPaise,
                'notes' => $data['notes'] ?? null,
                'status_changed_at' => Carbon::now(),
            ]);

            // 10. Persist Order Items
            foreach ($preparedItems as $item) {
                $item['order_id'] = $order->id;
                OrderItem::create($item);
            }

            // 11. Record Order Status Log
            OrderStatusLog::create([
                'id' => (string) Str::uuid(),
                'order_id' => $order->id,
                'from_status' => null,
                'to_status' => 'pending',
                'actor_type' => 'customer',
                'actor_id' => $user->id,
                'notes' => 'Order placed successfully by customer.',
            ]);

            // 12. Create Payment record & link payment_id
            $payment = Payment::create([
                'id' => (string) Str::uuid(),
                'order_id' => $order->id,
                'razorpay_payment_id' => 'pay_' . Str::random(14),
                'amount' => $totalPaise,
                'currency' => 'INR',
                'status' => 'created',
                'capture_status' => 'pending',
            ]);

            $order->update(['payment_id' => $payment->id]);

            return $order->fresh(['items', 'branch', 'statusLogs', 'user', 'payment']);
        });
    }
}
