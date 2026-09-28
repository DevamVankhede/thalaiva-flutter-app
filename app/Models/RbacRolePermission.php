<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class RbacRolePermission extends Model
{
    protected $table = 'rbac_role_permissions';

    public $incrementing = false;
    public $timestamps = false;
    protected $primaryKey = null;

    protected $fillable = [
        'role_id',
        'permission_id',
    ];

    public function role(): BelongsTo
    {
        return $this->belongsTo(RbacRole::class, 'role_id');
    }

    public function permission(): BelongsTo
    {
        return $this->belongsTo(RbacPermission::class, 'permission_id');
    }
}
