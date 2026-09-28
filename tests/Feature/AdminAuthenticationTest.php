<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Auth;
use Tests\TestCase;

class AdminAuthenticationTest extends TestCase
{
    public function test_admin_authentication_succeeds_with_valid_credentials(): void
    {
        $credentials = [
            'email' => 'admin@thalaivaa.com',
            'password' => 'Admin@Thalaivaa2026',
        ];

        $this->assertTrue(Auth::guard('admin')->attempt($credentials));
    }

    public function test_admin_authentication_fails_with_invalid_password(): void
    {
        $credentials = [
            'email' => 'admin@thalaivaa.com',
            'password' => 'WrongPassword123!',
        ];

        $this->assertFalse(Auth::guard('admin')->attempt($credentials));
    }
}
