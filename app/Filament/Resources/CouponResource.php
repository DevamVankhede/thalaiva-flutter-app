<?php

namespace App\Filament\Resources;

use App\Filament\Resources\CouponResource\Pages;
use App\Models\Coupon;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class CouponResource extends Resource
{
    protected static ?string $model = Coupon::class;
    protected static ?string $navigationIcon = 'heroicon-o-ticket';
    protected static ?string $navigationGroup = 'Marketing & Promotions';

    public static function form(Form $form): Form
    {
        return $form->schema([
            Forms\Components\Select::make('branch_id')
                ->relationship('branch', 'name')
                ->nullable()
                ->label('Branch (Leave empty for All Branches)'),
            Forms\Components\TextInput::make('code')->required()->unique(ignoreRecord: true),
            Forms\Components\Select::make('type')->options(['fixed' => 'Fixed Amount (₹)', 'percent' => 'Percentage (%)'])->required(),
            Forms\Components\TextInput::make('value')->numeric()->required(),
            Forms\Components\DateTimePicker::make('valid_from'),
            Forms\Components\DateTimePicker::make('valid_to'),
            Forms\Components\TextInput::make('max_uses')->numeric()->default(1000),
            Forms\Components\TextInput::make('used_count')->numeric()->default(0)->readOnly(),
            Forms\Components\Toggle::make('is_active')->default(true),
        ]);
    }

    public static function table(Table $table): Table
    {
        return $table->columns([
            Tables\Columns\TextColumn::make('code')->searchable()->sortable(),
            Tables\Columns\TextColumn::make('type')->badge(),
            Tables\Columns\TextColumn::make('value')->formatStateUsing(fn ($record, $state) => $record->type === 'percent' ? $state . '%' : '₹' . number_format($state, 0))->sortable(),
            Tables\Columns\TextColumn::make('valid_to')->label('Valid Until')->dateTime(),
            Tables\Columns\TextColumn::make('used_count')->label('Redeemed'),
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
            'index' => Pages\ManageCoupons::route('/'),
        ];
    }
}
