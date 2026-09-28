<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    $simPath = public_path('simulator.html');
    if (file_exists($simPath)) {
        return response()->file($simPath);
    }
    return response()->json([
        'app' => 'Thalaivaa API',
        'status' => 'online',
        'version' => '1.0.0',
    ]);
});

Route::get('/preview', function () {
    $previewPath = public_path('preview.html');
    if (file_exists($previewPath)) {
        return response()->file($previewPath);
    }
    return redirect('/');
});

Route::get('/simulator', function () {
    $simPath = public_path('simulator.html');
    if (file_exists($simPath)) {
        return response()->file($simPath);
    }
    return redirect('/');
});

Route::get('/flutter_web', function () {
    $flutterPath = public_path('flutter_web/index.html');
    if (file_exists($flutterPath)) {
        return response()->file($flutterPath);
    }
    return redirect('/');
});

Route::get('/health', function () {
    return response()->json([
        'app' => 'Thalaivaa API',
        'status' => 'online',
        'version' => '1.0.0',
    ]);
});
