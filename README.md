# thalaiva-flutter-app

Authentic South Indian Cuisine Food-Tech Platform & Flutter Web App.

## Features
- **Flutter Web App:** Full food ordering experience, user authentication, customer profile management, and live order tracking.
- **Backend API:** Laravel RESTful backend with transactional order management, IDOR protection, coupon validation, and administrative controls.
- **Simulator Interface:** Built-in mobile device simulator for testing desktop & web preview seamlessly.

## Getting Started

### Backend Setup
```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan migrate --seed
php artisan serve
```

### Accessing Simulator & Flutter Web
- Simulator: `http://localhost:8000/simulator`
- Flutter Web App: `http://localhost:8000/flutter_web`
