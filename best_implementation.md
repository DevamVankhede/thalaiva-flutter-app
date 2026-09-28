# Thalaivaa API — Best Implementations Report

**Scope:** Solid, well-engineered parts of the Thalaivaa multi-branch restaurant SaaS backend (Laravel 11 + Filament 3).
**Method:** Full source scan + live verification. Facts marked `[VERIFIED]` were confirmed by running code/tests; `[SOURCE]` means confirmed by direct source inspection.
**Companion document:** `report.md` covers remaining gaps; this report intentionally documents what is *done well*.

---

## Scorecard of strengths

| Area | Status | Evidence |
|---|---|---|
| Architecture (service layer, thin controllers, FormRequests) | SOLID | `[SOURCE]` app/Services, app/Http/Controllers, app/Http/Requests |
| Database schema (25 tables, real FKs, UUIDs) | SOLID | `[SOURCE]` database/migrations |
| Money handling (integer paise, server-side pricing) | SOLID | `[SOURCE]` OrderService, migrations |
| Order pipeline (transactional, snapshots, status log, payments) | SOLID | `[VERIFIED]` tests + migration schema |
| Auth foundation (hashed OTP, Sanctum, admin guard) | SOLID | `[SOURCE]` AuthController, Admin.php |
| IDOR / ownership protection | SOLID | `[VERIFIED]` test passes — 403 on cross-user |
| Coupon engine | SOLID | `[VERIFIED]` 5 coupon tests pass |
| API design (versioning, envelope, pagination) | SOLID | `[SOURCE]` routes/api.php, controllers |
| Filament admin (24 resources, dedicated guard, auto-discovery) | SOLID | `[VERIFIED]` 24 resources, 27+ admin routes |
| Seeders (idempotent, real Surat menu) | SOLID | `[SOURCE]` DatabaseSeeder |
| Test suite (13 tests / 585 assertions, green) | SOLID | `[VERIFIED]` `php artisan test` → 13 passed, 585 assertions |
| Ops groundwork (.env.example, .gitignore, phpunit config) | SOLID | `[SOURCE]` |

---

## 1. Architecture — separation of concerns

The codebase follows a clean Layered architecture, which is rare to see this well done in a young project:

- **Thin controllers** — HTTP/JSON handling only (`app/Http/Controllers/Api/V1/OrderController.php` is 178 lines and does no business logic).
- **Service layer** — real business rules live in `app/Services/OrderService.php` and `app/Services/CouponService.php`, both unit-testable and reusable.
- **FormRequest validation** — `CreateOrderRequest` and `ValidateCouponRequest` centralize validation with a consistent custom JSON error envelope (`422 {success:false, errors:{...}}`).
- **Dependency injection** — `OrderController` receives `OrderService` via constructor; `OrderService` receives `CouponService`. Loose coupling, testable with mocks.
- **Domain namespace** — API v1 controllers isolated under `Api\V1`, enabling a clean `api/v2` later.

`[VERIFIED]` — the whole stack works: request → service → transaction → response, end to end, proven by the feature tests.

---

## 2. Database schema — genuinely good data modeling

`database/migrations/` contains 4 cohesive migrations creating **25 tables**, and the modeling choices are clearly considered:

- **UUID primary keys** everywhere, generated via `Order::create(['id' => (string) Str::uuid()])` — table IDs are not guessable/enumerable (feeds the IDOR defense).
- **Real foreign keys with intent-driven `ON DELETE` behavior** (`[SOURCE]` migrations):
  - `cascade` — children that only make sense with their parent (`categories`→`branches`, `order_items`→`orders`).
  - `restrict` — financial/operational records you must never silently orphan (`orders`→`users`, `orders`→`branches`, `payments`→`orders`).
  - `nullOnDelete` — optional links (`cart_items.variant_id`, `delivery_assignments.partner_id`).
- **Composite primary keys on pivot tables** — `product_modifier_links(product_id, modifier_group_id)` and `rbac_role_permissions(role_id, permission_id)` — no phantom surrogate IDs.
- **Unique constraints** that encode business rules — `branches.slug`, `users.phone`, `users.email`, `coupons.code`, `orders.order_number`, plus scoped `unique(branch_id, slug)` on categories and products (per-branch slugs — correct for a multi-branch SaaS).
- **Postgres integrity check constraints** — `orders.total_amount = subtotal + tax - discount + delivery_charge` and `order_items.line_total = unit_price * quantity` enforce arithmetically consistent ledgers at the database level (`[SOURCE]` `create_core_phase2_tables.php:36,73`).
- **Indexes on lookups** — `otp_codes.phone`, `order_status_logs.order_id`, `delivery_assignments.order_id`.
- **Schema comments** — in-paise conventions and FK-restrict rationale are documented inline in the code.

Money is stored as **`bigInteger` paise**, never floats — this is the single most important correctness decision in a food-ordering app and it is done right.

---

## 3. Money handling — integer paise end to end

Pricing flows through the entire system as integer paise and is **computed by the server from the catalog**, never trusted from the client (`[SOURCE]` `OrderService.php`):

- Product `base_price` + variant `price_adjustment` + modifier `price_adjustment` combine server-side (`OrderService.php:85-124`).
- Each money field gets an explicit integer cast in its model (`Order.php:39-47`, `Payment.php:20-23`).
- Discounts are **capped at the subtotal** (`CouponService.php:59`) — a client can never drive a negative total.
- Tax = 5% of (subtotal − discount) and delivery charge are computed server-side in a single place (`OrderService.php:159-166`).
- The API converts to INR only at the *response edge* (`round($x / 100, 2)`) — consistent, single conversion point.

---

## 4. Order system — transactional with real integrity

`OrderService::createOrder()` is a textbook DB transaction (`[SOURCE]` + `[VERIFIED]` by `test_transactional_order_creation_with_real_catalog_prices`):

1. **Branch must exist and be active** — fails fast with a 422, not silent fallback.
2. **Guest → user resolution** via phone (`firstOrCreate`), or explicit auth user.
3. **Per-item server-side re-pricing** — product availability, quantity ≥ 1, variant must belong to the product and be available, modifier prices pulled from DB (`OrderService.php:72-137`).
4. **Coupon re-validation inside the transaction** against the *server-computed* subtotal.
5. **Atomic persistence** of order + items + status log + payment record in one `DB::transaction` — no partial orders.
6. **Historical snapshots** — `product_name_snapshot`, `variant_name_snapshot`, `modifier_snapshot_json` freeze what the customer actually ordered, so later catalog edits never corrupt order history (`[SOURCE]` `OrderService.php:128-136`, `order_items` migration).
7. **Audit trail at birth** — every order gets an `OrderStatusLog` row (`from_status: null → pending`) with actor (`customer`) and note (`OrderService.php:202-210`).
8. **Payment record created and linked** — `Payment` row with amount, currency INR, lifecycle `created/pending`, then `orders.payment_id` set (`OrderService.php:213-223`).
9. **Collision-resistant order numbers** — `THL-YYYYMMDD-RANDOM` (`OrderService.php:169`).

The ownership check on `OrderController::show()` returns **403** when a logged-in user accesses another user's order — `[VERIFIED]` by `test_idor_protection_blocks_cross_user_order_access` (asserts 403). Access via UUID *or* human-friendly `order_number` is supported (`OrderController.php:112-116`).

---

## 5. Auth foundation

The auth layer has genuinely sound pieces:

- **OTP is stored hashed** — `Hash::make($otp)` in `OtpCode.code_hash`, never plaintext (`AuthController.php:32`, schema docs). Verification uses `Hash::check`.
- **OTP lifecycle fields** — `expires_at` (10-min), `verified_at` toggle, and an `attempts` counter are modeled from day one; the query only matches un-verified, un-expired codes (`AuthController.php:60-64`).
- **Phone normalization** — input scrubbed with `preg_replace('/[^\d+]/', '')` at both send and verify so `+91...` and `91...` book to the same account.
- **Sanctum token auth** — `createToken('customer-app')` on verify, `me` endpoint behind `auth:sanctum`, and **token revocation on logout** (`currentAccessToken()->delete()`, `AuthController.php:134`).
- **Dedicated admin guard** — `Admin` model implements Filament's `FilamentUser`, maps auth password to `password_hash` via `getAuthPassword()/getAuthPasswordName()`, hides the hash from serialization, and gates panel access on `is_active` (`Admin.php:32-45`). The panel is bound to `->authGuard('admin')` (`AdminPanelProvider.php:31`).
- `[VERIFIED]` — `test_admin_authentication_succeeds_with_valid_credentials` and `..._fails_with_invalid_password` both pass.

---

## 6. Coupon engine

`CouponService::validateCoupon()` is a complete, self-contained promotion kernel (`[VERIFIED]` by 5 passing tests):

- Case-insensitive code lookup (`strtoupper(trim(...))`), active-only.
- Expiry check against `expires_at`.
- Hard usage cap (`max_uses` vs `used_count`).
- Minimum-order thresholds (e.g., `FEAST100` requires ₹500) enforced server-side — not the frontend.
- Both `percent` and `fixed` (INR) calculation paths, with the discount converted into paise and **capped at the subtotal**.
- `recordCouponUse()` increments `used_count` so redemption limits actually move.
- Rich, human-readable messages (`"Coupon 'THALAIVAA50' requires a minimum order of ₹200…"`) surfaced via a consistent 422 JSON envelope (`CouponController.php:38-41`).

---

## 7. API design — developer-friendly and consistent

`routes/api.php` shows intentional API craft:

- **Versioning** — everything lives under `/api/v1/...`, plus comments-backed legacy aliases for older clients (`api.php:52-59`) — backwards compatibility without breaking consumers.
- **Health check** — `/api/health` returns status/service/version/ISO timestamp for simple uptime monitoring (`api.php:17-24`).
- **Consistent envelope** — every endpoint responds `{success: bool, data|message: ...}`; errors are always `{success: false, message}` with correct status codes (422 validation, 403 auth, 404 not found).
- **Pagination with meta** — products and orders return `{total, per_page, current_page, last_page}` (`CatalogController.php:120-126`).
- **Eager loading everywhere** — no N+1 in `products` (`category`, `variants`, `modifierLinks.modifierGroup.options`), `show` (`items.product`, `branch`, `statusLogs`, `payments`), or `index`.
- **Clean serializers** — the products transformer flattens nested catalog data into a mobile-friendly shape (`base_price_paise` + `price_inr`, `modifier_groups[].options[].price_adjustment` + `price_inr`) (`CatalogController.php:97-114`).
- **Guarded middleware split** — most endpoints are public (catalog), only `me`/`logout` sit behind `auth:sanctum` (`api.php:46-49`).

---

## 8. Filament admin — well-wired

The admin panel is structurally sound even where individual resources still need schema fixes (documented in `report.md`):

- **24 resources** across the full domain (catalog, orders, payments, RBAC, POS, delivery, customers) — the whole data model is surfaced to admins.
- **Auto-discovery** (`discoverResources`/`discoverPages`) — resources and pages register themselves; no manual registration drift.
- **Dedicated admin guard + login page** — `->login()` with `->authGuard('admin')` keeps staff auth fully separate from the customer API (`AdminPanelProvider.php:30-31`).
- **Navigation groups** — e.g., `NavigationGroup('Menu & Catalog')` on `ProductResource`, keeping a 24-resource sidebar organized.
- **Live slug auto-generation** — `ProductResource` fills `slug` from the name on create via `->afterStateUpdated(fn ... => $set('slug', Str::slug($state)))` (`ProductResource.php:31-32`).
- **Admin-friendly money rendering** — prices shown as `₹180.00` from paise (`ProductResource.php:54`).
- **Branding** — brand name + primary color `#FF6B00` thermale into `Panel` config.

---

## 9. Seeders — idempotent, realistic, demo-ready

`DatabaseSeeder.php` is genuinely well-built (`[SOURCE]`):

- **Fully idempotent** — `firstOrCreate`/`updateOrInsert` throughout, so `db:seed` can be re-run safely, differentiating it from appending seeders most projects ship.
- **Realistic Surat domain data** — 3 real branches (City Light / Vesu / Adajan) with valid addresses and phone numbers; 30 actual dishes across 7 categories, with authentic prices in paise (₹50 Kiwi cooler → ₹320 Executive Thali), veg/spicy flags, an emoji + descriptions + ratings in `meta_json`.
- **Per-branch catalog** — every branch gets its own categories and products with branch-scoped slugs (`ghee-roast-masala-dosa-thalaivaa-vesu`), plus a shared modifier group and product–modifier links — validating the multi-branch model.
- **Seedable RBAC** — 3 roles (`super_admin`, `branch_manager`, `kitchen_operator`), 5 permissions, role↔permission links, and an admin assignment — the skeleton of the permission system ships working.
- **Seedable coupons** — `THALAIVAA50` / `FEAST100` with validity windows and usage caps.

---

## 10. Testing — real coverage of real behavior

The suite is compact but *behavioral* — it tests outcomes, not implementation (`[VERIFIED]` `php artisan test` → **13 passed, 585 assertions**, ~18s):

- **Catalog** — health check, the 3 seeded branches, categories with product counts, ≥30 products with the full expected response shape.
- **Coupons** — correct discount math for fixed codes, minimum-threshold rejection, and 422 for unknown codes.
- **Admin auth** — guard-level password success/failure (not a mocked login).
- **Orders** — real `DB` order creation asserting DB rows for `orders` *and* `order_status_logs`; empty-items 422; and the **IDOR 403** case as a first-class privacy test.
- **Unit** — `CouponService` price math (₹50 → 5000 paise, ₹100 → 10000 paise) against the paise boundary.

`phpunit.xml.dist` is configured for isolation — `sqlite :memory:`, `bcrypt rounds 4`, `queue sync`, `array` cache/session — so tests are fast, hermetic, and safe to run anywhere (`[SOURCE]`).

---

## 11. Ops groundwork

- **`.env.example`** documents the full production surface — PostgreSQL connection, Razorpay keys, Soketi realtime keys, queue/cache/session drivers — so a real deployment can be stood up from a checklist (`[SOURCE]`).
- **Solid `.gitignore`** — env files, sqlite files, vendor, key files, and editor cruft are all excluded.
- **Standard Laravel 11 config tree** — all framework configs registered and intact.

---

## 12. What this means

The engineering **foundation is solid and production-shaped**: correct money handling, transactional order integrity, ownership/enumeration defense, hashed secrets at rest, idempotent seed data, and a green behavioral test suite that guards the payout path and the privacy path. These are the hard parts of a food-ordering SaaS and they were built properly.

Remaining work (documented exhaustively in `report.md` as blockers B1–B9) is *completion work* on top of this foundation — not a re-do of it. The natural next milestone is making every Filament resource create/list-safe and freeing order pricing/payment from remaining front-end trust assumptions.

*Generated 2026-09-12. Verified against the live source tree and a passing test run (13 passed / 585 assertions).*