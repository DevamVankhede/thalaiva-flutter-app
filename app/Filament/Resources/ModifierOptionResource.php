<?php

namespace App\Filament\Resources;

use App\Filament\Resources\ModifierOptionResource\Pages;
use App\Models\ModifierOption;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class ModifierOptionResource extends Resource
{
    protected static ?string $model = ModifierOption::class;
    protected static ?string $navigationIcon = 'heroicon-o-plus-circle';
    protected static ?string $navigationGroup = 'Menu & Catalog';

    public static function form(Form $form): Form
    {
        return $form->schema([
            Forms\Components\Select::make('modifier_group_id')
                ->relationship('modifierGroup', 'name')
                ->required(),
            Forms\Components\TextInput::make('name')->required(),
            Forms\Components\TextInput::make('price_adjustment')
                ->numeric()
                ->label('Price Adjustment (Paise)')
                ->default(0),
            Forms\Components\TextInput::make('sort_order')->numeric()->default(0),
            Forms\Components\Toggle::make('is_available')->default(true),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([
            Tables\Columns\TextColumn::make('name')->searchable()->sortable(),
            Tables\Columns\TextColumn::make('modifierGroup.name')->label('Group')->sortable(),
            Tables\Columns\TextColumn::make('price_adjustment')->label('Add-on (₹)')->formatStateUsing(fn ($state) => '₹' . number_format($state / 100, 2)),
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
            'index' => Pages\ManageModifierOptions::route('/'),
        ];
    }
}
