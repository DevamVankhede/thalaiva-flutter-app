<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class OrderStoreRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'branch_id' => 'required|string|max:50',
            'order_type' => 'nullable|string|in:delivery,takeaway,dine_in',
            'delivery_address' => 'required|string|max:255',
            'delivery_instructions' => 'nullable|string|max:255',
            'contactless' => 'nullable|boolean',
            'tip_amount' => 'nullable|numeric|min:0|max:1000',
            'coupon_code' => 'nullable|string|max:30|alpha_num',
            'items' => 'required|array|min:1|max:50',
            'items.*.product_id' => 'required|string|max:50',
            'items.*.quantity' => 'required|integer|min:1|max:20',
            'items.*.modifiers' => 'nullable|array|max:10',
            'items.*.modifiers.*.id' => 'required_with:items.*.modifiers|string|max:50',
            'items.*.modifiers.*.name' => 'required_with:items.*.modifiers|string|max:100',
            'items.*.modifiers.*.price' => 'required_with:items.*.modifiers|numeric|min:0|max:500',
        ];
    }

    /**
     * Sanitize input before validation to neutralize XSS payloads.
     */
    protected function prepareForValidation(): void
    {
        $this->merge([
            'delivery_address' => strip_tags((string) $this->input('delivery_address')),
            'delivery_instructions' => strip_tags((string) $this->input('delivery_instructions')),
            'coupon_code' => strtoupper(trim((string) $this->input('coupon_code'))),
        ]);
    }
}
