<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Category extends Model
{
    use HasUuids;

    protected $fillable = ['branch_id', 'name', 'slug', 'is_active', 'sort_order'];
    protected $casts = ['is_active'=>'boolean'];
    public function products(): HasMany { return $this->hasMany(Product::class); }
}
