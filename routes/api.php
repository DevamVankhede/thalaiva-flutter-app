<?php

use App\Http\Controllers\Api\V1\AuthController;
use App\Http\Controllers\Api\V1\CatalogController;
use App\Http\Controllers\Api\V1\CouponController;
use App\Http\Controllers\Api\V1\OrderController;
use Carbon\Carbon;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes — Thalaivaa SaaS Platform (OWASP Hardened)
|--------------------------------------------------------------------------
*/

// Health Check
Route::get('/health', function () {
    return response()->json([
        'status' => 'healthy',
        'service' => 'Thalaivaa API',
        'version' => '1.0.0',
        'timestamp' => Carbon::now()->toIso8601String(),
    ]);
});

// API Version 1
Route::prefix('v1')->middleware(['throttle:api'])->group(function () {
    // Auth & OTP — Anti-Brute-Force Rate Limiting (5 attempts/min)
    Route::post('/auth/otp/send', [AuthController::class, 'sendOtp'])->middleware('throttle:5,1');
    Route::post('/auth/otp/verify', [AuthController::class, 'verifyOtp'])->middleware('throttle:5,1');

    // Catalog (Public Read)
    Route::get('/branches', [CatalogController::class, 'branches']);
    Route::get('/categories', [CatalogController::class, 'categories']);
    Route::get('/products', [CatalogController::class, 'products']);

    // Coupons
    Route::post('/coupons/validate', [CouponController::class, 'validateCoupon'])->middleware('throttle:20,1');

    // Orders — Bot Flood Mitigation
    Route::get('/orders', [OrderController::class, 'index']);
    Route::post('/orders', [OrderController::class, 'store'])->middleware('throttle:15,1');
    Route::get('/orders/{id}', [OrderController::class, 'show']);

    // Authenticated Routes
    Route::middleware('auth:sanctum')->group(function () {
        Route::get('/auth/me', [AuthController::class, 'me']);
        Route::post('/auth/logout', [AuthController::class, 'logout']);
    });
});

// Backward-compatible un-prefixed aliases for legacy clients
Route::middleware(['throttle:api'])->group(function () {
    Route::get('/branches', [CatalogController::class, 'branches']);
    Route::get('/categories', [CatalogController::class, 'categories']);
    Route::get('/products', [CatalogController::class, 'products']);
    Route::post('/coupons/validate', [CouponController::class, 'validateCoupon']);
    Route::get('/orders', [OrderController::class, 'index']);
    Route::post('/orders', [OrderController::class, 'store']);
    Route::get('/orders/{id}', [OrderController::class, 'show']);
});
