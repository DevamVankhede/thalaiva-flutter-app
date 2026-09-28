<?php

namespace App\Filament\Resources;

use App\Filament\Resources\UserProfileResource\Pages;
use App\Models\UserProfile;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class UserProfileResource extends Resource
{
    protected static ?string $model = UserProfile::class;
    protected static ?string $navigationIcon = 'heroicon-o-user';
    protected static ?string $navigationGroup = 'Customers';

    public static function form(Form $form): Form
    {
        return $form->schema([

            Forms\Components\Select::make('user_id')->relationship('user', 'phone')->required(),
            Forms\Components\TextInput::make('dietary_preference'),
            Forms\Components\Textarea::make('default_delivery_address'),
            Forms\Components\DatePicker::make('birthday'),
            Forms\Components\DatePicker::make('anniversary'),
        
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([

            Tables\Columns\TextColumn::make('user.phone')->label('User Phone'),
            Tables\Columns\TextColumn::make('dietary_preference'),
            Tables\Columns\TextColumn::make('birthday')->date(),
        
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
            'index' => Pages\ManageUserProfiles::route('/'),
        ];
    }
}
