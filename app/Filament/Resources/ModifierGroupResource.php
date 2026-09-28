<?php

namespace App\Filament\Resources;

use App\Filament\Resources\ModifierGroupResource\Pages;
use App\Models\ModifierGroup;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class ModifierGroupResource extends Resource
{
    protected static ?string $model = ModifierGroup::class;
    protected static ?string $navigationIcon = 'heroicon-o-adjustments-horizontal';
    protected static ?string $navigationGroup = 'Menu & Catalog';

    public static function form(Form $form): Form
    {
        return $form->schema([
            Forms\Components\Select::make('branch_id')
                ->relationship('branch', 'name')
                ->required(),
            Forms\Components\TextInput::make('name')->required(),
            Forms\Components\Select::make('modifier_type')
                ->options([
                    'optional' => 'Optional',
                    'required' => 'Required',
                    'multiple' => 'Multiple',
                ])
                ->default('optional'),
            Forms\Components\TextInput::make('min_select')->numeric()->default(0),
            Forms\Components\TextInput::make('max_select')->numeric()->default(1),
            Forms\Components\TextInput::make('sort_order')->numeric()->default(0),
            Forms\Components\Toggle::make('is_required')->default(false),
            Forms\Components\Toggle::make('is_active')->default(true),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([
            Tables\Columns\TextColumn::make('name')->searchable()->sortable(),
            Tables\Columns\TextColumn::make('branch.name')->label('Branch')->sortable(),
            Tables\Columns\TextColumn::make('modifier_type')->badge(),
            Tables\Columns\TextColumn::make('min_select'),
            Tables\Columns\TextColumn::make('max_select'),
            Tables\Columns\IconColumn::make('is_required')->boolean(),
            Tables\Columns\IconColumn::make('is_active')->boolean(),
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
            'index' => Pages\ManageModifierGroups::route('/'),
        ];
    }
}
