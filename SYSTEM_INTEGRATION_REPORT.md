# Thalaivaa Food-Tech Platform — System Integration Report

**Version**: 2.0.0 Enterprise  
**Architecture**: Decoupled SaaS (Flutter Web Frontend + Laravel 11 REST API + PostgreSQL / SQLite DB)  
**Deployment Profile**: Containerized (Docker & Docker Compose)  

---

## 1. System Architecture Overview

```
+-------------------------------------------------------------------------+
|                        Client Layer (Flutter Web)                       |
|  - Riverpod State (Cart, Orders, Theme, i18n, Filters)                  |
|  - Micro-Animations, Glassmorphism, Pure Veg Indicators, Deals Carousel|
|  - Live Tracking 4-Stage Timeline & Profile Manager                     |
+------------------------------------+------------------------------------+
                                     | HTTP REST (JSON)
                                     v
+-------------------------------------------------------------------------+
|                        Backend Layer (Laravel 11 API)                   |
|  - Authentication & RBAC (Sanctum Tokens, Roles & Permissions)          |
|  - Sealed Server-Side Pricing (OrderService & Modifier Resolution)      |
|  - Multi-Branch Catalog & Inventory Engine (Surat Hubs)                 |
|  - Filament v3 Back-Office Administration Dashboard                     |
+------------------------------------+------------------------------------+
                                     | SQL / Eloquent ORM
                                     v
+-------------------------------------------------------------------------+
|                        Persistence Layer                                |
|  - PostgreSQL 16 (Production) / SQLite3 (Local Development)             |
+-------------------------------------------------------------------------+
```

---

## 2. API Contract Endpoints & Specifications

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `GET` | `/api/v1/branches` | Fetch Surat branches with coordinates & delivery times | No | `200 OK` |
| `GET` | `/api/v1/categories` | Fetch active catalog category hierarchy | No | `200 OK` |
| `GET` | `/api/v1/products` | Fetch 30 varieties of dishes with modifier groups | No | `200 OK` |
| `POST` | `/api/v1/coupons/validate` | Verify coupon validity against cart total | No | `200 OK` |
| `POST` | `/api/v1/orders` | Create verified order with server-sealed pricing | Optional / Bearer | `201 Created` |
| `GET` | `/api/v1/orders/{id}` | Real-time order status and stage tracker | Bearer | `200 OK` |

---

## 3. Security & Anti-Tampering Controls

1. **Server-Sealed Pricing**:
   - Client sends only `product_id`, `quantity`, and `modifier_option_ids`.
   - `OrderService` queries database base prices and modifier costs directly, preventing client-side price tampering.
2. **Payment Lifecycle Enforcement**:
   - Order creation strictly defaults `payment_status` to `'pending'`, linked within an atomic DB transaction.
3. **IDOR Protection**:
   - All models utilize RFC 4122 Version 4 UUID primary keys (`HasUuids` trait), eliminating sequential ID enumeration attacks.
4. **CORS & CSRF Headers**:
   - API middleware permits preflight checks with strict content negotiation (`application/json`).

---

## 4. Environment & Port Allocation

- **Frontend Web UI**: `http://localhost:8085` (served via Nginx / high-speed static web server)
- **Backend API**: `http://127.0.0.1:8000`
- **Database**: PostgreSQL on `5432` / SQLite on local filesystem
