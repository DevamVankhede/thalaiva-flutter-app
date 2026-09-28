<?php

namespace App\Filament\Resources\DeliveryPartnerIntegrationResource\Pages;

use App\Filament\Resources\DeliveryPartnerIntegrationResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManageDeliveryPartnerIntegrations extends ManageRecords
{
    protected static string $resource = DeliveryPartnerIntegrationResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
