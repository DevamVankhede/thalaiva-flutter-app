<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class PosIntegrationConfig extends Model
{
    use HasUuids;

    protected $table = 'pos_integration_configs';

    protected $fillable = [
        'branch_id',
        'provider',
        'store_id',
        'api_key_hash',
        'api_key',
        'webhook_url',
        'webhook_secret',
        'is_active',
        'config_json',
        'last_synced_at',
    ];

    protected $casts = [
        'is_active' => 'boolean',
        'config_json' => 'array',
        'last_synced_at' => 'datetime',
    ];

    public function branch(): BelongsTo
    {
        return $this->belongsTo(Branch::class, 'branch_id');
    }
}
