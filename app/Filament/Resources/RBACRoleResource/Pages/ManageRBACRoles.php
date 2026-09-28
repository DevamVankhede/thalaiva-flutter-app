<?php

namespace App\Filament\Resources\RBACRoleResource\Pages;

use App\Filament\Resources\RBACRoleResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManageRBACRoles extends ManageRecords
{
    protected static string $resource = RBACRoleResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
