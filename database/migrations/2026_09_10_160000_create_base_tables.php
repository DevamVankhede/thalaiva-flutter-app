<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('branches', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->string('name', 150);
            $table->string('slug', 150)->unique();
            $table->string('address_line', 255);
            $table->string('phone', 20)->nullable();
            $table->boolean('is_active')->default(true);
            $table->integer('sort_order')->default(0);
            $table->timestamps();
        });

        Schema::create('users', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->string('phone', 20)->unique();
            $table->string('email', 150)->nullable()->unique();
            $table->string('name', 150)->nullable();
            $table->string('password', 255)->nullable();
            $table->timestamp('otp_verified_at')->nullable();
            $table->text('fcm_token')->nullable();
            $table->string('locale', 10)->default('en');
            $table->boolean('is_active')->default(true);
            $table->timestamps();
        });

        Schema::create('admins', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->string('email', 150)->unique();
            $table->string('password_hash', 255)->nullable();
            $table->boolean('is_active')->default(true);
            $table->timestamps();
        });

        Schema::create('categories', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('branch_id')->constrained('branches')->onDelete('cascade');
            $table->string('name', 100);
            $table->string('slug', 100);
            $table->boolean('is_active')->default(true);
            $table->integer('sort_order')->default(0);
            $table->timestamps();
            $table->unique(['branch_id', 'slug']);
        });

        Schema::create('products', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('branch_id')->constrained('branches')->onDelete('cascade');
            $table->foreignUuid('category_id')->constrained('categories')->onDelete('cascade');
            $table->string('name', 150);
            $table->string('slug', 150);
            $table->bigInteger('base_price'); // in paise (e.g., 18000 = Rs 180)
            $table->boolean('is_veg')->default(true);
            $table->boolean('is_spicy')->default(false);
            $table->boolean('is_available')->default(true);
            $table->integer('prep_time_min')->default(15);
            $table->json('meta_json')->nullable();
            $table->string('image_url', 500)->nullable();
            $table->timestamps();
            $table->unique(['branch_id', 'slug']);
        });

        Schema::create('product_variants', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('product_id')->constrained('products')->onDelete('cascade');
            $table->string('name', 100);
            $table->string('sku', 100)->nullable();
            $table->bigInteger('price_adjustment')->default(0);
            $table->integer('prep_time_adjustment')->default(0);
            $table->boolean('is_default')->default(false);
            $table->boolean('is_available')->default(true);
            $table->timestamps();
        });

        Schema::create('modifier_groups', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('branch_id')->constrained('branches')->onDelete('cascade');
            $table->string('name', 100);
            $table->string('modifier_type', 50)->default('optional');
            $table->integer('min_select')->default(0);
            $table->integer('max_select')->default(1);
            $table->boolean('is_required')->default(false);
            $table->boolean('is_active')->default(true);
            $table->integer('sort_order')->default(0);
            $table->timestamps();
        });

        Schema::create('modifier_options', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('modifier_group_id')->constrained('modifier_groups')->onDelete('cascade');
            $table->string('name', 100);
            $table->bigInteger('price_adjustment')->default(0);
            $table->boolean('is_default')->default(false);
            $table->boolean('is_available')->default(true);
            $table->timestamps();
        });

        Schema::create('product_modifier_links', function (Blueprint $table) {
            $table->foreignUuid('product_id')->constrained('products')->onDelete('cascade');
            $table->foreignUuid('modifier_group_id')->constrained('modifier_groups')->onDelete('cascade');
            $table->boolean('is_required')->default(false);
            $table->primary(['product_id', 'modifier_group_id']);
        });

        Schema::create('coupons', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('branch_id')->nullable()->constrained('branches')->onDelete('cascade');
            $table->string('code', 50)->unique();
            $table->enum('type', ['percent', 'fixed']);
            $table->decimal('value', 10, 2);
            $table->dateTime('valid_from');
            $table->dateTime('valid_to');
            $table->integer('max_uses')->default(1000);
            $table->integer('used_count')->default(0);
            $table->boolean('is_active')->default(true);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('coupons');
        Schema::dropIfExists('product_modifier_links');
        Schema::dropIfExists('modifier_options');
        Schema::dropIfExists('modifier_groups');
        Schema::dropIfExists('product_variants');
        Schema::dropIfExists('products');
        Schema::dropIfExists('categories');
        Schema::dropIfExists('admins');
        Schema::dropIfExists('users');
        Schema::dropIfExists('branches');
    }
};
