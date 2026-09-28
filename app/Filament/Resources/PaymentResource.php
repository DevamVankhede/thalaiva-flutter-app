<?php

namespace App\Filament\Resources;

use App\Filament\Resources\PaymentResource\Pages;
use App\Models\Payment;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class PaymentResource extends Resource
{
    protected static ?string $model = Payment::class;
    protected static ?string $navigationIcon = 'heroicon-o-currency-inr';
    protected static ?string $navigationGroup = 'Orders & Sales';

    public static function form(Form $form): Form
    {
        return $form->schema([
            Forms\Components\Select::make('order_id')
                ->relationship('order', 'order_number')
                ->required(),
            Forms\Components\TextInput::make('razorpay_payment_id')
                ->label('Razorpay Payment ID'),
            Forms\Components\TextInput::make('amount')
                ->label('Amount (Paise)')
                ->numeric()
                ->required(),
            Forms\Components\TextInput::make('currency')
                ->default('INR')
                ->required(),
            Forms\Components\Select::make('status')
                ->options([
                    'created' => 'Created',
                    'authorized' => 'Authorized',
                    'captured' => 'Captured',
                    'failed' => 'Failed',
                    'refunded' => 'Refunded',
                ])
                ->required(),
            Forms\Components\Select::make('capture_status')
                ->options([
                    'pending' => 'Pending',
                    'captured' => 'Captured',
                    'partial' => 'Partial',
                ]),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([
            Tables\Columns\TextColumn::make('order.order_number')->label('Order #')->searchable(),
            Tables\Columns\TextColumn::make('razorpay_payment_id')->label('Gateway Ref')->searchable(),
            Tables\Columns\TextColumn::make('amount')->label('Amount (₹)')->formatStateUsing(fn ($state) => '₹' . number_format($state / 100, 2))->sortable(),
            Tables\Columns\TextColumn::make('status')->badge()->color(fn (string $state): string => match ($state) {
                'captured' => 'success',
                'authorized' => 'info',
                'created' => 'warning',
                'failed', 'refunded' => 'danger',
                default => 'gray',
            }),
            Tables\Columns\TextColumn::make('currency'),
            Tables\Columns\TextColumn::make('created_at')->dateTime()->sortable(),
        ])->filters([
            //
        ])->actions([
            Tables\Actions\EditAction::make(),
            Tables\Actions\DeleteAction::make(),
        ])->bulkActions([
            Tables\Actions\BulkActionGroup::make([
                Tables\Actions\DeleteBulkAction::make(),
            ]),
        ]);
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ManagePayments::route('/'),
        ];
    }
}
