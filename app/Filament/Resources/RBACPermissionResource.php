<?php

namespace App\Filament\Resources;

use App\Filament\Resources\RBACPermissionResource\Pages;
use App\Models\RbacPermission;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class RBACPermissionResource extends Resource
{
    protected static ?string $model = RbacPermission::class;
    protected static ?string $navigationIcon = 'heroicon-o-lock-closed';
    protected static ?string $navigationGroup = 'Security';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\TextInput::make('name')->required()->unique(ignoreRecord: true),
            Forms\Components\TextInput::make('module'),
            Forms\Components\Textarea::make('description'),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('name')->searchable(),
            Tables\Columns\TextColumn::make('module'),
        
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
            'index' => Pages\ManageRBACPermissions::route('/'),
        ];
    }
}
