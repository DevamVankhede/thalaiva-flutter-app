<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;

class ProductModifierLink extends Model
{
    protected $fillable = ['product_id','modifier_group_id','is_required'];
    public $incrementing = false;
    protected $primaryKey = null; // composite PK handled in migration
    protected $casts = ['is_required'=>'boolean'];

    public function product() { return $this->belongsTo(Product::class); }
    public function modifierGroup() { return $this->belongsTo(ModifierGroup::class); }
}
