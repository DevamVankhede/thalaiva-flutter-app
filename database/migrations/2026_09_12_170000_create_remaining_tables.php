<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        // 1. OTP Codes
        if (!Schema::hasTable('otp_codes')) {
            Schema::create('otp_codes', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->string('phone')->index();
                $table->string('code_hash');
                $table->timestamp('expires_at');
                $table->timestamp('verified_at')->nullable();
                $table->integer('attempts')->default(0);
                $table->timestamps();
            });
        }

        // 2. User Profiles
        if (!Schema::hasTable('user_profiles')) {
            Schema::create('user_profiles', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->foreignUuid('user_id')->constrained('users')->cascadeOnDelete();
                $table->string('dietary_preference')->nullable();
                $table->text('default_delivery_address')->nullable();
                $table->date('birthday')->nullable();
                $table->date('anniversary')->nullable();
                $table->timestamps();
            });
        }

        // 3. Cart Items
        if (!Schema::hasTable('cart_items')) {
            Schema::create('cart_items', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->foreignUuid('user_id')->nullable()->constrained('users')->cascadeOnDelete();
                $table->foreignUuid('branch_id')->nullable()->constrained('branches')->nullOnDelete();
                $table->foreignUuid('product_id')->constrained('products')->cascadeOnDelete();
                $table->foreignUuid('variant_id')->nullable()->constrained('product_variants')->nullOnDelete();
                $table->integer('quantity')->default(1);
                $table->json('modifiers_json')->nullable();
                $table->timestamps();
            });
        }

        // 4. Order Status Logs
        if (!Schema::hasTable('order_status_logs')) {
            Schema::create('order_status_logs', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->foreignUuid('order_id')->constrained('orders')->cascadeOnDelete();
                $table->string('from_status')->nullable();
                $table->string('to_status');
                $table->string('actor_type')->nullable(); // admin, customer, system, kds, driver
                $table->string('actor_id')->nullable();
                $table->text('notes')->nullable();
                $table->timestamps();

                $table->index('order_id');
            });
        }

        // 5. RBAC Roles
        if (!Schema::hasTable('rbac_roles')) {
            Schema::create('rbac_roles', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->string('name')->unique();
                $table->string('display_name')->nullable();
                $table->text('description')->nullable();
                $table->timestamps();
            });
        }

        // 6. RBAC Permissions
        if (!Schema::hasTable('rbac_permissions')) {
            Schema::create('rbac_permissions', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->string('name')->unique();
                $table->string('module')->nullable();
                $table->text('description')->nullable();
                $table->timestamps();
            });
        }

        // 7. RBAC Role-Permission Link
        if (!Schema::hasTable('rbac_role_permissions')) {
            Schema::create('rbac_role_permissions', function (Blueprint $table) {
                $table->foreignUuid('role_id')->constrained('rbac_roles')->cascadeOnDelete();
                $table->foreignUuid('permission_id')->constrained('rbac_permissions')->cascadeOnDelete();
                $table->primary(['role_id', 'permission_id']);
            });
        }

        // 8. Admin RBAC Assignments
        if (!Schema::hasTable('admin_rbac_assignments')) {
            Schema::create('admin_rbac_assignments', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->foreignUuid('admin_id')->constrained('admins')->cascadeOnDelete();
                $table->foreignUuid('role_id')->constrained('rbac_roles')->cascadeOnDelete();
                $table->foreignUuid('branch_id')->nullable()->constrained('branches')->nullOnDelete();
                $table->timestamps();
            });
        }

        // 9. POS Integration Configs
        if (!Schema::hasTable('pos_integration_configs')) {
            Schema::create('pos_integration_configs', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->foreignUuid('branch_id')->constrained('branches')->cascadeOnDelete();
                $table->string('provider')->default('petpooja');
                $table->text('api_key')->nullable();
                $table->text('api_secret')->nullable();
                $table->string('store_id')->nullable();
                $table->boolean('is_active')->default(true);
                $table->json('config_json')->nullable();
                $table->timestamps();
            });
        }

        // 10. Delivery Partner Integrations
        if (!Schema::hasTable('delivery_partner_integrations')) {
            Schema::create('delivery_partner_integrations', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->string('provider')->default('inhouse');
                $table->foreignUuid('branch_id')->nullable()->constrained('branches')->nullOnDelete();
                $table->text('api_key')->nullable();
                $table->boolean('is_active')->default(true);
                $table->string('webhook_secret')->nullable();
                $table->timestamps();
            });
        }

        // 11. Delivery Assignments
        if (!Schema::hasTable('delivery_assignments')) {
            Schema::create('delivery_assignments', function (Blueprint $table) {
                $table->uuid('id')->primary();
                $table->foreignUuid('order_id')->constrained('orders')->cascadeOnDelete();
                $table->foreignUuid('partner_id')->nullable()->constrained('delivery_partner_integrations')->nullOnDelete();
                $table->string('rider_name')->nullable();
                $table->string('rider_phone')->nullable();
                $table->string('tracking_url')->nullable();
                $table->string('status')->default('assigned');
                $table->timestamp('dispatched_at')->nullable();
                $table->timestamp('delivered_at')->nullable();
                $table->timestamps();

                $table->index('order_id');
            });
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('delivery_assignments');
        Schema::dropIfExists('delivery_partner_integrations');
        Schema::dropIfExists('pos_integration_configs');
        Schema::dropIfExists('admin_rbac_assignments');
        Schema::dropIfExists('rbac_role_permissions');
        Schema::dropIfExists('rbac_permissions');
        Schema::dropIfExists('rbac_roles');
        Schema::dropIfExists('order_status_logs');
        Schema::dropIfExists('cart_items');
        Schema::dropIfExists('user_profiles');
        Schema::dropIfExists('otp_codes');
    }
};
