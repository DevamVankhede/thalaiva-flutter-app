<?php

namespace App\Filament\Resources;

use App\Filament\Resources\ProductVariantResource\Pages;
use App\Models\ProductVariant;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class ProductVariantResource extends Resource
{
    protected static ?string $model = ProductVariant::class;
    protected static ?string $navigationIcon = 'heroicon-o-adjustments-horizontal';
    protected static ?string $navigationGroup = 'Menu Catalog';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\Select::make('product_id')->relationship('product', 'name')->required(),
            Forms\Components\TextInput::make('name')->required(),
            Forms\Components\TextInput::make('sku')->required(),
            Forms\Components\TextInput::make('price_adjustment')->numeric()->default(0),
            Forms\Components\Toggle::make('is_default')->default(false),
            Forms\Components\Toggle::make('is_available')->default(true),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('product.name')->label('Product'),
            Tables\Columns\TextColumn::make('name'),
            Tables\Columns\TextColumn::make('sku'),
            Tables\Columns\TextColumn::make('price_adjustment')->label('Adj (₹)')->formatStateUsing(fn ($state) => '₹' . number_format($state / 100, 2)),
            Tables\Columns\IconColumn::make('is_available')->boolean(),
        
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
            'index' => Pages\ManageProductVariants::route('/'),
        ];
    }
}
