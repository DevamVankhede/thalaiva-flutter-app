<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class ModifierOption extends Model
{
    use HasUuids;

    protected $table = 'modifier_options';

    protected $fillable = [
        'modifier_group_id',
        'name',
        'price_adjustment',
        'is_available',
        'sort_order',
    ];

    protected $casts = [
        'price_adjustment' => 'integer',
        'is_available' => 'boolean',
        'sort_order' => 'integer',
    ];

    public function group(): BelongsTo
    {
        return $this->belongsTo(ModifierGroup::class, 'modifier_group_id');
    }

    public function modifierGroup(): BelongsTo
    {
        return $this->belongsTo(ModifierGroup::class, 'modifier_group_id');
    }
}
