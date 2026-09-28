<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;

class OrderItem extends Model
{
    protected $fillable = [
        'order_id','product_id','variant_id','quantity','unit_price',
        'line_total','product_name_snapshot','variant_name_snapshot',
        'modifier_snapshot_json','discount_applied','tax_rate',
    ];
    protected $casts = [
        'variant_id'=>'string','quantity'=>'integer','unit_price'=>'integer',
        'line_total'=>'integer','modifier_snapshot_json'=>'json',
        'discount_applied'=>'integer','tax_rate'=>'decimal:2',
    ];

    public function order() { return $this->belongsTo(Order::class); }
    public function product() { return $this->belongsTo(Product::class); }
}
