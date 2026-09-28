<?php

namespace App\Filament\Resources;

use App\Filament\Resources\OrderStatusLogResource\Pages;
use App\Models\OrderStatusLog;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class OrderStatusLogResource extends Resource
{
    protected static ?string $model = OrderStatusLog::class;
    protected static ?string $navigationIcon = 'heroicon-o-clock';
    protected static ?string $navigationGroup = 'Orders & Sales';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\Select::make('order_id')->relationship('order', 'order_number')->required(),
            Forms\Components\TextInput::make('from_status'),
            Forms\Components\TextInput::make('to_status')->required(),
            Forms\Components\TextInput::make('actor_type'),
            Forms\Components\Textarea::make('notes'),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('order.order_number')->label('Order #'),
            Tables\Columns\TextColumn::make('from_status'),
            Tables\Columns\TextColumn::make('to_status'),
            Tables\Columns\TextColumn::make('actor_type'),
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
            'index' => Pages\ManageOrderStatusLogs::route('/'),
        ];
    }
}
