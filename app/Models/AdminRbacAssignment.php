<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class AdminRbacAssignment extends Model
{
    use HasUuids;

    protected $table = 'admin_rbac_assignments';

    protected $fillable = [
        'admin_id',
        'role_id',
        'branch_id',
    ];

    public function admin(): BelongsTo
    {
        return $this->belongsTo(Admin::class, 'admin_id');
    }

    public function role(): BelongsTo
    {
        return $this->belongsTo(RbacRole::class, 'role_id');
    }

    public function branch(): BelongsTo
    {
        return $this->belongsTo(Branch::class, 'branch_id');
    }
}
