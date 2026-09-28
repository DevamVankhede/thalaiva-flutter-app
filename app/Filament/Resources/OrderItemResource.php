<?php

namespace App\Filament\Resources;

use App\Filament\Resources\OrderItemResource\Pages;
use App\Models\OrderItem;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class OrderItemResource extends Resource
{
    protected static ?string $model = OrderItem::class;
    protected static ?string $navigationIcon = 'heroicon-o-list-bullet';
    protected static ?string $navigationGroup = 'Orders & Sales';

    public static function form(Form $form): Form
    {
        return $form->schema([
            Forms\Components\Select::make('order_id')
                ->relationship('order', 'order_number')
                ->required(),
            Forms\Components\Select::make('product_id')
                ->relationship('product', 'name')
                ->nullable(),
            Forms\Components\TextInput::make('product_name_snapshot')->required(),
            Forms\Components\TextInput::make('quantity')->numeric()->default(1)->required(),
            Forms\Components\TextInput::make('unit_price')->numeric()->label('Unit Price (Paise)')->required(),
            Forms\Components\TextInput::make('line_total')->numeric()->label('Line Total (Paise)')->required(),
            Forms\Components\KeyValue::make('modifier_snapshot_json')->columnSpanFull(),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([
            Tables\Columns\TextColumn::make('order.order_number')->label('Order #')->searchable(),
            Tables\Columns\TextColumn::make('product_name_snapshot')->label('Item'),
            Tables\Columns\TextColumn::make('quantity'),
            Tables\Columns\TextColumn::make('unit_price')->label('Unit (₹)')->formatStateUsing(fn ($state) => '₹' . number_format($state / 100, 2)),
            Tables\Columns\TextColumn::make('line_total')->label('Line Total (₹)')->formatStateUsing(fn ($state) => '₹' . number_format($state / 100, 2)),
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
            'index' => Pages\ManageOrderItems::route('/'),
        ];
    }
}
