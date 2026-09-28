<?php

namespace App\Filament\Resources\RBACRolePermissionResource\Pages;

use App\Filament\Resources\RBACRolePermissionResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManageRBACRolePermissions extends ManageRecords
{
    protected static string $resource = RBACRolePermissionResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
