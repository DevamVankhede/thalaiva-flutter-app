<?php

namespace Tests\Feature;

use Tests\TestCase;

class CouponValidationTest extends TestCase
{
    public function test_valid_coupon_computes_correct_discount(): void
    {
        $response = $this->postJson('/api/v1/coupons/validate', [
            'code' => 'THALAIVAA50',
            'subtotal_inr' => 300,
        ]);

        $response->assertStatus(200)
            ->assertJson([
                'success' => true,
                'data' => [
                    'code' => 'THALAIVAA50',
                    'discount_inr' => 50,
                    'subtotal_after_discount_inr' => 250,
                ],
            ]);
    }

    public function test_coupon_fails_when_below_minimum_threshold(): void
    {
        $response = $this->postJson('/api/v1/coupons/validate', [
            'code' => 'THALAIVAA50',
            'subtotal_inr' => 150,
        ]);

        $response->assertStatus(422)
            ->assertJson([
                'success' => false,
            ]);
    }

    public function test_non_existent_coupon_returns_422(): void
    {
        $response = $this->postJson('/api/v1/coupons/validate', [
            'code' => 'INVALID_CODE_123',
            'subtotal_inr' => 500,
        ]);

        $response->assertStatus(422)
            ->assertJson([
                'success' => false,
            ]);
    }
}
