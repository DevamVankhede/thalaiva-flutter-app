<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Concerns\HasUuids;

class ProductVariant extends Model
{
    use HasUuids;

    protected $fillable = [
        'product_id','name','sku','price_adjustment','prep_time_adjustment',
        'is_default','is_available',
    ];
    protected $casts = [
        'price_adjustment'=>'integer','prep_time_adjustment'=>'integer',
        'is_default'=>'boolean','is_available'=>'boolean',
    ];
    public function product() { return $this->belongsTo(Product::class); }
}
