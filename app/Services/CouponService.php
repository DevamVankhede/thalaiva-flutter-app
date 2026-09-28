<?php

namespace App\Services;

use App\Models\Coupon;
use Carbon\Carbon;
use Exception;

class CouponService
{
    /**
     * Validate a coupon code against subtotal in paise.
     *
     * @param string $code
     * @param int $subtotalPaise
     * @param string|null $branchId
     * @return array
     * @throws Exception
     */
    public function validateCoupon(string $code, int $subtotalPaise, ?string $branchId = null): array
    {
        $coupon = Coupon::where('code', strtoupper(trim($code)))
            ->where('is_active', true)
            ->first();

        if (!$coupon) {
            throw new Exception("Invalid or inactive coupon code '{$code}'", 422);
        }

        // Check expiration
        if ($coupon->expires_at && Carbon::now()->isAfter($coupon->expires_at)) {
            throw new Exception("Coupon code '{$code}' has expired", 422);
        }

        // Check max uses
        if ($coupon->max_uses !== null && $coupon->used_count >= $coupon->max_uses) {
            throw new Exception("Coupon code '{$code}' has reached its maximum redemption limit", 422);
        }

        $subtotalInr = $subtotalPaise / 100;
        $discountPaise = 0;

        // Check specific minimum order thresholds
        if (strtoupper($code) === 'FEAST100' && $subtotalInr < 500) {
            throw new Exception("Coupon 'FEAST100' requires a minimum order of ₹500 (Current: ₹{$subtotalInr})", 422);
        }
        if (strtoupper($code) === 'THALAIVAA50' && $subtotalInr < 200) {
            throw new Exception("Coupon 'THALAIVAA50' requires a minimum order of ₹200 (Current: ₹{$subtotalInr})", 422);
        }

        if ($coupon->type === 'percent') {
            $discountPaise = (int) round(($subtotalPaise * (float) $coupon->value) / 100);
        } else {
            // Fixed discount: value is in INR
            $discountPaise = (int) round(((float) $coupon->value) * 100);
        }

        // Cap discount at subtotal
        $discountPaise = min($discountPaise, $subtotalPaise);

        return [
            'coupon_id' => $coupon->id,
            'code' => $coupon->code,
            'type' => $coupon->type,
            'value' => (float) $coupon->value,
            'discount_paise' => $discountPaise,
            'discount_inr' => round($discountPaise / 100, 2),
            'subtotal_after_discount_inr' => round(($subtotalPaise - $discountPaise) / 100, 2),
        ];
    }

    /**
     * Increment coupon used count.
     */
    public function recordCouponUse(string $code): void
    {
        $coupon = Coupon::where('code', strtoupper(trim($code)))->first();
        if ($coupon) {
            $coupon->increment('used_count');
        }
    }
}
