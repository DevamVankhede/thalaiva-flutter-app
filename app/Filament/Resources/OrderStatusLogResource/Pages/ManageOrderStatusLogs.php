<?php

namespace App\Filament\Resources\OrderStatusLogResource\Pages;

use App\Filament\Resources\OrderStatusLogResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManageOrderStatusLogs extends ManageRecords
{
    protected static string $resource = OrderStatusLogResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
