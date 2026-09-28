<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Payment extends Model
{
    use HasUuids;

    public $incrementing = false;
    protected $primaryKey = 'id';
    protected $keyType = 'string';

    protected $fillable = [
        'order_id','razorpay_payment_id','amount','currency','status',
        'capture_status','attempts','error_code','error_description',
        'collected_at','refunded_at','refund_amount',
    ];
    protected $casts = [
        'amount'=>'integer','attempts'=>'integer','refunded_at'=>'datetime',
        'collected_at'=>'datetime','refund_amount'=>'integer',
    ];

    // Fixed circular dependency: payments FK -> orders (RESTRICT); orders.payment_id nullable (no reverse required FK)
    public function order(): BelongsTo { return $this->belongsTo(Order::class, 'order_id'); }
}
