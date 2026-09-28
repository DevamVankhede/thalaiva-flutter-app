<?php
// REAL-TIME: Livewire 3 + Soketi reference for Thalaivaa Filament Admin
// Note: vendor/filament NOT present; Soketi server configured externally via env variables.
// Environment reference: SOKETI_APP_ID, SOKETI_APP_KEY, SOKETI_HOST, SOKETI_PORT=6001
// Livewire 3 real-time updates for admin order status: $pollingInterval or Soketi push.
// References: https://laravel-livewire.com/docs/3/quickstart
// https://docs.soketi.app/
// No soketi_channels DB table (excluded per master plan item #17).
// Admin actions tracked in order_status_logs (changed_by = admin id, changed_by_type='admin').
