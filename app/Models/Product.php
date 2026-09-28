<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Product extends Model
{
    use HasUuids;

    protected $fillable = [
        'branch_id','category_id','name','slug','base_price','is_veg',
        'is_spicy','is_available','prep_time_min','meta_json','image_url',
    ];
    protected $casts = [
        'base_price'=>'integer','is_veg'=>'boolean','is_spicy'=>'boolean',
        'is_available'=>'boolean','meta_json'=>'json',
    ];
    public function category(): \Illuminate\Database\Eloquent\Relations\BelongsTo { return $this->belongsTo(Category::class); }
    public function branch(): \Illuminate\Database\Eloquent\Relations\BelongsTo { return $this->belongsTo(Branch::class); }
    public function variants(): HasMany { return $this->hasMany(ProductVariant::class); }
    public function modifierLinks(): HasMany { return $this->hasMany(ProductModifierLink::class); }
}
