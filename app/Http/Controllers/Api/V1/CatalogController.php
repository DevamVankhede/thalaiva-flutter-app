<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Models\Branch;
use App\Models\Category;
use App\Models\Product;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class CatalogController extends Controller
{
    /**
     * Get active branches in Surat.
     */
    public function branches(): JsonResponse
    {
        $branches = Branch::where('is_active', true)
            ->orderBy('sort_order')
            ->get();

        return response()->json([
            'success' => true,
            'data' => $branches,
        ]);
    }

    /**
     * Get categories with dish counts.
     */
    public function categories(): JsonResponse
    {
        $categories = Category::where('is_active', true)
            ->withCount(['products' => fn($q) => $q->where('is_available', true)])
            ->orderBy('sort_order')
            ->get();

        return response()->json([
            'success' => true,
            'data' => $categories,
        ]);
    }

    /**
     * Get products filtered by category, search query, or branch.
     */
    public function products(Request $request): JsonResponse
    {
        $query = Product::where('is_available', true)
            ->with([
                'category',
                'variants' => fn($q) => $q->where('is_available', true),
                'modifierLinks.modifierGroup.options' => fn($q) => $q->where('is_available', true),
            ]);

        if ($request->filled('category_id')) {
            $query->where('category_id', $request->input('category_id'));
        }

        if ($request->filled('search')) {
            $search = $request->input('search');
            $query->where(function ($q) use ($search) {
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('description', 'like', "%{$search}%");
            });
        }

        if ($request->boolean('is_veg')) {
            $query->where('is_veg', true);
        }

        $perPage = (int) $request->input('per_page', 50);
        $products = $query->paginate($perPage);

        $transformed = $products->getCollection()->map(function ($p) {
            $meta = is_string($p->meta_json) ? json_decode($p->meta_json, true) : ($p->meta_json ?? []);

            $modGroups = $p->modifierLinks->map(function ($link) {
                $grp = $link->modifierGroup;
                if (!$grp) return null;
                return [
                    'id' => $grp->id,
                    'name' => $grp->name,
                    'is_required' => (bool) $grp->is_required,
                    'min_select' => $grp->min_select,
                    'max_select' => $grp->max_select,
                    'options' => $grp->options->map(fn($o) => [
                        'id' => $o->id,
                        'name' => $o->name,
                        'price_adjustment' => $o->price_adjustment,
                        'price_inr' => round($o->price_adjustment / 100, 2),
                    ]),
                ];
            })->filter()->values();

            return [
                'id' => $p->id,
                'name' => $p->name,
                'slug' => $p->slug,
                'category_id' => $p->category_id,
                'category_name' => $p->category?->name,
                'base_price_paise' => (int) $p->base_price,
                'price_inr' => round($p->base_price / 100, 2),
                'is_veg' => (bool) $p->is_veg,
                'is_spicy' => (bool) $p->is_spicy,
                'prep_time_min' => $p->prep_time_min,
                'icon_emoji' => $meta['emoji'] ?? ($meta['icon_emoji'] ?? '🍲'),
                'description' => $p->description ?? ($meta['description'] ?? ($meta['desc'] ?? '')),
                'rating' => $meta['rating'] ?? 4.8,
                'rating_count' => $meta['rating_count'] ?? 100,
                'variants' => $p->variants,
                'modifier_groups' => $modGroups,
            ];
        });

        return response()->json([
            'success' => true,
            'data' => $transformed,
            'meta' => [
                'total' => $products->total(),
                'per_page' => $products->perPage(),
                'current_page' => $products->currentPage(),
                'last_page' => $products->lastPage(),
            ],
        ]);
    }
}
