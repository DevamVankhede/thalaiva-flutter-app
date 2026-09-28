<?php

namespace App\Filament\Resources;

use App\Filament\Resources\DeliveryAssignmentResource\Pages;
use App\Models\DeliveryAssignment;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class DeliveryAssignmentResource extends Resource
{
    protected static ?string $model = DeliveryAssignment::class;
    protected static ?string $navigationIcon = 'heroicon-o-map-pin';
    protected static ?string $navigationGroup = 'Integrations';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\Select::make('order_id')->relationship('order', 'order_number')->required(),
            Forms\Components\TextInput::make('rider_name'),
            Forms\Components\TextInput::make('rider_phone'),
            Forms\Components\Select::make('status')->options(['assigned'=>'Assigned','picked_up'=>'Picked Up','delivered'=>'Delivered','cancelled'=>'Cancelled'])->default('assigned'),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('order.order_number')->label('Order #'),
            Tables\Columns\TextColumn::make('rider_name'),
            Tables\Columns\TextColumn::make('rider_phone'),
            Tables\Columns\TextColumn::make('status')->badge(),
            Tables\Columns\TextColumn::make('created_at')->dateTime(),
        
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
            'index' => Pages\ManageDeliveryAssignments::route('/'),
        ];
    }
}
