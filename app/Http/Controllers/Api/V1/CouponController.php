<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Http\Requests\ValidateCouponRequest;
use App\Services\CouponService;
use Exception;
use Illuminate\Http\JsonResponse;

class CouponController extends Controller
{
    protected CouponService $couponService;

    public function __construct(CouponService $couponService)
    {
        $this->couponService = $couponService;
    }

    /**
     * Validate coupon code against subtotal.
     */
    public function validateCoupon(ValidateCouponRequest $request): JsonResponse
    {
        try {
            $code = $request->input('code');
            $subtotalPaise = (int) round(((float) $request->input('subtotal_inr')) * 100);
            $branchId = $request->input('branch_id');

            $result = $this->couponService->validateCoupon($code, $subtotalPaise, $branchId);

            return response()->json([
                'success' => true,
                'message' => "Coupon '{$result['code']}' applied successfully!",
                'data' => $result,
            ]);
        } catch (Exception $e) {
            return response()->json([
                'success' => false,
                'message' => $e->getMessage(),
            ], 422);
        }
    }
}
