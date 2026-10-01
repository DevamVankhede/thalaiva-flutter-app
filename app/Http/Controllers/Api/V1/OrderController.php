<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\CreateOrderRequest;
use App\Models\Order;
use App\Services\OrderService;
use Exception;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class OrderController extends Controller
{
    protected OrderService $orderService;

    public function __construct(OrderService $orderService)
    {
        $this->orderService = $orderService;
    }

    /**
     * Create an order.
     */
    public function store(CreateOrderRequest $request): JsonResponse
    {
        try {
            $user = $request->user() ?: auth('sanctum')->user();
            $order = $this->orderService->createOrder($request->validated(), $user);

            return response()->json([
                'success' => true,
                'message' => 'Order placed successfully!',
                'data' => [
                    'id' => $order->id,
                    'order_number' => $order->order_number,
                    'status' => $order->status,
                    'payment_status' => $order->payment_status,
                    'subtotal_inr' => round($order->subtotal / 100, 2),
                    'discount_inr' => round($order->discount_amount / 100, 2),
                    'tax_inr' => round($order->tax_amount / 100, 2),
                    'delivery_charge_inr' => round($order->delivery_charge / 100, 2),
                    'total_amount_inr' => round($order->total_amount / 100, 2),
                    'delivery_name' => $order->delivery_name,
                    'delivery_phone' => $order->delivery_phone,
                    'delivery_address' => $order->delivery_address_line . ', ' . $order->delivery_city,
                    'items_count' => $order->items->count(),
                    'items' => $order->items->map(fn($item) => [
                        'id' => $item->id,
                        'product_name' => $item->product_name_snapshot,
                        'variant_name' => $item->variant_name_snapshot,
                        'quantity' => $item->quantity,
                        'unit_price_inr' => round($item->unit_price / 100, 2),
                        'total_price_inr' => round($item->line_total / 100, 2),
                    ]),
                    'created_at' => $order->created_at->toIso8601String(),
                ],
            ], 201);
        } catch (Exception $e) {
            $statusCode = ($e->getCode() >= 400 && $e->getCode() < 500) ? $e->getCode() : 500;
            return response()->json([
                'success' => false,
                'message' => $e->getMessage(),
            ], $statusCode);
        }
    }

    /**
     * List customer's past orders.
     */
    public function index(Request $request): JsonResponse
    {
        $user = $request->user() ?: auth('sanctum')->user();

        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthenticated. Please log in to view orders.',
            ], 401);
        }

        $query = Order::with(['items', 'branch'])
            ->where('user_id', $user->id)
            ->latest();

        $orders = $query->paginate(20);

        return response()->json([
            'success' => true,
            'data' => $orders->getCollection()->map(fn($o) => [
                'id' => $o->id,
                'order_number' => $o->order_number,
                'status' => $o->status,
                'payment_status' => $o->payment_status,
                'branch_name' => $o->branch?->name,
                'total_amount_inr' => round($o->total_amount / 100, 2),
                'items_count' => $o->items->count(),
                'items' => $o->items->map(fn($item) => [
                    'id' => $item->id,
                    'product_name' => $item->product_name_snapshot,
                    'variant_name' => $item->variant_name_snapshot,
                    'quantity' => $item->quantity,
                    'unit_price_inr' => round($item->unit_price / 100, 2),
                    'total_price_inr' => round($item->line_total / 100, 2),
                ]),
                'delivery_name' => $o->delivery_name,
                'delivery_address' => $o->delivery_address_line . ', ' . $o->delivery_city,
                'created_at' => $o->created_at->toIso8601String(),
            ]),
            'meta' => [
                'total' => $orders->total(),
                'current_page' => $orders->currentPage(),
            ],
        ]);
    }

    /**
     * Get single order details with ownership verification.
     */
    public function show(Request $request, string $id): JsonResponse
    {
        $user = $request->user() ?: auth('sanctum')->user();

        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthenticated. Please log in to view order details.',
            ], 401);
        }

        $query = Order::with(['items.product', 'branch', 'statusLogs', 'payments']);

        if (strlen($id) === 36) {
            $query->where('id', $id);
        } else {
            $query->where('order_number', $id);
        }

        $order = $query->first();

        if (!$order) {
            return response()->json([
                'success' => false,
                'message' => 'Order not found.',
            ], 404);
        }

        // Ownership verification (IDOR protection)
        if ($order->user_id !== $user->id) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthorized access to this order.',
            ], 403);
        }

        return response()->json([
            'success' => true,
            'data' => [
                'id' => $order->id,
                'order_number' => $order->order_number,
                'status' => $order->status,
                'payment_status' => $order->payment_status,
                'branch' => [
                    'id' => $order->branch?->id,
                    'name' => $order->branch?->name,
                    'phone' => $order->branch?->phone,
                ],
                'delivery' => [
                    'name' => $order->delivery_name,
                    'phone' => $order->delivery_phone,
                    'address' => $order->delivery_address_line . ', ' . $order->delivery_city . ' ' . $order->delivery_postal,
                ],
                'pricing' => [
                    'subtotal_inr' => round($order->subtotal / 100, 2),
                    'discount_inr' => round($order->discount_amount / 100, 2),
                    'tax_inr' => round($order->tax_amount / 100, 2),
                    'delivery_charge_inr' => round($order->delivery_charge / 100, 2),
                    'total_amount_inr' => round($order->total_amount / 100, 2),
                ],
                'items' => $order->items->map(fn($item) => [
                    'id' => $item->id,
                    'product_name' => $item->product_name_snapshot,
                    'variant_name' => $item->variant_name_snapshot,
                    'quantity' => $item->quantity,
                    'unit_price_inr' => round($item->unit_price / 100, 2),
                    'total_price_inr' => round($item->line_total / 100, 2),
                    'modifiers' => $item->modifier_snapshot_json ? json_decode($item->modifier_snapshot_json, true) : [],
                ]),
                'status_logs' => $order->statusLogs->map(fn($log) => [
                    'from' => $log->from_status,
                    'to' => $log->to_status,
                    'time' => $log->created_at->toIso8601String(),
                    'notes' => $log->notes,
                ]),
                'created_at' => $order->created_at->toIso8601String(),
            ],
        ]);
    }
}
