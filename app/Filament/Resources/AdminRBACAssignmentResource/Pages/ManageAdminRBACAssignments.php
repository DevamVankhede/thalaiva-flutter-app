<?php

namespace App\Filament\Resources\AdminRBACAssignmentResource\Pages;

use App\Filament\Resources\AdminRBACAssignmentResource;
use Filament\Actions;
use Filament\Resources\Pages\ManageRecords;

class ManageAdminRBACAssignments extends ManageRecords
{
    protected static string $resource = AdminRBACAssignmentResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
