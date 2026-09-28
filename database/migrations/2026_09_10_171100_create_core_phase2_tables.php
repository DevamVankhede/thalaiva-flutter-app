<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('user_id')->constrained('users')->onDelete('restrict');
            $table->foreignUuid('branch_id')->constrained('branches')->onDelete('restrict');
            $table->string('order_number')->unique(); // THL-YYYYMMDD-NNNN
            $table->enum('status', ['pending','confirmed','preparing','out_for_delivery','delivered','cancelled']);
            $table->enum('payment_status', ['none','pending','paid','failed','refunded']);
            $table->bigInteger('subtotal')->default(0);
            $table->bigInteger('tax_amount')->default(0);
            $table->bigInteger('discount_amount')->default(0);
            $table->bigInteger('total_amount')->default(0);
            $table->bigInteger('delivery_charge')->default(0);
            $table->enum('discount_type', ['none','percent','fixed'])->nullable();
            $table->decimal('discount_value', 10, 2)->nullable();
            $table->text('notes')->nullable();
            $table->text('special_instructions')->nullable();
            $table->string('delivery_name');
            $table->string('delivery_phone');
            $table->string('delivery_address_line');
            $table->string('delivery_city');
            $table->string('delivery_postal');
            $table->foreignUuid('payment_id')->nullable();
            $table->timestamp('status_changed_at')->nullable();
            $table->timestamps();
            
            if (DB::getDriverName() === 'pgsql') {
                DB::statement("ALTER TABLE orders ADD CONSTRAINT chk_total_computed CHECK (total_amount = subtotal + tax_amount - discount_amount + delivery_charge)");
            }
        });

        Schema::create('payments', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('order_id')->unique()->constrained('orders')->onDelete('restrict');
            $table->string('razorpay_payment_id', 100)->unique()->nullable();
            $table->bigInteger('amount');
            $table->char('currency', 3)->default('INR');
            $table->enum('status', ['created','authorized','captured','failed','refunded']);
            $table->enum('capture_status', ['pending','captured','partial']);
            $table->integer('attempts')->default(0);
            $table->string('error_code')->nullable();
            $table->text('error_description')->nullable();
            $table->timestamp('collected_at')->nullable();
            $table->timestamp('refunded_at')->nullable();
            $table->bigInteger('refund_amount')->default(0);
            $table->timestamps();
        });

        Schema::create('order_items', function (Blueprint $table) {
            $table->id(); // BIGSERIAL PK
            $table->foreignUuid('order_id')->constrained('orders')->onDelete('cascade');
            $table->foreignUuid('product_id')->nullable()->constrained('products')->onDelete('restrict');
            $table->foreignUuid('variant_id')->nullable()->constrained('product_variants')->onDelete('restrict');
            $table->integer('quantity')->default(1);
            $table->bigInteger('unit_price');
            $table->bigInteger('line_total');
            $table->string('product_name_snapshot', 255);
            $table->string('variant_name_snapshot', 255)->nullable();
            $table->json('modifier_snapshot_json')->nullable();
            $table->bigInteger('discount_applied')->default(0);
            $table->decimal('tax_rate', 5, 2)->default(0.00);
            $table->timestamps();
            
            if (DB::getDriverName() === 'pgsql') {
                DB::statement("ALTER TABLE order_items ADD CONSTRAINT chk_line_total CHECK (line_total = unit_price * quantity)");
            }
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('order_items');
        Schema::dropIfExists('payments');
        Schema::dropIfExists('orders');
    }
};
