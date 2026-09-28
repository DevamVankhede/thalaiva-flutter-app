# 🎬 PHASE 5 — PLAYWRIGHT END-TO-END (E2E) TESTING REPORT

**Date:** 2026-09-24  
**Driver:** Playwright Chromium Engine (Automated via Playwright MCP)  
**Execution Video:** [`qa-reports/evidence/videos/e2e_user_journey.webm`](file:///c:/Users/Admin/thalaivaa_api/qa-reports/evidence/videos/e2e_user_journey.webm)  

---

## 1. Executed E2E User Journeys

1. **Journey 1 — Customer Menu Discovery to Cart Checkout:**
   - Launch application at `/simulator`.
   - Filter menu by "🥣 Idlis & Vadas".
   - Search for "Kaapi" and clear search.
   - Add items to cart with live price aggregation.
   - Open Cart screen (`text="Cart"`).
   - Verify 5% GST computation and subtotal.

2. **Journey 2 — Live Milestone Tracking & Privacy Guard:**
   - Navigate to Track screen (`text="Track"`).
   - Inspect dynamic radar graphic and milestone timeline.
   - Verify driver card details (Ramesh Patel, TVS Jupiter EV, Call/Chat CTA buttons).

3. **Journey 3 — Administrator Authentication Lifecycle:**
   - Navigate to `/admin/login`.
   - Submit invalid credentials (`invalid_admin@thalaivaa.com` / `wrongpassword123`).
   - Verify failure state and rejection.

---

## 2. Screenshot Evidence Index

- `01_simulator_home.png` : Initial mobile viewport rendering
- `02_category_filter_idli.png` : Category filtered state
- `03_search_kaapi_results.png` : Instant search match
- `04_cart_screen.png` : Cart bill calculation with GST
- `05_live_order_tracking.png` : Live radar and milestone timeline
- `06_profile_screen.png` : Customer profile and loyalty balance
- `07_admin_login_screen.png` : Filament admin sign-in portal
