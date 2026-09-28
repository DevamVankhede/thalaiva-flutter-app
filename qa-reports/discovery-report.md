# 🔍 PHASE 0 — PROJECT DISCOVERY REPORT

**Date:** 2026-09-24  
**Auditor:** Principal QA Automation Engineer & Release Specialist  
**Application Target:** Thalaivaa Multi-Surface Restaurant SaaS  

---

## 1. Architecture & Stack Overview

- **Backend Framework:** Laravel 11.56.1 (PHP 8.5.10 CLI x64)
- **Database:** SQLite 3 WAL Mode (`database/database.sqlite`)
- **Admin Dashboard Engine:** Filament 3.2 + Livewire 3
- **Mobile Frontend Engine:** Flutter 3.47.4 (Dart 3.13.3) compiled to CanvasKit/WebAssembly
- **Interactive Simulator Viewport:** HTML5 / Vanilla JS SPA (`public/simulator.html`)
- **API Authentication:** Laravel Sanctum Token & Session Auth
- **Test Frameworks:**
  - Backend: PHPUnit 11.5.46
  - Frontend: Flutter Test Runner (with LCOV coverage collection)
  - Browser Automation / E2E: Playwright MCP (Chromium / Chrome Engine)

---

## 2. Discovered Routes & Endpoints (59 Registered Routes)

### 2.1 Core Customer API Endpoints
- `GET /api/v1/products` : 30 authentic South Indian catalog dishes
- `GET /api/v1/categories` : Category taxonomy with dish aggregations
- `GET /api/v1/branches` : Surat branches (City Light, Vesu, Adajan)
- `POST /api/v1/coupons/validate` : Promo validation (`THALAIVAA50`)
- `POST /api/v1/orders` : Transactional order placement with price calculation
- `GET /api/v1/orders/{id}` : Live order tracking & driver details
- `POST /api/v1/auth/otp/send` & `/verify` : Customer phone authentication
- `GET /api/health` & `/health` : System health diagnostics

### 2.2 Admin Panel & Management Routes
- `GET /admin/login` & `POST /admin/logout` : Filament Auth
- `GET /admin/orders` : Real-time KDS & order status manager
- `GET /admin/products` & `/admin/modifier-groups` : Menu manager
- `GET /admin/branches` : Outlet management

### 2.3 Interactive Web Frontends
- `GET /simulator` : Mobile phone frame viewport & interactive simulator
- `GET /preview` : Multi-surface multi-device studio
- `GET /flutter_web/index.html` : Production Flutter CanvasKit Web build
