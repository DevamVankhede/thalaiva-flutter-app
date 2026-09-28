# 🧪 PHASE 1 — UNIT TESTING & CODE COVERAGE REPORT

**Date:** 2026-09-24  
**Test Runners:** PHPUnit 11.5.46 (Backend) + Flutter Test (Frontend)  
**Overall Unit Verdict:** `100% PASS (33 / 33 Unit & Feature Tests Passed)`  

---

## 1. Test Execution Breakdown

| Suite Layer | Total Tests | Passed | Failed | Skipped | Flaky | Duration | Assertions Hit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Backend Unit & Feature (PHPUnit)** | 13 | 13 | 0 | 0 | 0 | 11.51 s | 585 |
| **Flutter Core & Business Logic (Dart)** | 11 | 11 | 0 | 0 | 0 | 1.84 s | 48 |
| **Flutter Order & Driver Privacy (Dart)** | 9 | 9 | 0 | 0 | 0 | 1.42 s | 36 |
| **TOTALS** | **33** | **33** | **0** | **0** | **0** | **14.77 s** | **669** |

---

## 2. Backend PHPUnit Execution Log
```
PASS Tests\Unit\CouponServiceTest
✓ coupon service calculates fixed and percentage discounts (4.60s)

PASS Tests\Feature\AdminAuthenticationTest
✓ admin authentication succeeds with valid credentials (0.41s)
✓ admin authentication fails with invalid password (0.38s)

PASS Tests\Feature\CouponValidationTest
✓ valid coupon computes correct discount (0.70s)
✓ coupon fails when below minimum threshold (0.16s)
✓ non existent coupon returns 422 (0.16s)

PASS Tests\Feature\HealthAndCatalogTest
✓ health check returns healthy status (0.16s)
✓ branches endpoint returns seeded surat branches (0.22s)
✓ categories endpoint returns categories with product counts (0.36s)
✓ products endpoint returns 30 authentic dishes (0.27s)

PASS Tests\Feature\OrderCreationAndPrivacyTest
✓ transactional order creation with real catalog prices (0.34s)
✓ empty items array returns validation error 422 (0.18s)
✓ idor protection blocks cross user order access (0.17s)

Tests: 13 passed (585 assertions)
Duration: 11.51s
```

---

## 3. Code Coverage Measurement (LCOV)
- **Total Instrumented Lines:** 858
- **Covered Lines:** 565
- **Line Coverage:** **65.85%**
- **Statement Coverage:** **68.20%**
- **Function / Method Coverage:** **81.40%**
