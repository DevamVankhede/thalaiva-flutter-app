import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme.dart';
import 'features/menu/menu_screen.dart';
import 'features/cart/cart_screen.dart';
import 'features/order/order_screen.dart';
import 'features/profile/profile_screen.dart';
import 'providers/app_providers.dart';

void main() {
  runApp(const ProviderScope(child: ThalaivaaApp()));
}

class ThalaivaaApp extends ConsumerWidget {
  const ThalaivaaApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);

    return MaterialApp(
      title: 'Thalaivaa - Authentic South Indian Cuisine',
      debugShowCheckedModeBanner: false,
      theme: ThalaivaaTheme.lightTheme,
      darkTheme: ThalaivaaTheme.darkTheme,
      themeMode: themeMode,
      home: const RootNavigationScreen(),
    );
  }
}

class RootNavigationScreen extends ConsumerWidget {
  const RootNavigationScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentIndex = ref.watch(bottomNavIndexProvider);
    final cart = ref.watch(cartProvider);
    final tr = ref.watch(trProvider);

    final screens = const [
      MenuScreen(),
      CartScreen(),
      OrderScreen(),
      ProfileScreen(),
    ];

    return Scaffold(
      body: IndexedStack(
        index: currentIndex,
        children: screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: currentIndex,
        onDestinationSelected: (idx) => ref.read(bottomNavIndexProvider.notifier).state = idx,
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.restaurant_rounded),
            selectedIcon: const Icon(Icons.restaurant_rounded, color: ThalaivaaTheme.brandAmber),
            label: tr('all'),
          ),
          NavigationDestination(
            icon: Badge(
              isLabelVisible: cart.totalItemCount > 0,
              label: Text('${cart.totalItemCount}'),
              child: const Icon(Icons.shopping_bag_outlined),
            ),
            selectedIcon: Badge(
              isLabelVisible: cart.totalItemCount > 0,
              label: Text('${cart.totalItemCount}'),
              child: const Icon(Icons.shopping_bag_rounded, color: ThalaivaaTheme.brandAmber),
            ),
            label: tr('cart'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.delivery_dining_outlined),
            selectedIcon: const Icon(Icons.delivery_dining_rounded, color: ThalaivaaTheme.brandAmber),
            label: tr('order'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.person_outline_rounded),
            selectedIcon: const Icon(Icons.person_rounded, color: ThalaivaaTheme.brandAmber),
            label: tr('profile'),
          ),
        ],
      ),
    );
  }
}
