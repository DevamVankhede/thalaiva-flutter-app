<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class RbacRole extends Model
{
    use HasUuids;

    protected $table = 'rbac_roles';

    protected $fillable = [
        'name',
        'display_name',
        'description',
        
    ];

    protected $casts = [
        
    ];

    public function permissions(): BelongsToMany
    {
        return $this->belongsToMany(RbacPermission::class, 'rbac_role_permissions', 'role_id', 'permission_id');
    }
}
