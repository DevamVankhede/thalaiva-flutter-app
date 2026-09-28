# 🕵️ PHASE 4 — MANUAL & EXPLORATORY TESTING REPORT

**Date:** 2026-09-24  
**Technique:** Socratic QA Exploratory Testing via Playwright MCP Browser Interaction  

---

## Exploratory Test Scenarios & Results

1. **Rapid Category Switching:**
   - Clicked Dosas -> Idlis -> Kaapi -> All in rapid succession (< 200ms between clicks).
   - Result: List transitions smoothly without UI freezing or stale state.

2. **Negative Boundary Input on Cart Steppers:**
   - Repeatedly clicked decrement (-) on cart item when quantity was 1.
   - Result: Item cleanly drops from cart without negative integer overflow.

3. **Promo Code Case Insensitivity & Threshold Boundary:**
   - Attempted promo `thalaivaa50` (lowercase) on cart with ₹180 subtotal.
   - Result: System gracefully rejected discount because subtotal is below ₹200 threshold.

4. **Multi-device Viewport Resizing:**
   - Switched between iPhone 16 Pro, Google Pixel 9, and Galaxy S24 frames in simulator header.
   - Result: CSS container responsive layout re-adapts seamlessly.

5. **Direct Route Invalidation:**
   - Navigated directly to `/invalid-route-404`.
   - Result: Handled cleanly by Laravel HTTP exception pipeline.
