<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;

class CartItem extends Model
{
    protected $fillable = [
        'user_id','product_id','quantity','modifier_ids_json',
    ];
    protected $casts = [
        'quantity'=>'integer','modifier_ids_json'=>'array',
    ];
    public function user() { return $this->belongsTo(User::class); }
    public function product() { return $this->belongsTo(Product::class); }
}
