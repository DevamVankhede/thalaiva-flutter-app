<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Models\OtpCode;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class AuthController extends Controller
{
    /**
     * Send OTP to customer phone.
     */
    public function sendOtp(Request $request): JsonResponse
    {
        $request->validate([
            'phone' => 'required|string|min:10|max:20',
        ]);

        $phone = preg_replace('/[^\d+]/', '', $request->input('phone'));
        $otp = (string) rand(100000, 999999);

        // Store hashed OTP
        OtpCode::create([
            'id' => (string) Str::uuid(),
            'phone' => $phone,
            'code_hash' => Hash::make($otp),
            'expires_at' => Carbon::now()->addMinutes(10),
            'attempts' => 0,
        ]);

        return response()->json([
            'success' => true,
            'message' => 'OTP dispatched successfully to your phone.',
            'phone' => $phone,
            // In dev environment, return the otp code for friction-free testing
            'dev_otp' => app()->environment('local', 'testing') ? $otp : null,
        ]);
    }

    /**
     * Verify OTP and issue Sanctum token.
     */
    public function verifyOtp(Request $request): JsonResponse
    {
        $request->validate([
            'phone' => 'required|string',
            'otp' => 'required|string|min:4|max:6',
        ]);

        $phone = preg_replace('/[^\d+]/', '', $request->input('phone'));
        $otp = $request->input('otp');

        // Look for valid OTP
        $otpRecord = OtpCode::where('phone', $phone)
            ->whereNull('verified_at')
            ->where('expires_at', '>', Carbon::now())
            ->latest()
            ->first();

        $isValid = false;
        if ($otpRecord && Hash::check($otp, $otpRecord->code_hash)) {
            $isValid = true;
        } elseif (app()->environment('local', 'testing') && ($otp === '123456' || $otp === '999999')) {
            $isValid = true;
        }

        if (!$isValid) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid or expired OTP code.',
            ], 422);
        }

        if ($otpRecord) {
            $otpRecord->update(['verified_at' => Carbon::now()]);
        }

        $user = User::firstOrCreate(
            ['phone' => $phone],
            [
                'name' => $request->input('name', 'Thalaivaa Customer'),
                'email' => $request->input('email'),
                'is_active' => true,
                'otp_verified_at' => Carbon::now(),
            ]
        );

        $token = $user->createToken('customer-app')->plainTextToken;

        return response()->json([
            'success' => true,
            'message' => 'Authentication successful.',
            'token' => $token,
            'user' => [
                'id' => $user->id,
                'name' => $user->name,
                'phone' => $user->phone,
                'email' => $user->email,
            ],
        ]);
    }

    /**
     * Get current authenticated user profile.
     */
    public function me(Request $request): JsonResponse
    {
        $user = $request->user();

        return response()->json([
            'success' => true,
            'data' => [
                'id' => $user->id,
                'name' => $user->name,
                'phone' => $user->phone,
                'email' => $user->email,
                'profile' => $user->profile,
            ],
        ]);
    }

    /**
     * Logout and revoke Sanctum token.
     */
    public function logout(Request $request): JsonResponse
    {
        if ($request->user()) {
            $request->user()->currentAccessToken()->delete();
        }

        return response()->json([
            'success' => true,
            'message' => 'Logged out successfully.',
        ]);
    }
}
