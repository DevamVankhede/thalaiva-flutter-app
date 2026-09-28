<?php

namespace App\Filament\Resources;

use App\Filament\Resources\DeliveryPartnerIntegrationResource\Pages;
use App\Models\DeliveryPartnerIntegration;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class DeliveryPartnerIntegrationResource extends Resource
{
    protected static ?string $model = DeliveryPartnerIntegration::class;
    protected static ?string $navigationIcon = 'heroicon-o-truck';
    protected static ?string $navigationGroup = 'Integrations';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\TextInput::make('provider')->default('inhouse')->required(),
            Forms\Components\Select::make('branch_id')->relationship('branch', 'name'),
            Forms\Components\Toggle::make('is_active')->default(true),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('provider'),
            Tables\Columns\TextColumn::make('branch.name')->label('Branch'),
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
            'index' => Pages\ManageDeliveryPartnerIntegrations::route('/'),
        ];
    }
}
