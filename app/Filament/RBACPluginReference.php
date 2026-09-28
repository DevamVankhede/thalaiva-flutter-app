<?php
// RBAC Plugin Reference — Custom 4-table RBAC (no spatie/laravel-permission installed)
// Tables: rbac_roles, rbac_permissions, rbac_role_permissions (junction), admin_rbac_assignments
// Admin links to role via admin_rbac_assignments (admin_id + role_id PK, ON DELETE CASCADE)
// Role links to permissions via rbac_role_permissions (role_id + permission_id PK, ON DELETE CASCADE)
// Permissions enforced at Filament resource/query level.
// Note: spatie/laravel-permission package NOT present in vendor/; custom RBAC implemented.
