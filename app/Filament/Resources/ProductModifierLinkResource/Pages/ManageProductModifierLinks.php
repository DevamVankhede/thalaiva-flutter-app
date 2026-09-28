<?php

namespace App\Filament\Resources\ProductModifierLinkResource\Pages;

use App\Filament\Resources\ProductModifierLinkResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManageProductModifierLinks extends ManageRecords
{
    protected static string $resource = ProductModifierLinkResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
