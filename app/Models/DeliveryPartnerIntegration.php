<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class DeliveryPartnerIntegration extends Model
{
    use HasUuids;

    protected $table = 'delivery_partner_integrations';

    protected $fillable = [
        'branch_id',
        'partner_name',
        'api_key',
        'api_key_hash',
        'webhook_url',
        'webhook_secret',
        'is_active',
        'config_json',
    ];

    protected $casts = [
        'is_active' => 'boolean',
        'config_json' => 'array',
    ];

    public function branch(): BelongsTo
    {
        return $this->belongsTo(Branch::class, 'branch_id');
    }
}
