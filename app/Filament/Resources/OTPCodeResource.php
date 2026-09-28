<?php

namespace App\Filament\Resources;

use App\Filament\Resources\OTPCodeResource\Pages;
use App\Models\OtpCode;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class OTPCodeResource extends Resource
{
    protected static ?string $model = OtpCode::class;
    protected static ?string $navigationIcon = 'heroicon-o-key';
    protected static ?string $navigationGroup = 'Security';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\TextInput::make('phone')->required(),
            Forms\Components\TextInput::make('code_hash')->readOnly(),
            Forms\Components\DateTimePicker::make('expires_at'),
            Forms\Components\DateTimePicker::make('verified_at'),
            Forms\Components\TextInput::make('attempts')->numeric()->default(0),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('phone')->searchable(),
            Tables\Columns\TextColumn::make('expires_at')->dateTime(),
            Tables\Columns\TextColumn::make('verified_at')->dateTime(),
            Tables\Columns\TextColumn::make('attempts'),
        
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
            'index' => Pages\ManageOTPCodes::route('/'),
        ];
    }
}
