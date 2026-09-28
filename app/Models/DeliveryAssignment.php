<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class DeliveryAssignment extends Model
{
    use HasUuids;

    protected $table = 'delivery_assignments';

    protected $fillable = [
        'order_id',
        'partner_integration_id',
        'partner_order_id',
        'rider_name',
        'rider_phone',
        'status',
        'tracking_url',
        'assigned_at',
        'picked_up_at',
        'delivered_at',
        'failure_reason',
    ];

    protected $casts = [
        'assigned_at' => 'datetime',
        'picked_up_at' => 'datetime',
        'delivered_at' => 'datetime',
    ];

    public function order(): BelongsTo
    {
        return $this->belongsTo(Order::class, 'order_id');
    }

    public function partnerIntegration(): BelongsTo
    {
        return $this->belongsTo(DeliveryPartnerIntegration::class, 'partner_integration_id');
    }
}
