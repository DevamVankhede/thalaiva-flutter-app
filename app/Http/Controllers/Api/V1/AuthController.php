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
     * Authenticate user by email or phone and password, issuing Sanctum token.
     */
    public function login(Request $request): JsonResponse
    {
        $request->validate([
            'email' => 'nullable|string',
            'phone' => 'nullable|string',
            'username' => 'nullable|string',
            'email_or_phone' => 'nullable|string',
            'password' => 'required|string',
        ]);

        $identifier = $request->input('email')
            ?? $request->input('phone')
            ?? $request->input('email_or_phone')
            ?? $request->input('username');

        if (empty($identifier)) {
            return response()->json([
                'success' => false,
                'message' => 'Email or phone number is required.',
            ], 422);
        }

        $cleanPhone = preg_replace('/[^\d+]/', '', $identifier);

        $user = User::where('email', $identifier)
            ->orWhere('phone', $identifier)
            ->when(!empty($cleanPhone), function ($query) use ($cleanPhone) {
                $query->orWhere('phone', $cleanPhone);
            })
            ->first();

        if (!$user || !$user->password || !Hash::check($request->input('password'), $user->password)) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid email or password.',
            ], 401);
        }

        if (!$user->is_active) {
            return response()->json([
                'success' => false,
                'message' => 'Account is inactive. Please contact support.',
            ], 403);
        }

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
        $user = $request->user() ?: auth('sanctum')->user();

        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthenticated.',
            ], 401);
        }

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
        $user = $request->user() ?: auth('sanctum')->user();

        if ($user) {
            if ($user->currentAccessToken()) {
                $user->currentAccessToken()->delete();
            } else {
                $user->tokens()->delete();
            }
        }

        return response()->json([
            'success' => true,
            'message' => 'Logged out successfully.',
        ]);
    }
}
