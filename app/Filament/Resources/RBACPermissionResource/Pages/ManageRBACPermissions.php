<?php

namespace App\Filament\Resources\RBACPermissionResource\Pages;

use App\Filament\Resources\RBACPermissionResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManageRBACPermissions extends ManageRecords
{
    protected static string $resource = RBACPermissionResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
