<?php

namespace App\Filament\Resources\POSIntegrationResource\Pages;

use App\Filament\Resources\POSIntegrationResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManagePOSIntegrations extends ManageRecords
{
    protected static string $resource = POSIntegrationResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
