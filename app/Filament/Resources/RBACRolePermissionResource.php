<?php

namespace App\Filament\Resources;

use App\Filament\Resources\RBACRolePermissionResource\Pages;
use App\Models\RbacRolePermission;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class RBACRolePermissionResource extends Resource
{
    protected static ?string $model = RbacRolePermission::class;
    protected static ?string $navigationIcon = 'heroicon-o-key';
    protected static ?string $navigationGroup = 'Security';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\Select::make('role_id')->relationship('role', 'name')->required(),
            Forms\Components\Select::make('permission_id')->relationship('permission', 'name')->required(),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('role.name')->label('Role'),
            Tables\Columns\TextColumn::make('permission.name')->label('Permission'),
        
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
            'index' => Pages\ManageRBACRolePermissions::route('/'),
        ];
    }
}
