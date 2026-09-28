<?php

namespace App\Filament\Resources\OTPCodeResource\Pages;

use App\Filament\Resources\OTPCodeResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManageOTPCodes extends ManageRecords
{
    protected static string $resource = OTPCodeResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
