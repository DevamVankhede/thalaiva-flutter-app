<?php

namespace Tests\Feature;

use Tests\TestCase;

class HealthAndCatalogTest extends TestCase
{
    public function test_health_check_returns_healthy_status(): void
    {
        $response = $this->getJson('/api/health');

        $response->assertStatus(200)
            ->assertJson([
                'status' => 'healthy',
                'service' => 'Thalaivaa API',
            ]);
    }

    public function test_branches_endpoint_returns_seeded_surat_branches(): void
    {
        $response = $this->getJson('/api/v1/branches');

        $response->assertStatus(200)
            ->assertJsonStructure([
                'success',
                'data' => [
                    '*' => ['id', 'name', 'slug', 'is_active'],
                ],
            ]);

        $this->assertCount(3, $response->json('data'));
    }

    public function test_categories_endpoint_returns_categories_with_product_counts(): void
    {
        $response = $this->getJson('/api/v1/categories');

        $response->assertStatus(200)
            ->assertJsonStructure([
                'success',
                'data' => [
                    '*' => ['id', 'name', 'slug', 'products_count'],
                ],
            ]);

        $this->assertGreaterThanOrEqual(6, count($response->json('data')));
    }

    public function test_products_endpoint_returns_30_authentic_dishes(): void
    {
        $response = $this->getJson('/api/v1/products');

        $response->assertStatus(200)
            ->assertJsonStructure([
                'success',
                'data' => [
                    '*' => [
                        'id', 'name', 'slug', 'category_name', 'base_price_paise',
                        'price_inr', 'is_veg', 'variants', 'modifier_groups',
                    ],
                ],
            ]);

        $this->assertGreaterThanOrEqual(30, count($response->json('data')));
    }
}
