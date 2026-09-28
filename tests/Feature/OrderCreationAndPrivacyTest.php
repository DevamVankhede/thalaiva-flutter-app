<?php

namespace Tests\Feature;

use App\Models\Branch;
use App\Models\Product;
use App\Models\User;
use Tests\TestCase;

class OrderCreationAndPrivacyTest extends TestCase
{
    public function test_transactional_order_creation_with_real_catalog_prices(): void
    {
        $user = User::first();
        $branch = Branch::first();
        $product = Product::with('variants')->first();
        $modifierOption = \App\Models\ModifierOption::first();

        $payload = [
            'branch_id' => $branch->id,
            'items' => [
                [
                    'product_id' => $product->id,
                    'variant_id' => $product->variants->first()?->id,
                    'quantity' => 2,
                    'modifiers' => $modifierOption ? [
                        ['id' => $modifierOption->id, 'name' => $modifierOption->name],
                    ] : [],
                ],
            ],
            'coupon_code' => 'THALAIVAA50',
            'delivery_name' => 'Ananya Sharma',
            'delivery_phone' => '+919217002598',
            'delivery_address_line' => '404 Vesu VIP Road',
            'delivery_city' => 'Surat',
            'delivery_postal' => '395007',
        ];

        $response = $this->actingAs($user, 'sanctum')->postJson('/api/v1/orders', $payload);

        $response->assertStatus(201)
            ->assertJson([
                'success' => true,
                'data' => [
                    'delivery_name' => 'Ananya Sharma',
                    'payment_status' => 'pending',
                ],
            ]);

        $this->assertDatabaseHas('orders', [
            'delivery_name' => 'Ananya Sharma',
            'user_id' => $user->id,
        ]);

        $this->assertDatabaseHas('order_status_logs', [
            'to_status' => 'pending',
        ]);
    }

    public function test_empty_items_array_returns_validation_error_422(): void
    {
        $branch = Branch::first();

        $response = $this->postJson('/api/v1/orders', [
            'branch_id' => $branch->id,
            'items' => [],
            'delivery_name' => 'Test User',
            'delivery_phone' => '+919217002598',
            'delivery_address_line' => 'Surat',
        ]);

        $response->assertStatus(422)
            ->assertJson([
                'success' => false,
            ]);
    }

    public function test_idor_protection_blocks_cross_user_order_access(): void
    {
        $userA = User::first();
        $userB = User::create([
            'phone' => '+919876543210',
            'name' => 'Attacker User',
            'is_active' => true,
        ]);

        $branch = Branch::first();
        $product = Product::first();

        // User A creates order
        $createRes = $this->actingAs($userA, 'sanctum')->postJson('/api/v1/orders', [
            'branch_id' => $branch->id,
            'items' => [
                ['product_id' => $product->id, 'quantity' => 1],
            ],
            'delivery_name' => 'User A',
            'delivery_phone' => $userA->phone,
            'delivery_address_line' => 'Address A',
        ]);

        $orderId = $createRes->json('data.id');

        // User A accesses their own order -> 200 OK
        $resA = $this->actingAs($userA, 'sanctum')->getJson("/api/v1/orders/{$orderId}");
        $resA->assertStatus(200);

        // User B attempts to access User A's order -> 403 Forbidden
        $resB = $this->actingAs($userB, 'sanctum')->getJson("/api/v1/orders/{$orderId}");
        $resB->assertStatus(403);
    }
}
