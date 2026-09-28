<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class RbacPermission extends Model
{
    use HasUuids;

    protected $table = 'rbac_permissions';

    protected $fillable = [
        'name',
        
        'module',
        'description',
    ];

    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(RbacRole::class, 'rbac_role_permissions', 'permission_id', 'role_id');
    }
}
