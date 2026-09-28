<?php

namespace App\Filament\Resources;

use App\Filament\Resources\ProductResource\Pages;
use App\Models\Product;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Illuminate\Support\Str;

class ProductResource extends Resource
{
    protected static ?string $model = Product::class;
    protected static ?string $navigationIcon = 'heroicon-o-cake';
    protected static ?string $navigationGroup = 'Menu & Catalog';

    public static function form(Form $form): Form
    {
        return $form->schema([
            Forms\Components\Select::make('branch_id')
                ->relationship('branch', 'name')
                ->required(),
            Forms\Components\Select::make('category_id')
                ->relationship('category', 'name')
                ->required(),
            Forms\Components\TextInput::make('name')
                ->required()
                ->live(onBlur: true)
                ->afterStateUpdated(fn (string $operation, $state, Forms\Set $set) => $operation === 'create' ? $set('slug', Str::slug($state)) : null),
            Forms\Components\TextInput::make('slug')->required(),
            Forms\Components\TextInput::make('base_price')
                ->numeric()
                ->label('Base Price (Paise)')
                ->required(),
            Forms\Components\TextInput::make('image_url')->url(),
            Forms\Components\Toggle::make('is_veg')->default(true),
            Forms\Components\Toggle::make('is_spicy')->default(false),
            Forms\Components\Toggle::make('is_available')->default(true),
            Forms\Components\KeyValue::make('meta_json')
                ->label('Item Metadata (Emoji, Description, etc.)')
                ->columnSpanFull(),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([
            Tables\Columns\TextColumn::make('name')->searchable()->sortable(),
            Tables\Columns\TextColumn::make('category.name')->label('Category')->sortable(),
            Tables\Columns\TextColumn::make('branch.name')->label('Branch')->sortable(),
            Tables\Columns\TextColumn::make('base_price')->label('Price (₹)')->formatStateUsing(fn ($state) => '₹' . number_format($state / 100, 2))->sortable(),
            Tables\Columns\IconColumn::make('is_veg')->boolean(),
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
            'index' => Pages\ManageProducts::route('/'),
        ];
    }
}
