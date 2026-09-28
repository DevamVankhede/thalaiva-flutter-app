<?php

namespace App\Filament\Resources;

use App\Filament\Resources\ProductModifierLinkResource\Pages;
use App\Models\ProductModifierLink;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class ProductModifierLinkResource extends Resource
{
    protected static ?string $model = ProductModifierLink::class;
    protected static ?string $navigationIcon = 'heroicon-o-link';
    protected static ?string $navigationGroup = 'Menu Catalog';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\Select::make('product_id')->relationship('product', 'name')->required(),
            Forms\Components\Select::make('modifier_group_id')->relationship('modifierGroup', 'name')->required(),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('product.name')->label('Product'),
            Tables\Columns\TextColumn::make('modifierGroup.name')->label('Modifier Group'),
        
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
            'index' => Pages\ManageProductModifierLinks::route('/'),
        ];
    }
}
