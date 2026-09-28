<?php

namespace Tests\Unit;

use App\Services\CouponService;
use Tests\TestCase;

class CouponServiceTest extends TestCase
{
    public function test_coupon_service_calculates_fixed_and_percentage_discounts(): void
    {
        $service = new CouponService();

        // 1. THALAIVAA50 (Fixed Rs 50 = 5000 paise on Rs 300 = 30000 paise)
        $result = $service->validateCoupon('THALAIVAA50', 30000);
        $this->assertEquals(5000, $result['discount_paise']);
        $this->assertEquals(50.0, $result['discount_inr']);

        // 2. FEAST100 (Fixed Rs 100 = 10000 paise on Rs 600 = 60000 paise)
        $resultFeast = $service->validateCoupon('FEAST100', 60000);
        $this->assertEquals(10000, $resultFeast['discount_paise']);
        $this->assertEquals(100.0, $resultFeast['discount_inr']);
    }
}
