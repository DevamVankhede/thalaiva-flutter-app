<?php

namespace Tests\Feature;

use App\Models\Order;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class MultiUserAuthAndOrderIsolationTest extends TestCase
{
    /**
     * Test 1: User A valid login.
     */
    public function test_user_a_valid_login_returns_token_and_user_profile(): void
    {
        $response = $this->postJson('/api/v1/auth/login', [
            'email' => 'usera@test.com',
            'password' => 'Password123!',
        ]);

        $response->assertStatus(200)
            ->assertJson([
                'success' => true,
                'user' => [
                    'email' => 'usera@test.com',
                    'name' => 'Aarav Sharma',
                ],
            ]);

        $this->assertNotEmpty($response->json('token'));
        $this->assertNotEmpty($response->json('user.id'));
    }

    /**
     * Test 2: User B valid login.
     */
    public function test_user_b_valid_login_returns_token_and_user_profile(): void
    {
        $response = $this->postJson('/api/v1/auth/login', [
            'email' => 'userb@test.com',
            'password' => 'Password123!',
        ]);

        $response->assertStatus(200)
            ->assertJson([
                'success' => true,
                'user' => [
                    'email' => 'userb@test.com',
                    'name' => 'Bhavna Patel',
                ],
            ]);

        $this->assertNotEmpty($response->json('token'));
    }

    /**
     * Test 3: User C valid login.
     */
    public function test_user_c_valid_login_returns_token_and_user_profile(): void
    {
        $response = $this->postJson('/api/v1/auth/login', [
            'email' => 'userc@test.com',
            'password' => 'Password123!',
        ]);

        $response->assertStatus(200)
            ->assertJson([
                'success' => true,
                'user' => [
                    'email' => 'userc@test.com',
                    'name' => 'Chirag Mehta',
                ],
            ]);

        $this->assertNotEmpty($response->json('token'));
    }

    /**
     * Test 4: Invalid password rejects authentication.
     */
    public function test_invalid_password_is_rejected(): void
    {
        $response = $this->postJson('/api/v1/auth/login', [
            'email' => 'usera@test.com',
            'password' => 'WrongPassword123',
        ]);

        $response->assertStatus(401)
            ->assertJson([
                'success' => false,
                'message' => 'Invalid email or password.',
            ]);
    }

    /**
     * Test 5: Unknown email rejects authentication.
     */
    public function test_unknown_email_is_rejected(): void
    {
        $response = $this->postJson('/api/v1/auth/login', [
            'email' => 'nonexistent@test.com',
            'password' => 'Password123!',
        ]);

        $response->assertStatus(401)
            ->assertJson([
                'success' => false,
                'message' => 'Invalid email or password.',
            ]);
    }

    protected function authenticatedGet(string $uri, string $token)
    {
        auth()->forgetGuards();
        return $this->withToken($token)->getJson($uri);
    }

    protected function authenticatedPost(string $uri, array $data, string $token)
    {
        auth()->forgetGuards();
        return $this->withToken($token)->postJson($uri, $data);
    }

    /**
     * Test 6: User A sees only User A's orders.
     */
    public function test_user_a_sees_only_user_a_orders(): void
    {
        $userA = User::where('email', 'usera@test.com')->first();
        $tokenA = $userA->createToken('test-a')->plainTextToken;

        $response = $this->authenticatedGet('/api/v1/orders', $tokenA);

        $response->assertStatus(200)
            ->assertJson(['success' => true]);

        $orders = $response->json('data');
        $this->assertCount(3, $orders);

        $orderNumbers = collect($orders)->pluck('order_number')->all();
        $this->assertContains('ORD-001', $orderNumbers);
        $this->assertContains('ORD-002', $orderNumbers);
        $this->assertContains('ORD-003', $orderNumbers);
        $this->assertNotContains('ORD-004', $orderNumbers);
    }

    /**
     * Test 7: User B sees only User B's orders.
     */
    public function test_user_b_sees_only_user_b_orders(): void
    {
        $userB = User::where('email', 'userb@test.com')->first();
        $tokenB = $userB->createToken('test-b')->plainTextToken;

        $response = $this->authenticatedGet('/api/v1/orders', $tokenB);

        $response->assertStatus(200)
            ->assertJson(['success' => true]);

        $orders = $response->json('data');
        $this->assertCount(1, $orders);

        $orderNumbers = collect($orders)->pluck('order_number')->all();
        $this->assertContains('ORD-004', $orderNumbers);
        $this->assertNotContains('ORD-001', $orderNumbers);
        $this->assertNotContains('ORD-002', $orderNumbers);
        $this->assertNotContains('ORD-003', $orderNumbers);
    }

    /**
     * Test 8: User C sees 0 orders (empty state).
     */
    public function test_user_c_sees_zero_orders_clean_empty_state(): void
    {
        $userC = User::where('email', 'userc@test.com')->first();
        $tokenC = $userC->createToken('test-c')->plainTextToken;

        $response = $this->authenticatedGet('/api/v1/orders', $tokenC);

        $response->assertStatus(200)
            ->assertJson([
                'success' => true,
                'data' => [],
                'meta' => [
                    'total' => 0,
                ],
            ]);
    }

    /**
     * Test 9: User A requests User B's order -> 403 Forbidden.
     */
    public function test_user_a_cannot_access_user_b_order(): void
    {
        $userA = User::where('email', 'usera@test.com')->first();
        $tokenA = $userA->createToken('test-a')->plainTextToken;

        $orderB = Order::where('order_number', 'ORD-004')->first();

        $response = $this->authenticatedGet("/api/v1/orders/{$orderB->id}", $tokenA);

        $response->assertStatus(403)
            ->assertJson([
                'success' => false,
                'message' => 'Unauthorized access to this order.',
            ]);
    }

    /**
     * Test 10: User B requests User A's order -> 403 Forbidden.
     */
    public function test_user_b_cannot_access_user_a_order(): void
    {
        $userB = User::where('email', 'userb@test.com')->first();
        $tokenB = $userB->createToken('test-b')->plainTextToken;

        $orderA = Order::where('order_number', 'ORD-001')->first();

        $response = $this->authenticatedGet("/api/v1/orders/{$orderA->id}", $tokenB);

        $response->assertStatus(403)
            ->assertJson([
                'success' => false,
                'message' => 'Unauthorized access to this order.',
            ]);
    }

    /**
     * Test 11: Logout invalidates token and prevents subsequent order access.
     */
    public function test_logout_revokes_token_and_blocks_order_access(): void
    {
        $loginRes = $this->postJson('/api/v1/auth/login', [
            'email' => 'usera@test.com',
            'password' => 'Password123!',
        ]);
        $token = $loginRes->json('token');

        // Verify order access works before logout
        $beforeRes = $this->authenticatedGet('/api/v1/orders', $token);
        $beforeRes->assertStatus(200);

        // Perform logout
        $logoutRes = $this->authenticatedPost('/api/v1/auth/logout', [], $token);
        $logoutRes->assertStatus(200)
            ->assertJson(['success' => true]);

        // Attempt order access after logout -> 401 Unauthenticated
        $afterRes = $this->authenticatedGet('/api/v1/orders', $token);
        $afterRes->assertStatus(401);
    }

    /**
     * Test 12: Refresh / Me endpoint returns current authenticated user.
     */
    public function test_me_endpoint_returns_authenticated_user_identity(): void
    {
        $userB = User::where('email', 'userb@test.com')->first();
        $tokenB = $userB->createToken('test-me')->plainTextToken;

        $response = $this->authenticatedGet('/api/v1/auth/me', $tokenB);

        $response->assertStatus(200)
            ->assertJson([
                'success' => true,
                'data' => [
                    'id' => $userB->id,
                    'name' => 'Bhavna Patel',
                    'email' => 'userb@test.com',
                ],
            ]);
    }

    /**
     * Test 13: Concurrent / simultaneous sessions maintain data isolation.
     */
    public function test_concurrent_sessions_maintain_data_isolation(): void
    {
        $loginA = $this->postJson('/api/v1/auth/login', [
            'email' => 'usera@test.com',
            'password' => 'Password123!',
        ]);
        $tokenA = $loginA->json('token');

        $loginB = $this->postJson('/api/v1/auth/login', [
            'email' => 'userb@test.com',
            'password' => 'Password123!',
        ]);
        $tokenB = $loginB->json('token');

        // Session A query
        $resA = $this->authenticatedGet('/api/v1/orders', $tokenA);
        // Session B query
        $resB = $this->authenticatedGet('/api/v1/orders', $tokenB);
        // Re-query Session A to ensure no overwritten global state
        $resA2 = $this->authenticatedGet('/api/v1/orders', $tokenA);

        $this->assertCount(3, $resA->json('data'));
        $this->assertCount(1, $resB->json('data'));
        $this->assertCount(3, $resA2->json('data'));

        $this->assertEquals('ORD-004', $resB->json('data.0.order_number'));
        $this->assertNotEquals($resA->json('data.0.order_number'), $resB->json('data.0.order_number'));
    }

    /**
     * Test 14: Phone number login alternative works.
     */
    public function test_phone_number_login_works(): void
    {
        $response = $this->postJson('/api/v1/auth/login', [
            'phone' => '+919800000001',
            'password' => 'Password123!',
        ]);

        $response->assertStatus(200)
            ->assertJson([
                'success' => true,
                'user' => [
                    'name' => 'Aarav Sharma',
                ],
            ]);
    }

    /**
     * Test 15: Unauthenticated orders request returns 401.
     */
    public function test_unauthenticated_orders_request_returns_401(): void
    {
        auth()->forgetGuards();
        $response = $this->getJson('/api/v1/orders');
        $response->assertStatus(401);
    }
}
