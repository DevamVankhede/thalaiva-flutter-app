<?php

namespace App\Models;

namespace App\Filament\Resources;

use App\Filament\Resources\OrderResource\Pages;
use App\Models\Order;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class OrderResource extends Resource
{
    protected static ?string $model = Order::class;
    protected static ?string $navigationIcon = 'heroicon-o-shopping-bag';
    protected static ?string $navigationGroup = 'Orders & Sales';

    public static function form(Form $form): Form
    {
        return $form->schema([
            Forms\Components\TextInput::make('order_number')->readOnly(),
            Forms\Components\Select::make('branch_id')
                ->relationship('branch', 'name')
                ->required(),
            Forms\Components\Select::make('status')->options([
                'pending' => 'Pending',
                'confirmed' => 'Confirmed',
                'preparing' => 'Preparing',
                'out_for_delivery' => 'Out for Delivery',
                'delivered' => 'Delivered',
                'cancelled' => 'Cancelled',
            ])->required(),
            Forms\Components\Select::make('payment_status')->options([
                'pending' => 'Pending',
                'paid' => 'Paid',
                'failed' => 'Failed',
                'refunded' => 'Refunded',
            ])->required(),
            Forms\Components\TextInput::make('delivery_name'),
            Forms\Components\TextInput::make('delivery_phone'),
            Forms\Components\Textarea::make('delivery_address_line'),
            Forms\Components\TextInput::make('total_amount')
                ->numeric()
                ->label('Total Amount (Paise)')
                ->readOnly(),
            Forms\Components\Textarea::make('notes'),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([
            Tables\Columns\TextColumn::make('order_number')->searchable()->sortable(),
            Tables\Columns\TextColumn::make('branch.name')->label('Branch')->sortable(),
            Tables\Columns\TextColumn::make('status')->badge()->color(fn (string $state): string => match ($state) {
                'pending' => 'warning',
                'confirmed' => 'info',
                'preparing' => 'primary',
                'out_for_delivery' => 'warning',
                'delivered' => 'success',
                'cancelled' => 'danger',
                default => 'gray',
            }),
            Tables\Columns\TextColumn::make('payment_status')->badge()->color(fn (string $state): string => match ($state) {
                'paid' => 'success',
                'pending' => 'warning',
                'failed', 'refunded' => 'danger',
                default => 'gray',
            }),
            Tables\Columns\TextColumn::make('delivery_name')->searchable(),
            Tables\Columns\TextColumn::make('total_amount')->label('Total (₹)')->formatStateUsing(fn ($state) => '₹' . number_format($state / 100, 2)),
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
            'index' => Pages\ManageOrders::route('/'),
        ];
    }
}
