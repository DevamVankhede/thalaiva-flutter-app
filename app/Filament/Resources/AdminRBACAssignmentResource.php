<?php

namespace App\Filament\Resources;

use App\Filament\Resources\AdminRBACAssignmentResource\Pages;
use App\Models\AdminRbacAssignment;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class AdminRBACAssignmentResource extends Resource
{
    protected static ?string $model = AdminRbacAssignment::class;
    protected static ?string $navigationIcon = 'heroicon-o-user-group';
    protected static ?string $navigationGroup = 'Security';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\Select::make('admin_id')->relationship('admin', 'email')->required(),
            Forms\Components\Select::make('role_id')->relationship('role', 'name')->required(),
            Forms\Components\Select::make('branch_id')->relationship('branch', 'name'),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('admin.email')->label('Admin'),
            Tables\Columns\TextColumn::make('role.name')->label('Role'),
            Tables\Columns\TextColumn::make('branch.name')->label('Branch'),
        
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
            'index' => Pages\ManageAdminRBACAssignments::route('/'),
        ];
    }
}
