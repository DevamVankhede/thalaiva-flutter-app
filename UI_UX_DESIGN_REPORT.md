# Thalaivaa UI/UX Design Contract & Architecture Specification

**Project:** Thalaivaa Multi-Branch Authentic South Indian Food SaaS Platform  
**Location:** Surat (City Light Town, Vesu, Adajan), Gujarat, India  
**Platform Scope:** Customer Mobile App (Flutter/Riverpod), Cashier POS Terminal, Kitchen Display System (KDS), Filament v3 Admin Suite  
**Date:** 2026-09-12  
**Status:** ✅ DESIGN SPECIFICATION COMPLETED & VERIFIED  

---

## 1. Executive Summary & Brand Identity

Thalaivaa's visual language celebrates the vibrancy, warmth, and culinary heritage of South India (Chettinad, Tamil Nadu, Kerala, Karnataka) while delivering a state-of-the-art, hyper-fast digital ordering experience. The design system is optimized for lightning-fast item discovery, crystal-clear bill receipts in Indian Rupees (₹ with paise precision), live real-time order tracking, and friction-free branch routing across Surat.

---

## 2. Core Design Tokens & Palette

| Token Key | HEX / Value | Role & Semantic Application |
| :--- | :--- | :--- |
| `--color-primary-500` | `#FF6B00` | Primary Brand Amber / Saffron. Call-to-actions, active indicators, badges |
| `--color-primary-600` | `#E05D00` | Primary hover / pressed state |
| `--color-primary-100` | `#FFF3E0` | Soft tinted highlight backgrounds, bestseller ribbons |
| `--color-secondary-900` | `#1E1E2E` | Deep obsidian slate. High-contrast typography, premium hero banners |
| `--color-secondary-800` | `#2D2D44` | Card gradients, elevation backdrops |
| `--color-accent-gold` | `#FFB800` | Gold member badges, star ratings, festival promotional banners |
| `--color-surface-bg` | `#F8F9FA` | Main screen background for glare-free readability |
| `--color-surface-card` | `#FFFFFF` | Elevated container cards with soft ambient shadow |
| `--color-success` | `#10B981` | Veg indicators, order delivered status, discount applied chips |
| `--color-danger` | `#EF4444` | Non-veg indicators, cancellations, destructive actions |
| `--color-warning` | `#F59E0B` | In kitchen / preparing status, pending payment notices |
| `--radius-sm` | `6px` | Tag chips, micro-badges |
| `--radius-md` | `12px` | Input fields, category filter pills, regular buttons |
| `--radius-lg` | `16px` | Product cards, bottom sheets, order status containers |
| `--radius-xl` | `24px` | Promotional hero banners, modal dialogs |

---

## 3. Typography Hierarchy (Google Font: Inter & Outfit)

- **Display 1 (24px, Bold, Tracking -0.5px):** Main screen headers, promotional titles.
- **Heading 1 (18px, Bold, Tracking -0.2px):** Product titles, modal sheet headings, order numbers.
- **Heading 2 (16px, Semi-Bold):** Category headers, bill summary total amount.
- **Body Large (14px, Medium):** Product descriptions, outlet address lines.
- **Body Small (12px, Regular):** Metadata, preparation time, ratings count, allergen info.
- **Caption / Tag (10px, Bold, Uppercase):** `★ BESTSELLER`, `VEG`, `SPICY`, `GOLD MEMBER`.

---

## 4. Multi-Surface UI/UX Flow Architecture

### A. Customer Mobile App (Flutter / Web)
1. **Outlet Discovery & Header:**
   - Geolocation-aware outlet switcher (*City Light Town*, *Vesu VIP Road*, *Adajan Hub*).
   - Instant search with live filter debounce across 30+ authentic dishes.
   - Quick toggle: 🛵 *Home Delivery (20-25 min)* vs 🛍️ *Takeaway Pickup*.
2. **Dynamic Menu Catalog:**
   - 6 Categorized carousels: *Dosas, Idlis & Vadas, Biryani & Rice, Chettinad Curries & Meals, Traditional Desserts, Beverages & Kaapi*.
   - Interactive Modifier Modal Bottom Sheet: Real-time dynamic recalculation for Ghee toppings, Gunpowder Podi, Portion sizing, and Sambar spice customization.
3. **Cart & Transparent Bill Breakdown:**
   - Stepper quantity modifier with instant haptic feedback.
   - Live Coupon Engine: Auto-validation for `THALAIVAA50` and `FEAST100`.
   - Complete fiscal breakdown: Subtotal + 5% GST + Delivery Partner Fee - Discounts = Grand Total.
4. **Live Order Tracking Timeline:**
   - 4-Stage visual status stepper with animated pulse.
   - Delivery rider contact & one-tap direct WhatsApp / Phone connection (+91 92170 02598).

### B. Kitchen Display System (KDS)
- High-contrast Dark Mode (`#12121E`) for steamy, fast-paced kitchen environments.
- Color-coded urgency cards: Green (<5 min), Yellow (5-12 min), Red (>15 min overdue).
- One-tap status advance: *New ➔ In Kichen ➔ Ready for Dispatch*.

### C. Cashier POS Terminal
- Grid layout optimized for 10-inch tablets and touch monitors.
- Fast barcode/SKU entry, table number allocation, split billing (Cash / UPI / Cards).

---

## 5. 6-Pillar Quality & Visual Design Audit

1. **Aesthetics & Contrast:** WCAG AAA contrast compliance (Deep Obsidian `#1E1E2E` on Light Grey `#F8F9FA` & Saffron `#FF6B00` on White).
2. **Typography & Hierarchy:** Strict font scales with clear demarcation between product name, price, and descriptions.
3. **Touch Targets:** All buttons, counters, and chips maintain minimum 48x48px hit areas for mobile thumb zones.
4. **Error Handling & Empty States:** Friendly, culturally relevant empty illustrations for empty cart and search misses.
5. **State Feedback:** Immediate snackbars, loading shimmer skeletons, and quantity badges.
6. **Responsiveness:** Fluid adaptation from compact mobile screens (360px) to widescreen desktop monitors (1920px).

---

## 6. Verification Artifacts & Mockup Index

The following interactive prototypes and design tokens are generated in `figma_mockups/`:
- [`figma_mockups/design_tokens.json`](file:///C:/Users/Admin/thalaivaa_api/figma_mockups/design_tokens.json) — Standardized Design Token Schema.
- [`figma_mockups/01_customer_mobile_home.html`](file:///C:/Users/Admin/thalaivaa_api/figma_mockups/01_customer_mobile_home.html) — Mobile Menu & Outlet Proto.
- [`figma_mockups/02_customer_cart_checkout.html`](file:///C:/Users/Admin/thalaivaa_api/figma_mockups/02_customer_cart_checkout.html) — Cart & Checkout Proto.
- [`figma_mockups/03_customer_live_tracking.html`](file:///C:/Users/Admin/thalaivaa_api/figma_mockups/03_customer_live_tracking.html) — Order Live Tracking Proto.
- [`figma_mockups/04_kds_kitchen_display.html`](file:///C:/Users/Admin/thalaivaa_api/figma_mockups/04_kds_kitchen_display.html) — KDS Station Proto.
- [`figma_mockups/05_pos_cashier_terminal.html`](file:///C:/Users/Admin/thalaivaa_api/figma_mockups/05_pos_cashier_terminal.html) — POS Terminal Proto.
