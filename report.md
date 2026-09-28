# Project Audit Report — Thalaivaa Multi-Branch Restaurant SaaS

**Repository audited:** `C:\Users\Admin\thalaivaa_api`
**Audit date:** 2026-09-12 (re-audit / full re-scan after substantial code changes)
**Auditor:** Senior Principal Software Architect / Full-Stack Engineer / QA Lead / Security Engineer / Product Reviewer
**Type:** Evidence-based, read-only audit (no source code was modified; the developer's real DB `database/database.sqlite` was only read for counts, never written)

> **Evidence rule used throughout:** every finding cites `file:line` / class / route and was confirmed by source inspection and/or live runtime tests (PHP 8.5.10, Laravel 11.56.1, Filament v3.3.55, SQLite). All destructive/runtime tests ran on **disposable SQLite copies** (`%TEMP%\opencode\db_runtime2.sqlite`) with `php artisan serve --port=8001`; the temp server was shut down after testing. Anything that could not be executed is explicitly marked `NOT VERIFIED`.

---

## 1. Executive Summary

### Project overview
Thalaivaa is a **multi-branch South Indian restaurant SaaS platform** (Surat, Gujarat, India). `thalaivaa_api` is the **Laravel 11 backend API + Filament v3 admin panel**. The customer-facing mobile app lives outside this repo (`C:\Users\Admin\thalaivaa_flutter`, Flutter + Riverpod). `figma_mockups/` and `Thalaivaa_Glimpse_Preview.html` hold static design mockups.

### What now actually exists (verified in this re-scan)
| Component | Status (verified) |
| --- | --- |
| Laravel 11.56.1 / PHP 8.5.10 / Filament v3.3.55 / Livewire v3.8.8 / Sanctum v4 | Boots; `GET /api/health` → 200 |
| Migrations | **4 migrations** → `migrate --force` clean on fresh SQLite; **25 business tables** now exist (all 10 previously-missing tables added) |
| Eloquent models | **24 models**, incl. new `UserProfile`, `OtpCode`, `ProductVariant` |
| `App\Models\User` / `Admin` | Now `Authenticatable`; `Admin` implements `FilamentUser`; `User` uses `HasApiTokens` |
| Filament resources | **All 23 resources now define `getPages()`** + Pages folders; `route:list` shows full admin CRUD (47 admin routes) |
| Admin login | **Verified working** (`Auth::guard('admin')->attempt(...)` → PASS, test-green; login page renders) |
| Public API | Now controller-based: `AuthController` / `CatalogController` / `CouponController` / `OrderController`, `FormRequest`s, `OrderService` / `CouponService` |
| OTP auth | **Works end-to-end (live):** send → verify → Sanctum token → `/auth/me`; IDOR blocked (403, live) |
| Order creation | Transactional (`DB::transaction`), validated (`CreateOrderRequest`), real catalog prices, status log + payment record written |
| Tests | `phpunit.xml.dist` present; **`php artisan test` → 13 passed (344 assertions)** |
| Git hygiene | `.gitignore` added (vendor/.env/*.sqlite covered); **still not a git repository** |
| Flutter customer app | **Still 100% mock/hard-coded** — `http` package added to `pubspec.yaml` but **zero** HTTP usage in `lib/` |
| Realtime / RBAC / payments / POS / delivery | Real **tables** exist; **runtime logic still missing/fiction** (see §6, §8, §16) |

### Current state — one sentence
The backend is now a **credible, testable API skeleton** (auth, catalog, coupons, transactional orders, 13 green tests, all 23 admin routes alive) but is **not yet a working SaaS**: several admin screens still crash or silently drop data, payments are simulated, pricing can be influenced by the client, RBAC/realtime/POS/delivery are inert, and the customer app never calls the API.

---

### Overall SaaS Readiness Score

**44 / 100 — STILL NOT READY for production** (up from 24/100; see §3 for weights).

Progress is real — the two original "can't-operate" blockers (no login, dead resources) are fixed and 13 tests pass — but the revenue core (real payment capture) and the customer-facing product (Flutter wired to API) remain unimplemented, and the admin panel has new runtime defects introduced by schema/column mismatches.

---

### Issue counts (re-audit)
- 🔴 **P0 (Critical / Blocking) — 9**
- 🟠 **P1 (High) — 14**
- 🟡 **P2 (Medium) — 12**
- 🔵 **P3 (Low) — 8**
- 🟢 **P4 (Enhancement) — 8**

### Major strengths (now verified)
1. **Admin login fixed and testably correct** — `Admin` is `Authenticatable` + `FilamentUser`, dedicated `admin` guard + provider (`config/auth.php`), `getAuthPassword()` maps `password_hash`, `canAccessPanel()` gates on `is_active`. `Auth::guard('admin')->attempt(...)` passes.
2. **All 23 Filament resources have real routes/pages** — `route:list` confirms every resource reachable.
3. **10 previously-missing tables migrated** — OTP, profiles, cart, status logs, RBAC (roles/permissions/assignments), POS, delivery partner + assignments, Sanctum tokens. Fresh `migrate --force` verified.
4. **Real API architecture** — controllers, `FormRequests` (JSON 422 envelope), `OrderService` (transaction, catalog prices, coupon integration, status log, payment row), `CouponService` (fixed/percent, min-order, expiry, max-uses).
5. **OTP flow works live** (send → verify → token → me) with hashed codes and expiry.
6. **Transactional orders** — invalid product no longer leaves orphan rows; empty items → 422; **IDOR blocked (403)** for cross-user access (live-verified).
7. **13 automated tests green** — admin auth, coupon matrix, health/catalog, order creation + privacy, coupon service unit tests.
8. **Brand color applied** to Filament (`Color::hex('#FF6B00')`).
9. **`.gitignore` added** covering vendor, `.env`, `*.sqlite`.

### Biggest risks (current)
1. **Admin panel has runtime crashes + silent data loss** — column/relationship mismatches in `OrderResource`, `PaymentResource`, `CategoryResource`, `ModifierGroupResource`, `ModifierOptionResource`, `OrderItemResource`, `CouponResource`, `ProductResource`, `RBAC*`, `POS*`, `Delivery*` (verified; §4 B1–B6). Screens either 500 or silently save blanks.
2. **Payments are simulated** — no Razorpay SDK, no capture/refund/webhook; a client can pass `payment_status=paid` and instantly get a "captured" record; `orders.payment_id` is never populated (live-verified bypass).
3. **Order pricing integrity hole** — modifier add-on prices are accepted from the client (live-verified: ₹999.99 add-on persisted into totals).
4. **RBAC is tables + UI only** — zero roles/permissions seeded, no policies, no enforcement; every admin is superuser.
5. **Flutter app still never calls the API** — the product's customer side is a static mock (`http` in pubspec, zero usages).
6. **Realtime is fiction** — `BROADCAST_CONNECTION=log`, no events/channels/`broadcasting.auth`; the "live order tracking / Soketi" claim has no code.

### Most important next actions
1. Fix the 9 admin runtime defects (schema/column/relationship mismatches) — §25 Phase 0.
2. Replace mock payments with a real gateway flow (Razorpay order → callback → capture); remove client `payment_status` trust; server-side modifier pricing.
3. Seed + enforce RBAC (roles/permissions/assignments + policies) or remove the ambert label "23 resources" until real.
4. Wire the Flutter app to `/api/v1` (real HTTP client + serializers) — or relabel it as design prototype.
5. Add CI (lint → test → migrate:fresh), rotate the live `APP_KEY`, and build on a real engine (PostgreSQL) to match `.env.example`.

---

## 2. Project Architecture

### Technology stack (verified)
| Layer | Technology | Evidence |
| --- | --- | --- |
| Backend framework | Laravel **11.56.1** on PHP **8.5.10** | `composer.lock`, `php artisan about` |
| Admin panel | Filament **v3.3.55** + Livewire **v3.8.8** | `php artisan about` |
| API auth | Laravel Sanctum v4 (now **actively used**: `HasApiTokens`, `auth:sanctum`, `personal_access_tokens` migration) | `app/Models/User.php:10`, `routes/api.php` |
| Realtime package | pusher/pusher-php-server 7.3.0 installed, **still unused** (`BROADCAST_CONNECTION=log`) | `composer.json`, config probe |
| Database | **SQLite** (dev, actual); PostgreSQL documented as target; 24-table master DDL outside repo | `.env`, `C:\Users\Admin\thalaivaa_db_ddl.sql` |
| Frontend (customer) | Flutter + Riverpod, `http ^1.2.0` declared but unused | `thalaivaa_flutter/pubspec.yaml`, grep of `lib/` |
| Frontend (admin) | Filament (server-rendered; no `node_modules`) | repo root |

### Directory map (verified via recursive scan)
```
thalaivaa_api/
├─ app/
│  ├─ Filament/Resources/ → 23 resources, each with Pages/ (Manage* pages)  ✅ all wired
│  ├─ Http/
│  │  ├─ Controllers/Api/V1/ → AuthController, CatalogController, CouponController, OrderController
│  │  └─ Requests/           → CreateOrderRequest, ValidateCouponRequest
│  ├─ Models/               → 24 models
│  ├─ Providers/            → AppServiceProvider, Filament/AdminPanelProvider (guard 'admin', #FF6B00)
│  └─ Services/             → OrderService, CouponService
├─ bootstrap/app.php          → default Laravel 11 bootstrap
├─ config/                    → standard Laravel 11 config set (app, broadcasting, database, queue, session,
│                               sanctum, filament, livewire, tinker, ... 21 keys registered — verified via probe)
├─ database/
│  ├─ migrations/             → 4 migrations (25 business tables)
│  └─ seeders/DatabaseSeeder.php
├─ routes/
│  └─ api.php                 → v1 prefix + backward-compatible aliases, controller-based
├─ tests/                     → 5 test files (13 tests), phpunit.xml.dist
├─ figma_mockups/             → 5 static HTML prototypes + design_tokens.json
└─ .gitignore                 → now present (vendor, .env, *.sqlite, logs, IDE)
```

### Entry points
- API: `GET /api/health`, `/api/v1/*` (+ un-prefixed aliases)
- Admin panel: `/admin` (login `/admin/login`, 23 resource sections)
- CLI: `artisan`

### External integrations (all **still not implemented** at runtime)
- **Razorpay** — no SDK in `composer.json`, no `services.razorpay`, no gateway calls; only a mock `Payment::create(['razorpay_payment_id'=>'pay_'.Str::random(14)])` row.
- **Soketi** — env placeholders only; `broadcasting.default=log`; no events, channels, listeners, or `/broadcasting/auth`.
- **POS (Petpooja)** — table (`pos_integration_configs`) + resource only; no sync code.
- **Delivery partners** — tables + resources only; no API calls, no webhooks.
- **SMS/OTP delivery** — OTP is generated and hashed but **never actually sent** (no SMS provider); dev debug codes returned in the response in `local`.
- **AWS S3** — env present, no SDK, storage = local.

---

## 3. Overall SaaS Readiness Score

| Dimension | Weight | Score (/10) | Weighted contribution |
| --- | ---: | ---: | ---: |
| Functionality | 25% | 5 | 12.5 |
| Reliability | 15% | 4 | 6.0 |
| UI/UX | 15% | 5 | 7.5 |
| Security | 15% | 4 | 6.0 |
| Architecture | 10% | 6 | 6.0 |
| Performance | 10% | 3 | 3.0 |
| Testing | 5% | 6 | 3.0 |
| DevOps/Deployment | 5% | 1 | 0.5 |
| **Total** | 100% | — | **44.5 → 44/100** |

**Why not higher:** ordering + auth + tests + an alive admin are real, but the money path is not (mock payments, client-trusted `payment_status`, client-supplied add-on prices), several admin screens crash or lose data, RBAC/realtime/delivery/POS carry no runtime logic, the customer app is disconnected, and there is no CI/deployment despite a live `APP_KEY` sitting in `.env`.

---

## 4. Critical Blockers

| # | Prio | Blocker | Evidence | Impact | Required Fix | Verification |
| - | --- | --- | --- | --- | --- | --- |
| B1 | 🔴 P0 | **Admin resource/DB column mismatches → blank columns & silent data loss-ish (6 resources).** `OrderResource.php:34,47` uses `total_amount_paise` (column is `total_amount`); `PaymentResource.php:24-28` uses `provider`, `gateway_payment_id`, `gateway_order_id`, `amount_paise` (columns are `razorpay_payment_id`, `amount`, `status`, …); `CouponResource.php` uses `expires_at` (columns `valid_from`/`valid_to`); `CategoryResource.php` uses `icon_emoji`, `description` (no such columns); `ModifierGroupResource.php` uses `slug` (no such column); `OrderItemResource.php` uses `unit_price_paise`/`total_price_paise` (columns `unit_price`/`line_total`). | Probe on disposable DB: `$order->total_amount_paise → null`, `$coupon->expires_at → null`, `$category->icon_emoji → null` (attribute access silently returns null). | Admin cannot read/write these fields; amounts, payment gateways, coupon expiry, category emojis are **blank in UI**; edits overwrite data with nulls. | Rename fields to true columns (or add the missing columns); align form/table with schema. | Create+Edit cycles persist correct values; table shows real data. |
| B2 | 🔴 P0 | **Create crashes: NOT-NULL / PK on 8 resources.** `ProductResource` form lacks `branch_id` (`products.branch_id` NOT NULL); `CategoryResource`/`ModifierGroupResource` likewise (branch_id NOT NULL, no field); `RbacRole`/`RbacPermission` have no `HasUuids` and no `id` supplied → NULL uuid PK; `PosIntegrationConfig`, `DeliveryPartnerIntegration`, `DeliveryAssignment`, `AdminRbacAssignment` likewise no id generation. | Probe: `Product::create(...)` → `NOT NULL constraint failed: products.branch_id`; `RbacRole::create(...)` → `NOT NULL constraint failed: rbac_roles.id`; `PosIntegrationConfig::create(...)` → `...pos_integration_configs.id`; `DeliveryAssignment::create(...)` → `...delivery_assignments.id` (all on disposable DB). | Admins cannot create any Product/Category/ModifierGroup/Role/Permission/POS/Delivery/Assignment record — a 500 on Save. | Add `branch_id` selects; add `HasUuids` (or explicit ids) to RBAC/POS/Delivery models. | Create works on every resource; row persisted with correct id. |
| B3 | 🔴 P0 | **List-page crashes on relationship mismatches.** `AdminRbacAssignmentResource` reads `admin.email`, `role.name`, `branch.name` but `AdminRbacAssignment` defines **no** `admin()`/`role()`/`branch()` relations; `RBACRolePermissionResource` reads `role.name`/`permission.name` but `RbacRolePermission` has **no** relations; `ModifierOptionResource` reads `modifierGroup.name` (model defines `group()`, not `modifierGroup()`) and its create form calls `relationship('modifierGroup', …)`. | Probe on disposable DB: accessing `ModifierOption->modifierGroup` → relation resolves to null → `Attempt to read property "name" on null`; relation methods missing on the other two models. | These three admin screens 500 as soon as rows exist / when opening create forms. | Add the relations to the models; align Filament relationship names. | Each list/create/edit page renders 200 with data. |
| B4 | 🔴 P0 | **Payments are fabricated end-to-end (no gateway).** `OrderService.php` creates `Payment::create(['razorpay_payment_id'=>'pay_'.Str::random(14), ..., 'status'=>'captured'/'created'])` with a fake id; **`orders.payment_id` is never set** on the order (stays NULL → `$order->payment()` returns null); no Razorpay SDK, order/callback/verify/capture/refund endpoints, or webhook exist. | Source; `OrderService.php:197-206`; probe: `Order::first()->payment → null`. | Money is booked on fake payloads; reconciliation impossible; multiple "captured" entries from a single request; no way to void/refund. | Real gateway integration (create order → redirect → callback signature-verification → capture) and link `orders.payment_id`. | Webhook sim marks order paid only after verified gateway event; refund flow works. |
| B5 | 🔴 P0 | **`payment_status` is client-trusted ("paid by fiat").** `CreateOrderRequest` allows `payment_status` ∈ {pending, paid}; passing `paid` immediately writes `Payment.status = captured` and `orders.payment_status = paid` with no gateway interaction. | **Live test (disposable DB):** `POST /api/v1/orders` with `payment_status=paid` → `201`, `payment_status=paid`, payment row `captured`. | Anyone can mark an order paid and "pay" without paying. | Remove `payment_status` from request; derive from gateway callback / COD rules; at minimum server-default `pending` + admin action. | Client cannot force `paid`; only verified gateway/admin action sets it. |
| B6 | 🔴 P0 | **Modifier add-on pricing is client-supplied** — order totals are not sealed to the catalog. `OrderService.php:93-104` takes `$mod['price_adjustment'] ?? ($mod['price_inr']*100)` from the request and adds it to the line price. | **Live test:** modifier `price_inr: 999.99` → order `item_line=₹1,179.99` (base ₹180 + ₹999.99), total ₹1,186.49 persisted. `ValidateCouponRequest`-style validation never checks modifier ids/prices server-side. | Pricing fraud / miscalculation; revenue totals unreliable. | Resolve each modifier id against `modifier_options` via `product_modifier_links`, price from DB. | Client price field ignored; total equals DB-sealed math. |
| B7 | 🔴 P0 | **RBAC is inert** — roles/permissions tables are empty (`rbac_roles=0`, `rbac_permissions=0` in real DB and post-seed disposable DB), the seeder creates **no** roles/permissions/assignments, no policies exist (`app/Policies` absent), and `Admin::canAccessPanel()` only checks `is_active`. `FILAMENT_DEVELOPER_REPORT.md` claims `RBACPluginReference.php` gates CRUD — that file does not exist. | Source; `database/seeders/DatabaseSeeder.php` (no RBAC); `app/Models/Admin.php:37-41`; probe counts. | Every admin is a superuser; fine-grained access control sold but not delivered. | Seed standard roles/permissions, wire Filament policies + a permission check in `canAccessPanel`, scope resources by branch. | Two admins with different roles see different menus/actions. |
| B8 | 🔴 P0 | **Customer Flutter app is still 100% mock** — no HTTP usage anywhere in `lib/` (`package:http`/`HttpClient`/`Uri.parse` grep → 0 hits), `auth_provider.dart` is a 1-line placeholder (`StateProvider<bool>(false)`), order/cart/user/settings providers are stubs; `app_providers.dart` still holds 30 hard-coded products, fake order `THL-9482`, client-side coupon logic. `menu_screen.dart:73` hard-codes the category list. | Grep + file reads; `flutter analyze` earlier passed (no network references to fail). | The customer-facing product shows data the API never produced and never hands money to the API. | Add a real repository/serializer layer using `http`; swap static providers; add loading/error/empty states; fix corrupted emoji. | With only the API reachable, app browses, carts, and orders against server truth. |
| B9 | 🔴 P1* | **OTP / SMS is "fire-and-forget"** — `sendOtp` hashes a code (`Hash::make`) but there is **no SMS provider integration**, no throttle/rate limit on the route, `attempts` is stored but never incremented/checked, expired OTPs are never cleaned, and dev bypass codes (`123456`, `999999`) plus `dev_otp` are returned in the response in `local`. | Source `AuthController.php:29-58,60-98`; `routes/api.php` (no throttle). | Unauthenticated SMS spam vector; OTP brute-force window in dev; "dispatched to your phone" message is false — nothing is sent. | Integrate an SMS gateway, add `throttle`, enforce attempts, remove bypasss outside `local`/`testing`. | Real SMS delivered; rate limit 429; attempts exhausted → block. |

---

## 5. High Priority Issues

| # | Prio | Category | Issue | Evidence | Impact |
| - | --- | --- | --- | --- | --- |
| H1 | 🟠 P1 | API | **Guest order escalation / weak guest identity.** `GET /api/v1/orders` returns everything for a `phone` query param without auth; guest-created orders (`OrderController.store` resolves/creates a user from `delivery_phone`) are then viewable by **any unauthenticated caller** using the order id, including full delivery PII (`OrderController.show` has no owner when `$user` is null). | Source `OrderController.php:63-70,76-80,146-153`; live test: guest order fetch with no token → 200 full details. | Delivery name/phone/address exposed without authentication. | Require auth to read orders; guest PII call masked responses. |
| H2 | 🟠 P1 | API | **No API rate limiting anywhere** (auth, coupons, orders, catalog). | `routes/api.php` — no `throttle:` middleware. | Abuse/DoS; OTP & coupon probing. | Add `throttle` per route group. |
| H3 | 🟠 P1 | Security | **`APP_DEBUG=true` in `.env` + a live `APP_KEY` in the working tree.** | `.env` (key present, value withheld in this report). | Error pages leak SQL/stack; exposed key enables session forgery if leaked. | `APP_DEBUG=false` for shared envs; rotate key; never commit `.env` (now ignored, but no repo yet). |
| H4 | 🟠 P1 | Database | **Missing indexes on hot columns** (`orders.user_id`, `orders.status`, `orders.payment_status`, `order_items.order_id` (FK yes, covering no), `payments.order_id` is unique → indexed). | Migrations source. | Degrading joins/filters as order counts grow. | Index `orders(user_id,status)`, `order_items(order_id)`. |
| H5 | 🟠 P1 | API | **`per_page` unclamped** on `/products` and seed `rating`/`rating_count` fabricated still served as live data. | `CatalogController.php:39` `(int)$request->input('per_page',50)`; `DatabaseSeeder.php` (`rating` 4.9, `rating_count = rand(120,680)`), fallback in `CatalogController.php:87-89`. | Huge payloads; fake reviews as facts. | Clamp per_page; move ratings to a real reviews aggregate or omit. |
| H6 | 🟠 P1 | Product | **Branch isolation missing.** `GET /api/v1/products` has **no `branch_id` filter** (doc claims branch filtering); `categories` aren't branch-scoped in the API; neither is coupon validity beyond which branch it belongs to. | `CatalogController.php` (products filters: category/search/is_veg only). | A multi-branch SaaS that cannot serve a specific branch's menu. | Add `branch_id` filter/path; scope catalog queries per branch. |
| H7 | 🟠 P1 | Product | **Delivery/tax rules hard-coded and inconsistent.** `OrderService.php:153-154` `$deliveryChargePaise = ($subtotalPaise >= 100000) ? 0 : 4000` (₹1000 threshold, ₹40 charge) while the comment claims "free over ₹11000"; tax pinned at 5% (`:150`). Seeder/request defaults for delivery remain Surat/pin `395007`/phone. | Source. | Wrong pricing for a real menu; no configurable business rules. | Move to settings/DB; clarify threshold; validate delivery inputs. |
| H8 | 🟠 P1 | API | **`order_number` uses `Str::random(6)`** — no uniqueness retry, collision → unique-constraint 500. | `OrderService.php:163`. | Random failures at scale. | Sequence/counter + retry on collision. |
| H9 | 🟠 P1 | Realtime | **Realtime still fiction.** `broadcasting.default=log`; no `routes/channels.php`, no Event classes, no `broadcasting.auth` route; Soketi env keys ignored. Live tracking claim (UI/UX report) has no implementation. | Config probe; `route:list` (no `/broadcasting/auth`); `app/Events` absent. | Live order tracking / KDS push cannot exist. | Implement events + channels or drop the claim from docs. |
| H10 | 🟠 P1 | UI/UX | **Admin brand/UX partially revived but data-quality issues hurt trust** — blank columns (B1), create failures (B2), and several money fields (`payment_status`) editable directly on `OrderResource` where totals can be set manually (`total_amount_paise`, already a phantom column). | Source of resources. | Operators see empty numbers; manual money entry. | Fix columns; make totals read-only derived displays. |
| H11 | 🟠 P1 | Data | **Cart model vs table mismatch.** `CartItem.php` fillable/casts use `modifier_ids_json` but migration column is `modifiers_json`; `CartItemResource` exposes `user_id` (nullable) — no server cart API exists for customers. | Source. | Server-side cart can never persist modifiers; app cart is client-only. | Align model/columns; add customer cart/patch endpoints. |
| H12 | 🟠 P1 | Data | **`orders.payment_id` never linked** (B4) and `PaymentResource` uses phantom fields (`gateway_*`, `amount_paise`) meaning the real Razorpay id/amount/status aren't shown in admin. | Source; probe `Order::first()->payment → null`. | Admin cannot see payment truth; reports wrong. | Link order↔payment; fix resource fields. |
| H13 | 🟠 P1 | Testing | **13 green tests, but no coverage of the admin panel or RBAC/realtime/payments and no CI to run them.** `phpunit.xml.dist` uses `:memory:` SQLite only. | `tests/` + `phpunit.xml.dist`. | Admin resource regressions (B1-B3) slip through — exactly what happened. | Add resource/render tests + CI (GitHub Actions). |
| H14 | 🟠 P1 | Ops | **Multi-branch seeder scope**: products/modifiers seeded only for the City-Light branch; Vesu/Adajan have no menu; admin/branch assignment tables empty. | `DatabaseSeeder.php` (all dishes → `$cityLightBranch`). | Two of three branches unusable in UI/API. | Seed per-branch or expose branch-menu gaps clearly. |

---

## 6. Functionality Audit — what is wired, what is **left**

Traced every advertised workflow `USER → UI → API → DB → RESPONSE → UI`.

### Feature → Status map (single source of truth for "what's left")

| # | Feature | Backend (API/DB) | Admin panel | Customer app | What is **left** to call it done |
| - | --- | --- | --- | --- | --- |
| F1 | Catalog browse | ✅ `/branches`, `/categories`, `/products` work; products include variants + modifier groups (live) | ⚠️ Product/Category pages — create crashes (B2), some blank cols (B1) | ❌ mocked locally | Fix admin create; add `branch_id` filter; wire app to API |
| F2 | Search / veg filter | ✅ `search`, `is_veg`, `category_id` (live checked shapes) | — | ❌ | Real app search back to API |
| F3 | Branch switching | ✅ 3 branches via API | ✅ Branch CRUD (phone not persisted — fillable gap) | ❌ 3 hard-coded | Persist phone; app branch from API |
| F4 | OTP auth | ✅ send/verify/token/me/logout live | ✅ OTP table + resource | ❌ `auth_provider.dart` 1-line stub | SMS sender, throttle, attempts; app login screen |
| F5 | Cart (server) | ⚠️ table + admin resource exist; **no public cart API** | ⚠️ CartItemResource (quantity only) | ❌ client-only `CartNotifier` | Cart add/update/remove endpoints; modifiers align column; app syncing |
| F6 | Coupons | ✅ `validateCoupon` server-side (fixed/percent/min/expiry/max-uses) + use counter | ✅ CouponResource (but `expires_at` phantom → blank) | ❌ client re-implementation | Admin expiry field fix; single coupon source in app |
| F7 | Place order | ✅ transactional, validated, catalog-priced, status-log + payment row (live) | ⚠️ OrderResource money cols blank/phantom | ❌ local fake `THL-XXXX` | Seal modifier pricing (B6); drop `payment_status` trust (B5); wire app |
| F8 | My Orders / history | ✅ `GET /orders` (owner or phone) + paginate | — | ❌ | Auth-gate + refine guest path (H1); app orders screen |
| F9 | Payments (Razorpay) | ❌ mock `pay_...` + status fiction | ❌ phantom fields | ❌ | Real gateway + webhook + link order; see B4/B5 |
| F10 | Order status transitions | ⚠️ status enum + logs written at creation only; **no transition endpoints/events** | ⚠️ admin can edit `status` field directly (no log written, no broadcast) | ❌ stepper static | Transition service logging `order_status_logs` + events |
| F11 | Realtime / live tracking | ❌ `log` driver, no events/channels | ❌ | ❌ | Implement OrderBroadcast + channels; Soketi wiring |
| F12 | RBAC | ❌ tables empty, no policies | ⚠️ resources exist but create crashes + assignments broken | — | Seed roles/permissions; bind policies; admin role assignment (B7) |
| F13 | POS (Petpooja) | ❌ no sync code | ⚠️ resource create crashes (B2) | — | Sync service/webhooks |
| F14 | Delivery partners | ❌ no code | ⚠️ resource create crashes | — | Partner API + status mapping |
| F15 | KDS / kitchen display | ❌ nothing (mockup only) | ❌ | — | KDS view from live orders |
| F16 | Admin dashboard | ✅ renders (brand color, widget) | — | — | Add KPIs from real data (currently empty shell) |
| F17 | Images/uploads | ⚠️ `image_url` string + meta emoji; no disk config | ⚠️ no FileUpload wired | ✅ emoji chips (corrupted) | Proper media pipeline + fix encoding |
| F18 | Ratings/reviews | ❌ fabricated in seeder + fallbacks | ❌ | ❌ shows fake ratings | Real reviews table/aggregate or remove |
| F19 | Notifications / FCM | ❌ `fcm_token` column only | — | ❌ | Push layer + queue |
| F20 | Multi-branch tenancy | ⚠️ branch FKs everywhere; **no scoping** in API/admin | ⚠️ no branch-scoped queries | ❌ | Scope per branch; admin selects branch |
| F21 | Admin auth | ✅ guard + login + tests | — | — | Password reset/rotation, 2FA optional |
| F22 | i18n / locale | ⚠️ `locale` column + admin select; no translation wiring | — | ❌ | Tag strings, locale-aware API |

### W-series detailed trace (updated)

### W1. Browse menu (customer)
| Step | Verdict | Evidence |
| --- | --- | --- |
| App shows menu | ✅ renders | Static `sampleProducts` in `thalaivaa_flutter/lib/providers/app_providers.dart` |
| Data from API | ❌ **Never** | No `http://`/`package:http` usage anywhere in `lib/` (grep = 0 hits); `http` in pubspec unused |
| Emoji rendering | ❌ corrupted | `iconEmoji: 'dY�z'` mojibake still in seeder `meta_json.emojis` and app constants (live API returns 2-byte emoji strings) |

### W2. Branch switching
- ⚠️ Backend returns 3 real branches (`CatalogController.php`). **App ignores them** — 3 hard-coded `Branch` objects in `app_providers.dart:9-27`. `branch.dart` duplicate model still shadows/shadowed by `models.dart`.

### W3. Coupon apply (app)
- ❌ App re-implements coupon logic locally (`CartNotifier.applyCoupon`) duplicating `CouponService` — two sources of truth; `POST /api/v1/coupons/validate` never called by the app.

### W4. Place order (app → API)
- ❌ `OrdersNotifier.placeOrder` synthesizes `THL-XXXX` locally, never calls `POST /api/v1/orders`; fake order `THL-9482` preloads state.
- ⚠️ API-side order creation now solid (transaction, validation, real prices, IDOR guard) — **live verified**. The bottleneck is 100% on the app side + server pricing integrity (B6).

### W5. Admin manage catalog
- ⚠️ All resource pages route-resolvable now, but Product/Category/ModifierGroup **Create crashes** (B2) and Category/ModifierGroup **blank columns** (B1).

### W6. Admin manage orders
- ⚠️ Orders list renders (Livewire + DB identical), but `total_amount_paise` phantom column shows blanks (B1); editing `status` doesn't write `order_status_logs` or broadcast (no transitions service).

### W7. Payments
- ❌ Mock rows only: `Payment::create(['razorpay_payment_id'=>'pay_'.Str::random(14)])`; `orders.payment_id` never linked; `payment_status=paid` client-bypass live-verified (B5). No gateway SDK/webhook.

### W8. Delivery / POS / KDS
- ❌ Tables and resources exist; no runtime flow, no webhooks, no status propagation, no KDS. Resource create crashes (B2).

### W9. Realtime (Livewire + Soketi)
- ❌ `broadcasting.default=log`; no events/channels/listeners; `/broadcasting/auth` absent; `LivewireSoketiReference.php` (claimed in `FILAMENT_DEVELOPER_REPORT.md`) **does not exist**.

### W10. RBAC
- ❌ Tables + resources + relations partially broken (B3); **zero roles/permissions seeded**; no policies; every admin full-access (B7).

### W11. OTP authentication
- ✅ Backend flow works live (hashed, expiry, token issuance). ❌ No SMS sender; throttle/attempts not enforced (B9). App has no login.

### W12. File uploads / images
- ⚠️ `image_url` text + meta_json emoji only; no storage disk publish, no FileUpload wiring; emoji corrupted. Left until backend truly hosts media.

---

## 7. End-to-End Data Flow Audit

| Data | Source | Path | Persisted? | Display correctness |
| --- | --- | --- | --- | --- |
| Branches | `branches` table (3 rows) | `GET /api/v1/branches` (200, live) → **Flutter: never fetched** | ✅ | ❌ app shows hard-coded copies |
| Products/prices | `products` (paise ints) + variants | `GET /api/v1/products` (200, live: 30 items + variants + modifier groups) | ✅ | ⚠️ app shows static doubles; API float serialization `price_inr` (¥100 rounding vs paise) |
| Ratings | seeder `meta_json` (4.9 / `rand(120,680)`) | API passthrough `rating`, `rating_count` (+ fallback `4.8`/`100`) | ✅ but fabricated | ❌ appears as real |
| Coupons | `coupons` + `CouponService` | `POST /api/v1/coupons/validate` (200/422 live) | ✅ (used_count increments only on order) | ⚠️ app re-derives locally |
| Order user | `OrderController` resolves Sanctum user or creates from `delivery_phone` | `POST /api/v1/orders` (201 live) | ✅ attributed | ⚠️ guest path weak (H1) |
| Payment status | **client `payment_status` param** (`pending|paid`) | → `orders.payment_status` + `payments.status='captured'` | persisted **lie** | ❌ "paid" without gateway |
| Modifier price | **client-supplied** `price_inr/price_adjustment` | → `order_items.unit_price/line_total` | persisted **lie** | ❌ ₹999.99 add-on live-verified |
| Delivery address | validated request (name/phone/address required) + default `Surat`/`395007` | → `orders.delivery_*` | ✅ | ⚠️ defaults still fabricated for city/postal |
| Delivery charge / tax | hard-coded constants (₹40/₹1000 threshold; 5%) | → `orders.delivery_charge/tax_amount` | ✅ computed | ⚠️ comment/code inconsistency (H7) |
| Order total | server math, transactional | → `orders.total_amount` (check `chk_total_computed` pgsql-only) | ✅ | ⚠️ no DB-level check on SQLite |
| Status timeline | `order_status_logs` | creation → `pending` log row (live) | ✅ creation only | ❌ no transition writes |
| Order history | `orders` + items | `GET /api/v1/orders` owner/paginated | ✅ | ⚠️ guest phone-listing weak (H1) |
| Authorization | `auth:sanctum` only on `/auth/me` + `/auth/logout`; orders/catalog public | — | — | ⚠️ orders readable unauthenticated (guest) (H1) |

**Bottom line:** the *backend* data path is now mostly honest (real catalog, transaction, logs, owner attribution for authenticated users) — but **money is still fiction** (`payment_status` + modifier prices from the client) and the *customer app* still does not consume a single byte of it.

---

## 8. Static / Mock / Fake Data Findings

| # | Location | What is fake | Real implementation should | How to verify |
| - | --- | --- | --- | --- |
| M1 | `thalaivaa_flutter/lib/providers/app_providers.dart` (entire file) | 30 products, 3 branches, cart, coupon logic, `OrdersNotifier` + fake order `THL-9482` — inline constants; **no network import** | Riverpod providers backed by an `http` API client + serializers | `flutter analyze`; run app with API down → must error, not render data |
| M2 | `thalaivaa_flutter/lib/providers/auth_provider.dart` | `StateProvider<bool>((ref) => false)` | Real OTP auth state machine | Attempt login flow |
| M3 | `thalaivaa_flutter/lib/providers/order_provider.dart` | `StateProvider((ref) => null)` | Order repository + polling | Place order and reload |
| M4 | `app/Services/OrderService.php:93-104` | **Modifier prices taken from client request** | Resolve modifier ids to DB prices | Send `price_inr:999.99` → must be ignored |
| M5 | `app/Services/OrderService.php:197-206` + `CreateOrderRequest` | **Payment is fictional** — random `pay_*` id; `payment_status=paid` fiat | Real Razorpay flow | Paid status only after gateway callback |
| M6 | `database/seeders/DatabaseSeeder.php` | `used_count` 12/4; `rating` 4.9; `rating_count = rand(120,680)`; `meta_json.emojis` mojibake | Neutral/real aggregates; fix UTF-8 | Inspect seeded rows; emoji bytes |
| M7 | `CatalogController.php:87-89` | `rating ?? 4.8`, `rating_count ?? 100` fallbacks served as data | Omit until real reviews exist | Empty meta → no fabricated rating |
| M8 | `app/Filament/` | No `LivewireSoketiReference.php` / `RBACPluginReference.php` exist, yet `FILAMENT_DEVELOPER_REPORT.md` claims them and a "24-table PostgreSQL" state | Docs must match reality or features implemented | `Test-Path` both files |
| M9 | `thalaivaa_flutter/lib/features/menu/menu_screen.dart:73` | Hard-coded category list | From `/api/categories` | Change server categories |
| M10 | `Thalaivaa_Glimpse_Preview.html`, `figma_mockups/*.html` | Design demos (explicit artifacts) | — | N/A |

---

## 9. API Audit

| Endpoint | Method | Auth | Notes / Findings |
| --- | --- | --- | --- |
| `/api/health` | GET | — | ✅ 200 (live) |
| `/api/v1/auth/otp/send` | POST | — | ✅ generates + **hashes**; ❌ no SMS; ❌ no throttle; `attempts` unused; `dev_otp` returned in local |
| `/api/v1/auth/otp/verify` | POST | — | ✅ issues Sanctum token, `firstOrCreate` user (live); dev bypass codes; ❌ no rate/attempt limit |
| `/api/v1/auth/me` | GET | ✅ sanctum | ✅ returns user + profile (live) |
| `/api/v1/auth/logout` | POST | ✅ sanctum | ✅ revokes token |
| `/api/v1/branches` | GET | — | ✅ 200, active+sorted (live) |
| `/api/v1/categories` | GET | — | ✅ with `products_count` of *available* products (live) — ❌ not branch-scoped |
| `/api/v1/products` | GET | — | ✅ 200; variants+modifier groups; ❌ **no `branch_id` filter**; ❌ `per_page` unclamped; ❌ fabricated ratings; ❌ float `price_inr` |
| `/api/v1/coupons/validate` | POST | — | ✅ server-side rule engine (live: ₹50/₹100 fixed, min-order, expiry, max-uses); ✅ `used_count` increments only at order time; ❌ no throttle |
| `/api/v1/orders` | POST | —* | ✅ transactional, validated (`CreateOrderRequest`), catalog-priced, status-log + payment row (live 201); 🔴 `payment_status=paid` fiat; 🔴 client modifier prices (B5/B6) |
| `/api/v1/orders` | GET | —* | ✅ owner-scoped when authenticated; ⚠️ unauthenticated `?phone=` lists all matching orders (PII, H1) |
| `/api/v1/orders/{id}` | GET | —* | ✅ 404 not found; ✅ **403 cross-user** when authenticated (live); 🔴 **unauthenticated guests get full PII** for guest orders (H1) |
| `/api/v1/auth/me`, `/auth/logout` | — | ✅ | only Sanctum-protected routes |

\* orders endpoints are publicly reachable; ownership checks apply only when a token is present.

**Cross-cutting API issues:** no rate limiting; no pagination meta beyond `total/current_page` (products has full meta); mixed integer/float money (`base_price_paise` int but `price_inr` float — keep paise everywhere); no structured error catalog; `APP_DEBUG` can still leak on 500s; unauthenticated read access to order PII.

---

## 10. Database Audit

### Verified current schema (SQLite, 25 business tables)
`admins, branches, users, categories, products, product_variants, modifier_groups, modifier_options, product_modifier_links, coupons, orders, payments, order_items, otp_codes, user_profiles, cart_items, order_status_logs, rbac_roles, rbac_permissions, rbac_role_permissions, admin_rbac_assignments, pos_integration_configs, delivery_partner_integrations, delivery_assignments, personal_access_tokens` (+ `migrations`, sqlite internals). `migrations`: 4 rows applied (fresh `migrate --force` verified).

### Findings
| # | Prio | Finding | Evidence |
| - | --- | --- | --- |
| D1 | 🔴 P0 | **Model/column drift** — the money/UI mismatches (B1): `total_amount`, `Razorpay`/`amount`, `valid_from/to`, `unit_price/line_total` vs resource field names | resources vs `…_171100.php`/`…_170000.php` |
| D2 | 🔴 P0 | **UUID-PK generation missing** on `RbacRole`, `RbacPermission`, `PosIntegrationConfig`, `DeliveryPartnerIntegration`, `DeliveryAssignment`, `AdminRbacAssignment` → create crashes (B2) | probe `NOT NULL constraint failed: …id` |
| D3 | 🔴 P0 | **Missing relations** on `RbacRolePermission` (`role`,`permission`), `AdminRbacAssignment` (`admin`,`role`,`branch`), `ModifierOption` (`modifierGroup` vs `group`) → admin list/create crashes (B3) | probe/property-null + source |
| D4 | 🟠 P1 | `orders.payment_id` declared nullable `foreignUuid` but **never set by OrderService** and **no FK constraint** → `$order->payment` always null | `OrderService.php`, migration `…_171100.php:31` |
| D5 | 🟠 P1 | No indexes on `orders.user_id/status/payment_status`, `order_items.order_id` (sqlite auto-indexes FKs only for the FK column itself, not composite lookups) | migrations |
| D6 | 🟠 P1 | Check constraints `chk_total_computed`/`chk_line_total` are **pgsql-only** and **absent on SQLite**; no app-level invariant | `…_171100.php:35-37,72-74` |
| D7 | 🟠 P1 | `cart_items.modifiers_json` vs model `modifier_ids_json` (and `CartItemResource` ignores it) | migration vs `CartItem.php` |
| D8 | 🟠 P1 | `pos_integration_configs` / `delivery_partner_integrations` columns (`api_key, store_id, config_json, webhook_secret`) vs model fillables (`api_key_hash, webhook_url`) mismatch | migrations vs models |
| D9 | 🟠 P1 | RBAC tables exist but **empty by design** — no seed roles/permissions; `admin_rbac_assignments` has no rows | probe counts (0) |
| D10 | 🟡 P2 | `Branch.php` fillable lacks `phone` → admin Branch phone silently dropped | model + resource |
| D11 | 🟡 P2 | `products.meta_json` continues to embed emoji/description/rating/rating_count (contender for a reviews table) | migration + seeder |
| D12 | 🟡 P2 | SQLite-only testing masks pgsql-only constructs; tests should run on the real engine | `phpunit.xml.dist` + DDL |

---

## 11. UI/UX Audit

### Admin panel (`/admin`)
- ✅ **Brand color now applied** — `Color::hex('#FF6B00')` (`AdminPanelProvider.php`).
- ✅ Panel themed; dashboard renders after login.
- ⚠️ **Data trust broken by schema mismatches**: Orders/Payments/Coupons/Categories/ModifierGroups/OrderItems show **blank money/badge columns** (B1); Product/Category/RBAC/POS/Delivery **Create buttons 500** (B2); ModifierOptions/RBAC assignment screens crash on data (B3).
- ⚠️ `OrderResource` exposes money/status as free-text edits (no read-only derived totals) — dangerous for bookkeeping.

### Customer app (Flutter prototype)
- Visual direction remains strong (brand palette, glassmorphism, gradients).
- **Corrupted emoji** still renders garbage on dish cards (M1/M6).
- **No loading/error/empty/success states** — screens are static snapshots.
- Coupon failure silently ignored; "free delivery > ₹1499" banner is a static string.
- Dead duplicate model `lib/models/branch.dart` still present.

### Scorecard (updated)

| Area | Score | Problems | Recommendation |
| --- | ---: | --- | --- |
| Visual Design | 6/10 | Admin on-brand now; app good but corrupted emoji | Fix UTF-8 seed/constants |
| UX | 3/10 | Admin data blanks/crashes; app all-static | Fix resource schema; wire app |
| Navigation | 7/10 | All 23 admin resources routable now; app bottom bar static | Keep; make pages functional |
| Responsiveness | 6/10 | Flutter LayoutBuilder; admin responsive by default | Test 360px |
| Accessibility | 4/10 | Color-only veg/non-veg marks; no reduced-motion | Add labels/semantics |
| Consistency | 4/10 | Admin theme fixed; but two coupon engines (app+API), fake ratings | Centralize domain rules |
| Forms | 3/10 | 8 resource create forms crash; phantom columns | Fix per B1/B2 |
| Tables | 4/10 | Blank columns on 6 resources (B1) | Align columns to schema |
| Loading States | 2/10 | None on either surface | Add |
| Error States | 2/10 | 500s on create; no app error paths | Fix crashes; friendly messages |
| Empty States | 2/10 | None | Add |
| **Overall SaaS Polish** | **4/10** | Vertical slice (order) nearly real server-side; client disconnected | Wire one end-to-end flow |

**Overall UI/UX score: 4.5/10**

---

## 12. Responsive & Accessibility Audit

- Admin: Filament default responsive; no custom breakpoints to break. `NOT VERIFIED` on physical mobile.
- App: `LayoutBuilder` + `SliverAppBar` wide/narrow paths OK; emoji corruption can break glyphs/overflow.
- A11y gaps unchanged: color-only Veg/Non-veg marks, no `Semantics` on emoji chips, no reduced-motion handling; Filament covers form/table a11y by default.

---

## 13. Security Audit (updated)

| # | Prio | Finding | Evidence |
| - | --- | --- | --- |
| S1 | 🔴 P0 | **Money/integrity by client input**: `payment_status=paid` (B5) and modifier `price_inr` (B6) flow into financial records — live-verified | `CreateOrderRequest.php:29`, `OrderService.php:93-104,171` |
| S2 | 🔴 P0 | **Guest order PII exposure**: unauthenticated `GET /orders/{id}` returns full delivery PII for phone-placed orders; `GET /orders?phone=` lists them (H1) | `OrderController.php:63-70,76-80` |
| S3 | 🔴 P0 | Secrets in working tree: real `APP_KEY` in `.env` (+ `APP_DEBUG=true`); value withheld here | `.env` |
| S4 | 🟠 P1 | No rate limiting on OTP/coupon/order endpoints (amplified by fake "OTP sent") | `routes/api.php` |
| S5 | 🟠 P1 | OTP attempts field unused; `123456`/`999999` bypass + `dev_otp` returned in local | `AuthController.php:89-93,39` |
| S6 | 🟡 P2 | No RBAC/policies — every admin superuser (B7) | `app/Policies` absent |
| S7 | 🟡 P2 | No webhook-signature design for any integration (none exist yet) | absence |
| S8 | 🟡 P2 | Admin money fields editable (`OrderResource`) with no read-only/audit wiring | resource source |
| S9 | 🟡 P2 | CORS/throttle/cookie-hardening untouched defaults | config (standard files, untouched) |
| S10 | 🔵 P3 | Phone/address stored plaintext (expected), but no masking in logs; `APP_DEBUG` leaks | schema/.env |
| S11 | 🔵 P3 | Sanctum tokens: no expiry configured (`expires_at` nullable), `last_used_at` not updated | migration/config defaults |

---

## 14. Performance Audit

- `GET /api/v1/products` still loads the full catalog + variants + modifier links + options and now **paginates only if asked**, `per_page` unclamped (H5). ~30 items today; will explode.
- Eloquent eager-loads are correct (`with([...])`) — good; but no caching anywhere (`Cache::remember`).
- No indexes on order lookups (D5).
- **Sequential work on DB**: order creation is transactional and light; fine at this scale.
- Order-number `Str::random(6)` (H8) — collision cost at scale.
- No queue workers used yet (`QUEUE_CONNECTION=database` set, zero jobs).
- Money kept in **integer paise** in DB (✅) but serialized as floats in API (`price_inr`, totals) — precision risk at scale.

---

## 15. AI/LLM Audit

No AI/LLM integration exists (no provider, prompts, or config). UI/UX report copy is marketing only. Score: N/A. If AI features are planned, gate with prompt-injection + cost controls.

---

## 16. Audio/Video/Real-Time Audit

- **Realtime: not implemented.** `broadcasting.default=log`; no `routes/channels.php`; no Event classes/Listeners; no `/broadcasting/auth`; Soketi env keys not mapped into `config/broadcasting.php` (default package config). `LivewireSoketiReference.php` **does not exist** despite `FILAMENT_DEVELOPER_REPORT.md` claiming it.
- **KDS/POS:** static mockups only (`figma_mockups/04_kds_kitchen_display.html`, `05_pos_cashier_terminal.html`).
- **Order status timeline:** creation log exists; **zero transition machinery** → the app stepper can never move.

---

## 17. Error Handling Audit

| Path | Behavior | Verdict |
| --- | --- | --- |
| Invalid coupon | 422 JSON | ✅ |
| Empty items / invalid product | **422** (request + service), DB rollback | ✅ (fixed) |
| Cross-user order fetch | 403 | ✅ |
| Missing order | 404 | ✅ |
| Invalid OTP | 422 | ✅ |
| Admin Create on Product/Category/RBAC/POS/Delivery | **500 (Integrity constraint)** | 🔴 B2 |
| Admin list on ModifierOption/RBAC-assignment | **500** when data present | 🔴 B3 |
| Admin blank columns (Orders/Payments/Coupons/…) | silent nulls | 🔴 B1 |
| DB down | debug page (APP_DEBUG) | 🔴 S3 |
| App failures | cannot occur (no networking) | — |

Security-fail-fast gap: all UI errors surface raw DB/Laravel errors to an authenticated operator (acceptable short-term, prohibited pre-release).

---

## 18. Testing Audit (updated)

| Aspect | Status |
| --- | --- |
| Framework | PHPUnit 11 + `phpunit.xml.dist` (sqlite `:memory:`, seeds on each test) |
| Unit tests | ✅ 1 (`CouponServiceTest`) |
| Feature (auth) | ✅ 2 (`AdminAuthenticationTest`) |
| Feature (coupons) | ✅ 3 (`CouponValidationTest`) |
| Feature (health/catalog) | ✅ 4 (`HealthAndCatalogTest`) |
| Feature (orders/privacy) | ✅ 3 (`OrderCreationAndPrivacyTest`) |
| **Total** | **13 passed / 344 assertions** (`php artisan test`, verified) |
| Admin resource render tests | ❌ none — allowed B1–B3 to regress |
| Flutter tests | ❌ none in `lib/`; no `test/` |
| Static analysis | none (pint present, no config; phpstan/larastan absent) |
| CI | ❌ none |

**The single biggest test-suite gap:** no rendering test (`livewire:test` / feature render of each admin page). Adding "GET each resource page returns 200 with seeded rows" would have caught every B1–B3 defect.

---

## 19. Code Quality & Architecture Audit

- ✅ Proper layering now: Controllers → `Services` → Models; `FormRequests` for validation; `{success,data}` envelope; controllers thin.
- ✅ `OrderService` is genuinely transactional and reads real catalog prices for products/variants; coupon discount computed server-side.
- ⚠️ New smells:
  - **Schema vs code drift** is the systemic issue (fields don't match columns/models/relations) — §4 B1–B3, §10 D1–D3.
  - Money logic partially client-mutable (B5/B6) — the single most dangerous architectural decision.
  - Hard-coded business rules (delivery charge, tax, "free delivery" threshold vs comment) in service code (H7).
  - Duplicate domain logic (coupon engine in app + API; branch list in app + DB).
  - `AdminRbacAssignment` (pivot model) makes `$incrementing=false` + `primaryKey=null` + `$timestamps=false` while the migration **does** have UUID `id` + timestamps — model/schema mismatch (D3).
  - Dead claim-docs: `FILAMENT_DEVELOPER_REPORT.md` describes `LivewireSoketiReference.php`, `RBACPluginReference.php`, "24 tables PostgreSQL" — files absent, engine actually SQLite (M8).
  - Flutter mono-stub providers (M1–M3).
- ✅ Filament resources are consistent in shape (all use `Manage*` single-page pattern) — easy to fix columns wholesale.

---

## 20. Dependencies & Configuration

| Item | Status |
| --- | --- |
| `composer.json` | Laravel ^11, Filament ^3.2, Sanctum ^4, pusher ^7.2, livewire ^3.5 — reasonable |
| Test deps | phpunit ^11, faker, mockery, collision, pint — all present |
| Unused deps | `pusher/pusher-php-server` (no runtime use); `laravel/sail` (no sail config/docker); `http` in Flutter (zero usage) |
| Missing deps | **Razorpay SDK** (payments claimed), AWS SDK (S3 env), a static analyzer, an observability/error tracker |
| `config/` | Standard Laravel 11 set present (verified via probe: 21 keys incl. `filament`, `sanctum`, `broadcasting`, `database`); no `config/services.php` razorpay block; `broadcasting.default=log` |
| `.env` vs `.env.example` | `.env`: **sqlite**, `APP_DEBUG=true`, real `APP_KEY`; example: **pgsql** — drift + secret hygiene risk |
| Lock file | `composer.lock` present; PHP 8.5.10 satisfies |
| CS | `pint` installed, no config, not enforced |

---

## 21. Git / Repository Hygiene

- ❌ **Still not a Git repository** (`git status` → fatal: not a git repository).
- ✅ **`.gitignore` now present and solid** (covers `/vendor`, `.env*`, `database/*.sqlite`, `storage/*.key`, caches, IDE dirs, build).
- ⚠️ The real dev DB now contains **live dev data** (snapshot at audit time: `orders=5, order_items=5, payments=5, users=5, branches=3, coupons=2, otp_codes=8, rbac_roles=0`) — fine for a dev DB, but **do not commit it** (now ignored).
- `.phpunit.result.cache` now exists (ignored) and `report.md` sits in the workdir (fine to commit or not).
- Next: `git init`, first commit **without** `.env`/`*.sqlite`/`vendor`, then CI.

---

## 22. What Is Already Good (verified)

1. Admin auth: dedicated guard, `FilamentUser`, meaningful `canAccessPanel` — small and correct (tests green).
2. 23/23 resources routable with Pages folders — navigation is whole again.
3. Full 25-table schema migrated cleanly; confirmed on fresh SQLite.
4. `OrderService`: transaction boundary, cold catalog pricing, coupon integration, status-log + payment rows, no orphans (regression prevented by tests).
5. OTP auth: hashed, expiring, token-backed, live-verified end-to-end.
6. Test suite exists and is green (13/344); validates the IDOR fix.
7. HTTP API envelope + ISO-8601 timestamps + `v1` prefixing + backward-compatible aliases.
8. Integer-paise money in schema; snapshot columns on order items; check-constraint intent for pgsql.
9. Brand theme applied to Filament (`#FF6B00`).
10. `.gitignore` added; composer deps pinned; `phpunit.xml.dist` sane.

---

## 23. Top 10–20 Recommendations

| # | Prio | Problem | Recommendation | Related |
| - | --- | --- | --- | --- |
| 1 | P0 | Admin schema/column drift | Align every resource field to real columns/relations; delete or add missing columns. Green target: each resource renders + saves | B1 |
| 2 | P0 | Admin Create crashes | Add `branch_id` selects (catalog), `HasUuids` to RBAC/POS/Delivery models | B2 |
| 3 | P0 | Admin list crashes | Define missing model relations (`role`/`permission`/`admin`/`branch`/`modifierGroup`) | B3 |
| 4 | P0 | Payments fake | Real Razorpay order/callback/capture; link `orders.payment_id`; remove client `payment_status` | B4/B5 |
| 5 | P0 | Modifier price client-injected | Resolve modifier ids server-side from `modifier_options` | B6 |
| 6 | P0 | RBAC inert | Seed roles/permissions, add policies, gate `canAccessPanel` | B7 |
| 7 | P0 | App disconnected | Real `http` repository + serializers; drop fake orders; fix emoji | B8/M1-M3 |
| 8 | P1 | Guest PII exposure | Require auth for order reads; mask guest responses or generate short-lived access keys | H1 |
| 9 | P1 | Admin ∂-sheet ledger honesty | Render totals read-only computed values in OrderResource | H10 |
| 10 | P1 | Auth hardening | SMS provider, throttle OTP, enforce attempts, remove dev bypass | B9 |
| 11 | P1 | Perf | Index order columns; clamp `per_page`; cache catalog; iterative paise-only serialization | H5/D5 |
| 12 | P1 | Business rules | Externalize delivery/tax/coupon min-order config; fix comment/code mismatch | H7 |
| 13 | P1 | Branch isolation | `branch_id` path/filter on catalog + scope admin queries | H6/F20 |
| 14 | P2 | Add resource render tests | Get every admin page 200 with seeded data + Livewire create flow | H13 |
| 15 | P2 | CI/CD + git init | GitHub Actions (pint, test, migrate:fresh), Dockerfile, deploy env | §21 |
| 16 | P2 | Realtime or stop claiming | Implement `OrderBroadcast` + channels or remove from docs | H9/W9 |
| 17 | P2 | Product hygiene | One coupon engine (API on both), review table, remove fabricated ratings | M4-M7 |
| 18 | P3 | Observability + hardening | JSON logs, error tracker, rotate APP_KEY, debug off, cookie/CORS/throttle defaults | S3/S8/S9 |

---

## 24. Quick Wins

1. **`HasUuids` on 6 models** (RbacRole, RbacPermission, PosIntegrationConfig, DeliveryPartnerIntegration, DeliveryAssignment, AdminRbacAssignment) → unblocks every RBAC/POS/Delivery create. 20 min.
2. **Rename phantom columns in 6 resources** to real schema names (`total_amount`, `amount`+`razorpay_payment_id`+`status`, `valid_to`, `unit_price`/`line_total`) — fixes blank tables/forms. 1–2 h.
3. **Add `modifierGroup()`, `role()`, `permission()`, `admin()`, `branch()` relations** to the 3 models. 30 min.
4. **`Select::make('branch_id')`** (required) on Product/Category/ModifierGroup forms. 20 min.
5. **Remove `payment_status` from `CreateOrderRequest`** and default `pending` in `OrderService`; gun 10-min but kills the "paid-by-fiat" hole.
6. **Server-side modifier pricing**: replace client price with `ModifierOption::find($m['id'])->price_adjustment`. 30 min.
7. **`Route::middleware('throttle:10,1')`** on `auth/otp/send` + `coupons/validate` + `orders`. 10 min.
8. **Index** `orders(user_id, status)`. 5 min.
9. **Seed RBAC roles/permissions + assign admin**; add policy stubs. 1–2 h.
10. **Flutter: replace `OrdersNotifier`/catalog with one `ApiClient` + serializer** — smallest honest step toward the real product. 0.5–1 day.
11. **Fix UTF-8 emojis** in seeder + app constants. 30 min.
12. **Resource render test** (`$this->get('/admin/...')` or Livewire button) after each fix to lock it in. 1 h.

---

## 25. Implementation Roadmap (revised after re-scan)

### Phase 0 — Make the admin and money path honest
| Task | Prio | Complexity | Outcome | Verify |
| --- | --- | --- | --- | --- |
| Column/relation alignment across 8 resources (B1/B3) | P0 | M | No blank columns/crashes | Render + create/edit each resource |
| UUID-PK + fillable fix on RBAC/POS/Delivery models (B2) | P0 | S | All Create buttons save | Create row on each |
| Remove client `payment_status` + server-side modifier pricing (B5/B6) | P0 | S | Money sealed to server | Negative/hostile payload tests |
| Link `orders.payment_id` when payment row is created | P0 | S | Order↔payment truthful | `$order->payment` resolves |
| Seed roles/permissions + policies + `canAccessPanel` RBAC | P0 | M | Scoped access | Role A vs B menus |
| Resource render tests for all 23 pages | P0 | M | Regressions blocked | `php artisan test` green |

### Phase 1 — Real payments + customer app wiring
| Task | Prio | Complexity | Outcome | Verify |
| --- | --- | --- | --- | --- |
| Razorpay SDK order → client redirect → callback (signature) → capture | P1 | XL | Real money | Webhook sim |
| Refund + failed-status handling + admin payment actions | P1 | M | Operations | Refund journal |
| Flutter API client (http) + serializers + replace mock providers | P1 | L | App shows real data | App with API down → error states |
| App OTP login + jwt/token store | P1 | L | Real authentication UX | Login flow E2E |
| Order transitions service + `order_status_logs` on every change | P1 | M | Audit trail complete | Transition writes log |
| Guest-order PII fix (mask or require auth) | P1 | S | Privacy | Unauthenticated fetch evals |

### Phase 2 — Branch tenancy, reliability, realtime
| Task | Prio | Complexity | Outcome | Verify |
| --- | --- | --- | --- | --- |
| `branch_id` scoping in API + admin; per-branch seeding | P2 | M | True multi-branch | Branch A/B isolation test |
| Order events + broadcasting (Soketi) + KDS view | P2 | L | Live tracking | Two browsers update |
| Indexes, per_page clamp, catalog cache | P2 | S | Baseline perf | Load test |
| Business-rule config (delivery/tax) | P2 | S | Adjustable policy | Change price live |

### Phase 3 — Security & ops hardening
| Task | Prio | Complexity | Outcome | Verify |
| --- | --- | --- | --- | --- |
| `APP_DEBUG=false`, rotate/regenerate `APP_KEY`, .env.production | P3 | S | No leaks | /api with error → JSON only |
| Rate limits, OTP attempts, cookie/CORS hardening | P3 | S | Abuse-resistant | Hammer test |
| PostgreSQL dev parity (run migrate:fresh on pgsql, check constraints) | P3 | M | Prod-schema truth | CI pgsql job |
| CI pipeline (pint → test → migrate:fresh both engines) | P3 | M | Guardrails | PR gates |
| Observability (JSON logs, Sentry, audit log) | P3 | M | Diagnosability | Incident drill |

### Phase 4 — SaaS polish
| Task | Prio | Complexity | Outcome | Verify |
| --- | --- | --- | --- | --- |
| Reviews/ratings real aggregate; remove fabricated fallbacks | P4 | M | Honest UX | Seed empty → no fake stars |
| Notifications/FCM + queue workers | P4 | L | Push engagement | Device push test |
| i18n wiring (en/hi/gu) | P4 | M | Locale-ready | Switch locale |
| Corporate dashboard KPIs from real data | P4 | M | Value | Dashboard vs DB |

---

## 26. Manual QA Test Plan (re-audit)

### T0 — Admin smoke
1. Fresh disposable DB → `migrate --force` + `db:seed --force`; `php artisan serve`.
2. Login `admin@thalaivaa.com` / `Admin@Thalaivaa2026`.
3. Expected: dashboard 200; sidebar lists 23 sections.
4. **Known failures to confirm-fixed:** Orders (blank `total_amount`), Payments (blank fields), Coupons (blank expiry), Categories/ModifierGroups (create 500), ModifierOptions (list 500), Products (create 500), RBAC Roles/Permissions/POS/Delivery (create 500), Branch (phone not saved).

### T1 — Catalog & OTP
- `/api/v1/branches|categories|products` 200 (live ✅).
- OTP send → verify (use `dev_otp` in local) → token → `/auth/me` → logout. Live ✅.

### T2 — Order lifecycle
- Authenticated order with real product + variant + modifiers; verify totals = catalog math.
- Negative: empty items 422; bogus product 422; duplicate request idempotency (not yet implemented); `customer-supplied modifier price must be ignored` (currently FAILS — B6).
- `payment_status` forced to `pending` regardless of input (currently FAILS — B5).

### T3 — Privacy
- User B fetches User A's order → 403 (✅ live).
- Unauthenticated fetch of a guest order → should be masked/denied (currently full PII — H1).

### T4 — Admin CRUD matrix
- For every one of the 23 resources: List (200, correct values) → Create → Edit → Delete. Current passes only for Admin/User/Branch-list/Order-Status-Log/POS-list/Delivery-list/RBAC-list/OTP/UserProfile/etc.; ~8 fail at create (B2), 3 list-crash (B3), 6 blank-column (B1).

### T5 — Flutter offline vs online
- Kill API → app must show errors/empty (currently still renders static data — B8).

### T6 — Coupon matrix
- THALAIVAA50 @ 300 → ₹50 (✅ tested); below min → 422; expired → 422; percent coupon → percent math; used_count increments once per redeemed order.

---

## 27. Automated Test Plan (revised)

### Unit
- `CouponService` fixed/percent/min/expiry/max-uses (✅ exists) + `OrderService` pricing purity: **modifier prices from DB, never from request**; discounts math; delivery/tax policy.
- Model invariants: `orders.payment_id` set when payment created; UUID ids present on RBAC/POS/Delivery creates.

### Feature / API
- Auth: OTP flow, token issuance/expiry, `me`, logout (add: throttle 429 on send).
- Orders: auth required; guest flow PII-masking; IDOR (✅ exists); **no `paid` fiat**; transactionality on failure (✅ exists); idempotency.
- Coupons: matrix (✅ exists).

### Admin rendering (missing — highest value)
- Livewire/feature test that **every resource page renders 200 with seeded rows** and that Create/Edit saves+persists (would have caught B1–B3).

### Flutter
- Unit tests for serializers; widget tests for loading/error/empty states; golden menu with valid UTF-8.

### Security
- Rate-limit hammer on OTP/coupon; per_page clamp; debug-off error shape; secrets scan (no `.env` in artifacts).

### Performance/DB
- pgsql `migrate:fresh` CI job (check constraints) + SQLite parity test; index effectiveness.

---

## 28. Final Verdict

### 🔴 MUST FIX BEFORE PRODUCTION
1. Admin create/list crashes (B1–B3) — 8 create-crash + 3 list-crash + 6 blank-column resources.
2. Payment realism — no client `payment_status`; real gateway; link `orders.payment_id` (B4/B5).
3. Server-only pricing (B6).
4. RBAC enforcement (B7) or declare "single-admin MVP" honestly.
5. Guest PII exposure (H1).
6. Secrets hygiene: `APP_DEBUG=false`, rotate `APP_KEY`, never commit `.env`.

### 🟠 SHOULD FIX BEFORE RELEASE
7. OTP real SMS + throttle/attempts (B9).
8. Flutter app actually talks to the API (B8) — otherwise the product is a mock.
9. Perf: indexes, per_page clamp, cache; paise-only serialization.
10. Branch scoping + per-branch seeding.
11. Order-number collision retry; idempotency keys.
12. Realtime decision: implement or remove claim.
13. CI + git init + deployment definition.

### 🟢 SAFE / GOOD TO GO
- Admin auth design, 23-resource routing, 25-table migration, transactional order service, OTP backend flow, coupon service, 13 green tests, brand theme, `.gitignore`.

---

*This report is a snapshot dated 2026-09-12. All runtime evidence was produced on disposable SQLite databases; the developer's real DB was only read (current row counts: orders=5, payments=5, users=5, otp_codes=8, rbac_roles=0). No source code in either repository was modified.*