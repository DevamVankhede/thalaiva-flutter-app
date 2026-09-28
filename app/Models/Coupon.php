<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Coupon extends Model
{
    use HasUuids;

    protected $table = 'coupons';

    protected $fillable = [
        'branch_id',
        'code',
        'type',
        'value',
        'valid_from',
        'valid_to',
        'max_uses',
        'used_count',
        'is_active',
    ];

    protected $casts = [
        'value' => 'float',
        'valid_from' => 'datetime',
        'valid_to' => 'datetime',
        'max_uses' => 'integer',
        'used_count' => 'integer',
        'is_active' => 'boolean',
    ];

    public function branch(): BelongsTo
    {
        return $this->belongsTo(Branch::class);
    }
}
