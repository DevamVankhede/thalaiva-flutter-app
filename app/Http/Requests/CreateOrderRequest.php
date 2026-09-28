<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\Validator;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Http\Exceptions\HttpResponseException;

class CreateOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'branch_id' => 'required|uuid|exists:branches,id',
            'items' => 'required|array|min:1',
            'items.*.product_id' => 'required|uuid|exists:products,id',
            'items.*.variant_id' => 'nullable|uuid|exists:product_variants,id',
            'items.*.quantity' => 'required|integer|min:1|max:50',
            'items.*.modifiers' => 'nullable|array',
            'items.*.modifiers.*.id' => 'nullable|uuid|exists:modifier_options,id',
            'coupon_code' => 'nullable|string|max:50',
            'delivery_name' => 'required|string|max:255',
            'delivery_phone' => 'required|string|max:20',
            'delivery_address_line' => 'required|string|max:500',
            'delivery_city' => 'nullable|string|max:100',
            'delivery_postal' => 'nullable|string|max:20',
            'payment_provider' => 'nullable|string|max:50',
            'notes' => 'nullable|string|max:500',
        ];
    }

    protected function failedValidation(Validator $validator)
    {
        throw new HttpResponseException(response()->json([
            'success' => false,
            'message' => 'Validation error',
            'errors' => $validator->errors(),
        ], 422));
    }
}
