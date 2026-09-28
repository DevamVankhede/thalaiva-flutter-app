# Build updated UI screens for Menu, Cart, Order, Profile, and Main Navigation
import os

# 1. Main.dart
MAIN_DART_CODE = r'''import 'package:flutter/material.dart';
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
            label: tr('navMenu'),
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
            label: tr('navCart'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.delivery_dining_outlined),
            selectedIcon: const Icon(Icons.delivery_dining_rounded, color: ThalaivaaTheme.brandAmber),
            label: tr('navOrders'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.person_outline_rounded),
            selectedIcon: const Icon(Icons.person_rounded, color: ThalaivaaTheme.brandAmber),
            label: tr('navProfile'),
          ),
        ],
      ),
    );
  }
}
'''

# 2. MenuScreen.dart
MENU_SCREEN_CODE = r'''import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../models/models.dart';
import '../../providers/app_providers.dart';

class MenuScreen extends ConsumerStatefulWidget {
  const MenuScreen({super.key});

  @override
  ConsumerState<MenuScreen> createState() => _MenuScreenState();
}

class _MenuScreenState extends ConsumerState<MenuScreen> {
  final TextEditingController _searchController = TextEditingController();

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _openCustomizer(Product product) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => ProductCustomizerSheet(product: product),
    );
  }

  void _openLanguagePicker(BuildContext context, WidgetRef ref) {
    final tr = ref.read(trProvider);
    final currentLang = ref.read(languageProvider);

    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        final isDark = Theme.of(ctx).brightness == Brightness.dark;
        return Container(
          decoration: BoxDecoration(
            color: isDark ? ThalaivaaTheme.surfaceCard : Colors.white,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
          ),
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    tr('language'),
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: [
                  {'code': 'en', 'label': 'English'},
                  {'code': 'hi', 'label': 'हिन्दी (Hindi)'},
                  {'code': 'gu', 'label': 'ગુજરાતી (Gujarati)'},
                  {'code': 'ta', 'label': 'தமிழ் (Tamil)'},
                ].map((item) {
                  final isSel = currentLang == item['code'];
                  return ChoiceChip(
                    label: Text(item['label']!, style: const TextStyle(fontWeight: FontWeight.bold)),
                    selected: isSel,
                    selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                    checkmarkColor: ThalaivaaTheme.brandAmber,
                    onSelected: (_) {
                      ref.read(languageProvider.notifier).state = item['code']!;
                      Navigator.pop(ctx);
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 16),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final products = ref.watch(filteredProductsProvider);
    final categories = ref.watch(availableCategoriesProvider);
    final selectedCategory = ref.watch(selectedCategoryProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final dietary = ref.watch(dietaryFilterProvider);
    final bestsellerOnly = ref.watch(bestsellerOnlyProvider);
    final sort = ref.watch(sortByProvider);
    final cart = ref.watch(cartProvider);
    final currentLang = ref.watch(languageProvider);
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [ThalaivaaTheme.brandAmber, ThalaivaaTheme.primaryDeep],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.3),
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: const Icon(Icons.restaurant_menu_rounded, color: Colors.white, size: 18),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    tr('appName'),
                    style: TextStyle(
                      fontWeight: FontWeight.w900,
                      fontSize: 16,
                      letterSpacing: 0.8,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                  Row(
                    children: [
                      const Icon(Icons.location_on_rounded, size: 12, color: ThalaivaaTheme.brandAmber),
                      const SizedBox(width: 3),
                      Flexible(
                        child: Text(
                          selectedBranch.name,
                          style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.w600),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      const SizedBox(width: 6),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
                        decoration: BoxDecoration(
                          color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          selectedBranch.deliveryTime,
                          style: const TextStyle(fontSize: 9, color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            // Quick 1-Tap Language Switcher
            InkWell(
              onTap: () => _openLanguagePicker(context, ref),
              borderRadius: BorderRadius.circular(20),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.3)),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.translate_rounded, size: 14, color: ThalaivaaTheme.brandAmber),
                    const SizedBox(width: 4),
                    Text(
                      currentLang.toUpperCase(),
                      style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: ThalaivaaTheme.brandAmber),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
      body: Stack(
        children: [
          Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 1080),
              child: CustomScrollView(
                slivers: [
                  // 1. Search Bar Header
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(16, 12, 16, 6),
                      child: Container(
                        decoration: BoxDecoration(
                          color: cardBg,
                          borderRadius: BorderRadius.circular(14),
                          border: Border.all(color: cardBorder),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withValues(alpha: isDark ? 0.2 : 0.03),
                              blurRadius: 10,
                              offset: const Offset(0, 3),
                            ),
                          ],
                        ),
                        child: TextField(
                          controller: _searchController,
                          onChanged: (val) => ref.read(searchQueryProvider.notifier).state = val,
                          decoration: InputDecoration(
                            hintText: tr('searchHint'),
                            hintStyle: TextStyle(fontSize: 13, color: isDark ? Colors.white38 : const Color(0xFF94A3B8)),
                            prefixIcon: const Icon(Icons.search_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                            suffixIcon: _searchController.text.isNotEmpty
                                ? IconButton(
                                    icon: const Icon(Icons.clear_rounded, size: 18),
                                    onPressed: () {
                                      _searchController.clear();
                                      ref.read(searchQueryProvider.notifier).state = '';
                                    },
                                  )
                                : null,
                            border: InputBorder.none,
                            contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                          ),
                        ),
                      ),
                    ),
                  ),

                  // 2. Promotional Special Banner
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(16, 6, 16, 8),
                      child: Container(
                        padding: const EdgeInsets.all(14),
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: isDark
                                ? [const Color(0xFF1E1B4B), const Color(0xFF311042)]
                                : [const Color(0xFFFFF7ED), const Color(0xFFFFEDD5)],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: ThalaivaaTheme.brandAmber.withValues(alpha: isDark ? 0.3 : 0.4),
                          ),
                        ),
                        child: Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(10),
                              decoration: BoxDecoration(
                                color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                                shape: BoxShape.circle,
                              ),
                              child: const Text('🔥', style: TextStyle(fontSize: 22)),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    tr('promo_title'),
                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                                  ),
                                  const SizedBox(height: 2),
                                  Text(
                                    tr('promo_sub'),
                                    style: TextStyle(
                                      fontSize: 11,
                                      fontWeight: FontWeight.w600,
                                      color: isDark ? const Color(0xFFFFB800) : const Color(0xFFC2410C),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),

                  // 3. Quick Multi-Dimension Filter Bar (Pure Veg, Bestsellers, Sort)
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
                      child: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          children: [
                            // Pure Veg Toggle
                            FilterChip(
                              label: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Container(
                                    width: 12,
                                    height: 12,
                                    decoration: BoxDecoration(
                                      border: Border.all(color: ThalaivaaTheme.vegGreen, width: 1.5),
                                      borderRadius: BorderRadius.circular(3),
                                    ),
                                    child: Center(
                                      child: Container(
                                        width: 5,
                                        height: 5,
                                        decoration: const BoxDecoration(color: ThalaivaaTheme.vegGreen, shape: BoxShape.circle),
                                      ),
                                    ),
                                  ),
                                  const SizedBox(width: 6),
                                  Text(tr('pureVeg'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                                ],
                              ),
                              selected: dietary == DietaryFilter.vegOnly,
                              selectedColor: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                              checkmarkColor: ThalaivaaTheme.vegGreen,
                              onSelected: (selected) {
                                ref.read(dietaryFilterProvider.notifier).state =
                                    selected ? DietaryFilter.vegOnly : DietaryFilter.all;
                              },
                            ),
                            const SizedBox(width: 8),

                            // Bestsellers Filter
                            FilterChip(
                              label: Text(tr('bestsellers'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                              selected: bestsellerOnly,
                              selectedColor: ThalaivaaTheme.goldAccent.withValues(alpha: 0.2),
                              checkmarkColor: ThalaivaaTheme.goldAccent,
                              onSelected: (selected) {
                                ref.read(bestsellerOnlyProvider.notifier).state = selected;
                              },
                            ),
                            const SizedBox(width: 8),

                            // Sort Dropdown
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 2),
                              decoration: BoxDecoration(
                                color: cardBg,
                                borderRadius: BorderRadius.circular(20),
                                border: Border.all(color: cardBorder),
                              ),
                              child: DropdownButtonHideUnderline(
                                child: DropdownButton<SortOption>(
                                  value: sort,
                                  isDense: true,
                                  icon: const Icon(Icons.sort_rounded, size: 16, color: ThalaivaaTheme.brandAmber),
                                  items: [
                                    DropdownMenuItem(value: SortOption.recommended, child: Text(tr('sort_rec'), style: const TextStyle(fontSize: 12))),
                                    DropdownMenuItem(value: SortOption.rating, child: Text(tr('sort_rating'), style: const TextStyle(fontSize: 12))),
                                    DropdownMenuItem(value: SortOption.priceLowToHigh, child: Text(tr('sort_price_low'), style: const TextStyle(fontSize: 12))),
                                    DropdownMenuItem(value: SortOption.priceHighToLow, child: Text(tr('sort_price_high'), style: const TextStyle(fontSize: 12))),
                                  ],
                                  onChanged: (val) {
                                    if (val != null) ref.read(sortByProvider.notifier).state = val;
                                  },
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),

                  // 4. Interactive Category Filter Pills (MATCHING EXACT SLUGS WITH LOCALIZATION)
                  SliverToBoxAdapter(
                    child: SizedBox(
                      height: 44,
                      child: ListView.separated(
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        scrollDirection: Axis.horizontal,
                        itemCount: categories.length,
                        separatorBuilder: (_, __) => const SizedBox(width: 8),
                        itemBuilder: (ctx, idx) {
                          final cat = categories[idx];
                          final isSelected = selectedCategory == cat;
                          final count = ref.watch(categoryCountProvider(cat));
                          final localizedCat = tr('cat_$cat');

                          return InkWell(
                            onTap: () {
                              ref.read(selectedCategoryProvider.notifier).state = cat;
                            },
                            borderRadius: BorderRadius.circular(22),
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 200),
                              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                              decoration: BoxDecoration(
                                color: isSelected
                                    ? ThalaivaaTheme.brandAmber
                                    : (isDark ? ThalaivaaTheme.surfaceCard : Colors.white),
                                borderRadius: BorderRadius.circular(22),
                                border: Border.all(
                                  color: isSelected
                                      ? ThalaivaaTheme.brandAmber
                                      : (isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0)),
                                ),
                                boxShadow: isSelected
                                    ? [
                                        BoxShadow(
                                          color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.35),
                                          blurRadius: 8,
                                          offset: const Offset(0, 2),
                                        ),
                                      ]
                                    : null,
                              ),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Text(
                                    localizedCat.isNotEmpty ? localizedCat : cat,
                                    style: TextStyle(
                                      color: isSelected ? Colors.white : (isDark ? Colors.white70 : const Color(0xFF475569)),
                                      fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                                      fontSize: 12,
                                    ),
                                  ),
                                  const SizedBox(width: 6),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                                    decoration: BoxDecoration(
                                      color: isSelected
                                          ? Colors.white.withValues(alpha: 0.25)
                                          : (isDark ? Colors.white10 : const Color(0xFFF1F5F9)),
                                      borderRadius: BorderRadius.circular(10),
                                    ),
                                    child: Text(
                                      '$count',
                                      style: TextStyle(
                                        color: isSelected ? Colors.white : const Color(0xFF64748B),
                                        fontSize: 10,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                  ),

                  const SliverToBoxAdapter(child: SizedBox(height: 12)),

                  // 5. Products List
                  if (products.isEmpty)
                    SliverFillRemaining(
                      hasScrollBody: false,
                      child: Center(
                        child: Padding(
                          padding: const EdgeInsets.all(32),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.search_off_rounded, size: 48, color: Colors.grey),
                              const SizedBox(height: 12),
                              Text(
                                'No authentic dishes found',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 15,
                                  color: isDark ? Colors.white70 : Colors.black87,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Try clearing filters or changing category search.',
                                textAlign: TextAlign.center,
                                style: TextStyle(fontSize: 12, color: isDark ? Colors.white38 : Colors.grey),
                              ),
                            ],
                          ),
                        ),
                      ),
                    )
                  else
                    SliverPadding(
                      padding: const EdgeInsets.fromLTRB(16, 0, 16, 100),
                      sliver: SliverList(
                        delegate: SliverChildBuilderDelegate(
                          (ctx, idx) {
                            final product = products[idx];
                            final qty = ref.watch(cartProvider.notifier).getProductQuantity(product.id);
                            final localizedInfo = ref.watch(localizedDishInfoProvider(product));

                            return Container(
                              margin: const EdgeInsets.only(bottom: 12),
                              padding: const EdgeInsets.all(14),
                              decoration: BoxDecoration(
                                color: cardBg,
                                borderRadius: BorderRadius.circular(18),
                                border: Border.all(color: cardBorder),
                                boxShadow: [
                                  BoxShadow(
                                    color: Colors.black.withValues(alpha: isDark ? 0.2 : 0.03),
                                    blurRadius: 10,
                                    offset: const Offset(0, 3),
                                  ),
                                ],
                              ),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  // Details Column
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          children: [
                                            // Veg FSSAI badge
                                            Container(
                                              width: 14,
                                              height: 14,
                                              decoration: BoxDecoration(
                                                border: Border.all(color: ThalaivaaTheme.vegGreen, width: 1.5),
                                                borderRadius: BorderRadius.circular(3),
                                              ),
                                              child: Center(
                                                child: Container(
                                                  width: 6,
                                                  height: 6,
                                                  decoration: const BoxDecoration(
                                                    color: ThalaivaaTheme.vegGreen,
                                                    shape: BoxShape.circle,
                                                  ),
                                                ),
                                              ),
                                            ),
                                            if (product.isBestseller) ...[
                                              const SizedBox(width: 6),
                                              Container(
                                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                                decoration: BoxDecoration(
                                                  color: ThalaivaaTheme.goldAccent.withValues(alpha: 0.15),
                                                  borderRadius: BorderRadius.circular(4),
                                                ),
                                                child: const Text(
                                                  '★ MUST TRY',
                                                  style: TextStyle(
                                                    fontSize: 9,
                                                    fontWeight: FontWeight.w800,
                                                    color: Color(0xFFD97706),
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ],
                                        ),
                                        const SizedBox(height: 6),
                                        Text(
                                          localizedInfo.name,
                                          style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 14,
                                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                                          ),
                                        ),
                                        const SizedBox(height: 4),
                                        Text(
                                          localizedInfo.description,
                                          style: TextStyle(
                                            fontSize: 11,
                                            color: isDark ? Colors.white54 : const Color(0xFF64748B),
                                            height: 1.3,
                                          ),
                                          maxLines: 2,
                                          overflow: TextOverflow.ellipsis,
                                        ),
                                        const SizedBox(height: 8),
                                        Row(
                                          children: [
                                            Text(
                                              ThalaivaaTheme.formatInr(product.price),
                                              style: const TextStyle(
                                                fontWeight: FontWeight.w900,
                                                fontSize: 15,
                                                color: ThalaivaaTheme.brandAmber,
                                              ),
                                            ),
                                            const SizedBox(width: 8),
                                            Text(
                                              '★ ${product.rating}',
                                              style: TextStyle(
                                                fontSize: 11,
                                                fontWeight: FontWeight.bold,
                                                color: isDark ? Colors.white38 : Colors.grey,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                  const SizedBox(width: 14),

                                  // Visual & Add Stepper
                                  Column(
                                    children: [
                                      Container(
                                        width: 80,
                                        height: 80,
                                        decoration: BoxDecoration(
                                          color: isDark ? const Color(0xFF161E2E) : const Color(0xFFFFF7ED),
                                          borderRadius: BorderRadius.circular(16),
                                          border: Border.all(
                                            color: isDark ? ThalaivaaTheme.borderDark : const Color(0xFFFFEDD5),
                                          ),
                                        ),
                                        child: Center(
                                          child: Text(
                                            product.iconEmoji,
                                            style: const TextStyle(fontSize: 40),
                                          ),
                                        ),
                                      ),
                                      const SizedBox(height: 8),
                                      if (qty == 0)
                                        SizedBox(
                                          width: 80,
                                          height: 32,
                                          child: ElevatedButton(
                                            onPressed: () {
                                              if (product.modifierGroups.isNotEmpty) {
                                                _openCustomizer(product);
                                              } else {
                                                ref.read(cartProvider.notifier).addItem(product);
                                              }
                                            },
                                            style: ElevatedButton.styleFrom(
                                              backgroundColor: ThalaivaaTheme.brandAmber,
                                              foregroundColor: Colors.white,
                                              padding: EdgeInsets.zero,
                                              elevation: 1,
                                              shape: RoundedRectangleBorder(
                                                borderRadius: BorderRadius.circular(8),
                                              ),
                                            ),
                                            child: Text(
                                              tr('add'),
                                              style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 11),
                                            ),
                                          ),
                                        )
                                      else
                                        Container(
                                          height: 32,
                                          decoration: BoxDecoration(
                                            color: ThalaivaaTheme.brandAmber,
                                            borderRadius: BorderRadius.circular(8),
                                          ),
                                          child: Row(
                                            mainAxisSize: MainAxisSize.min,
                                            children: [
                                              IconButton(
                                                padding: EdgeInsets.zero,
                                                constraints: const BoxConstraints(minWidth: 28, minHeight: 32),
                                                icon: const Icon(Icons.remove, size: 14, color: Colors.white),
                                                onPressed: () => ref.read(cartProvider.notifier).removeOne(product),
                                              ),
                                              Text(
                                                '$qty',
                                                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                                              ),
                                              IconButton(
                                                padding: EdgeInsets.zero,
                                                constraints: const BoxConstraints(minWidth: 28, minHeight: 32),
                                                icon: const Icon(Icons.add, size: 14, color: Colors.white),
                                                onPressed: () => ref.read(cartProvider.notifier).addItem(product),
                                              ),
                                            ],
                                          ),
                                        ),
                                    ],
                                  ),
                                ],
                              ),
                            );
                          },
                          childCount: products.length,
                        ),
                      ),
                    ),
                ],
              ),
            ),
          ),

          // Floating Quick Cart Tray
          if (cart.totalItemCount > 0)
            Positioned(
              bottom: 16,
              left: 16,
              right: 16,
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 600),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFF0F172A), Color(0xFF1E293B)],
                      ),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.4)),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.4),
                          blurRadius: 16,
                          offset: const Offset(0, 6),
                        ),
                      ],
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: ThalaivaaTheme.brandAmber,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                '${cart.totalItemCount} ITEMS',
                                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 10),
                              ),
                            ),
                            const SizedBox(width: 10),
                            Text(
                              ThalaivaaTheme.formatInr(cart.grandTotal),
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 14),
                            ),
                          ],
                        ),
                        TextButton(
                          onPressed: () {
                            ref.read(bottomNavIndexProvider.notifier).state = 1; // Switch to Cart tab
                          },
                          style: TextButton.styleFrom(
                            foregroundColor: ThalaivaaTheme.brandAmber,
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          ),
                          child: Row(
                            children: [
                              Text(tr('navCart'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                              const SizedBox(width: 4),
                              const Icon(Icons.arrow_forward_rounded, size: 14),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}

class ProductCustomizerSheet extends ConsumerStatefulWidget {
  final Product product;
  const ProductCustomizerSheet({super.key, required this.product});

  @override
  ConsumerState<ProductCustomizerSheet> createState() => _ProductCustomizerSheetState();
}

class _ProductCustomizerSheetState extends ConsumerState<ProductCustomizerSheet> {
  final List<ModifierOption> _selectedOptions = [];

  @override
  Widget build(BuildContext context) {
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final localizedInfo = ref.watch(localizedDishInfoProvider(widget.product));

    double extraPrice = _selectedOptions.fold(0.0, (sum, o) => sum + o.price);
    double totalPrice = widget.product.price + extraPrice;

    return Container(
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      padding: const EdgeInsets.all(20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                localizedInfo.name,
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              IconButton(
                icon: const Icon(Icons.close),
                onPressed: () => Navigator.pop(context),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ...widget.product.modifierGroups.map((group) {
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  group.title,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: ThalaivaaTheme.brandAmber),
                ),
                const SizedBox(height: 6),
                ...group.options.map((opt) {
                  final isSel = _selectedOptions.any((o) => o.id == opt.id);
                  return CheckboxListTile(
                    dense: true,
                    title: Text(opt.name, style: const TextStyle(fontSize: 13)),
                    subtitle: Text('+${ThalaivaaTheme.formatInr(opt.price)}', style: const TextStyle(fontSize: 11)),
                    value: isSel,
                    activeColor: ThalaivaaTheme.brandAmber,
                    onChanged: (val) {
                      setState(() {
                        if (val == true) {
                          _selectedOptions.add(opt);
                        } else {
                          _selectedOptions.removeWhere((o) => o.id == opt.id);
                        }
                      });
                    },
                  );
                }).toList(),
              ],
            );
          }).toList(),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () {
              ref.read(cartProvider.notifier).addItem(widget.product, selectedModifiers: _selectedOptions);
              Navigator.pop(context);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: ThalaivaaTheme.brandAmber,
              foregroundColor: Colors.white,
              minimumSize: const Size.fromHeight(48),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            child: Text(
              '${tr('addToTray')} • ${ThalaivaaTheme.formatInr(totalPrice)}',
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
            ),
          ),
        ],
      ),
    );
  }
}
'''

# 3. CartScreen.dart (Full Delivery Suite)
CART_SCREEN_CODE = r'''import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../providers/app_providers.dart';

class CartScreen extends ConsumerStatefulWidget {
  const CartScreen({super.key});

  @override
  ConsumerState<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends ConsumerState<CartScreen> {
  final TextEditingController _couponController = TextEditingController();

  @override
  void dispose() {
    _couponController.dispose();
    super.dispose();
  }

  void _openAddressPicker(BuildContext context, WidgetRef ref) {
    final tr = ref.read(trProvider);
    final addresses = ref.read(savedAddressesProvider);
    final selectedAddr = ref.read(selectedAddressProvider);

    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        final isDark = Theme.of(ctx).brightness == Brightness.dark;
        return Container(
          decoration: BoxDecoration(
            color: isDark ? ThalaivaaTheme.surfaceCard : Colors.white,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
          ),
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    tr('deliveryAddress'),
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              ...addresses.map((addr) {
                final isSel = selectedAddr.id == addr.id;
                return Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  decoration: BoxDecoration(
                    color: isSel ? ThalaivaaTheme.brandAmber.withValues(alpha: 0.1) : null,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: isSel ? ThalaivaaTheme.brandAmber : (isDark ? Colors.white10 : const Color(0xFFE2E8F0)),
                    ),
                  ),
                  child: ListTile(
                    leading: Icon(
                      addr.label == 'Home' ? Icons.home_rounded : (addr.label == 'Work' ? Icons.business_rounded : Icons.place_rounded),
                      color: isSel ? ThalaivaaTheme.brandAmber : Colors.grey,
                    ),
                    title: Text(addr.label, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    subtitle: Text('${addr.addressLine} • ${addr.landmark}', style: const TextStyle(fontSize: 11)),
                    trailing: isSel ? const Icon(Icons.check_circle_rounded, color: ThalaivaaTheme.brandAmber, size: 20) : null,
                    onTap: () {
                      ref.read(selectedAddressProvider.notifier).state = addr;
                      Navigator.pop(ctx);
                    },
                  ),
                );
              }).toList(),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final cart = ref.watch(cartProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final selectedAddress = ref.watch(selectedAddressProvider);
    final orderType = cart.orderType;
    final selectedInstructions = ref.watch(deliveryInstructionsProvider);
    final contactless = ref.watch(contactlessDeliveryProvider);
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    if (cart.items.isEmpty) {
      return Scaffold(
        backgroundColor: bg,
        appBar: AppBar(
          title: Text(tr('navCart'), style: const TextStyle(fontWeight: FontWeight.bold)),
          elevation: 0,
          backgroundColor: cardBg,
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('🛒', style: TextStyle(fontSize: 64)),
              const SizedBox(height: 16),
              Text(
                'Your Food Tray is Empty',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: isDark ? Colors.white : Colors.black87),
              ),
              const SizedBox(height: 6),
              Text(
                'Explore authentic South Indian Dosas & Filter Kaapi',
                style: TextStyle(fontSize: 12, color: isDark ? Colors.white54 : Colors.grey),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () => ref.read(bottomNavIndexProvider.notifier).state = 0,
                style: ElevatedButton.styleFrom(
                  backgroundColor: ThalaivaaTheme.brandAmber,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: Text(tr('browseMenu')),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        title: Text(tr('navCart'), style: const TextStyle(fontWeight: FontWeight.bold)),
        elevation: 0,
        backgroundColor: cardBg,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 40),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // 1. Order Type Switcher (Delivery / Takeaway / Dine-in)
                Container(
                  padding: const EdgeInsets.all(4),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: InkWell(
                          onTap: () => ref.read(cartProvider.notifier).setOrderType(OrderType.delivery),
                          borderRadius: BorderRadius.circular(10),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 8),
                            decoration: BoxDecoration(
                              color: orderType == OrderType.delivery ? ThalaivaaTheme.brandAmber : Colors.transparent,
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: Center(
                              child: Text(
                                tr('orderType_delivery'),
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                  color: orderType == OrderType.delivery ? Colors.white : (isDark ? Colors.white70 : Colors.black87),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                      Expanded(
                        child: InkWell(
                          onTap: () => ref.read(cartProvider.notifier).setOrderType(OrderType.takeaway),
                          borderRadius: BorderRadius.circular(10),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 8),
                            decoration: BoxDecoration(
                              color: orderType == OrderType.takeaway ? ThalaivaaTheme.brandAmber : Colors.transparent,
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: Center(
                              child: Text(
                                tr('orderType_takeaway'),
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                  color: orderType == OrderType.takeaway ? Colors.white : (isDark ? Colors.white70 : Colors.black87),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                      Expanded(
                        child: InkWell(
                          onTap: () => ref.read(cartProvider.notifier).setOrderType(OrderType.dineIn),
                          borderRadius: BorderRadius.circular(10),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 8),
                            decoration: BoxDecoration(
                              color: orderType == OrderType.dineIn ? ThalaivaaTheme.brandAmber : Colors.transparent,
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: Center(
                              child: Text(
                                tr('orderType_dineIn'),
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                  color: orderType == OrderType.dineIn ? Colors.white : (isDark ? Colors.white70 : Colors.black87),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 14),

                // 2. Delivery Address Card
                if (orderType == OrderType.delivery)
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: cardBg,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: cardBorder),
                    ),
                    child: Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.location_on_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Text(
                                    '${tr('deliverTo')} ${selectedAddress.label}',
                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                                  ),
                                  const SizedBox(width: 6),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
                                    decoration: BoxDecoration(
                                      color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: const Text('20-25 min', style: TextStyle(color: ThalaivaaTheme.vegGreen, fontSize: 9, fontWeight: FontWeight.bold)),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 2),
                              Text(
                                '${selectedAddress.addressLine}, Surat',
                                style: TextStyle(fontSize: 11, color: isDark ? Colors.white54 : const Color(0xFF64748B)),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ],
                          ),
                        ),
                        TextButton(
                          onPressed: () => _openAddressPicker(context, ref),
                          style: TextButton.styleFrom(foregroundColor: ThalaivaaTheme.brandAmber),
                          child: Text(tr('change'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11)),
                        ),
                      ],
                    ),
                  ),

                const SizedBox(height: 14),

                // 3. Free Delivery Threshold Meter
                if (orderType == OrderType.delivery)
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: cart.subtotal >= 499
                          ? ThalaivaaTheme.vegGreen.withValues(alpha: 0.15)
                          : ThalaivaaTheme.brandAmber.withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          cart.subtotal >= 499 ? Icons.check_circle_rounded : Icons.local_shipping_rounded,
                          color: cart.subtotal >= 499 ? ThalaivaaTheme.vegGreen : ThalaivaaTheme.brandAmber,
                          size: 18,
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Text(
                            cart.subtotal >= 499
                                ? '🎉 ${tr('free_delivery_above')}'
                                : '${tr('free_delivery_unlock')} (₹${(499 - cart.subtotal).toInt()} more)',
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: cart.subtotal >= 499 ? ThalaivaaTheme.vegGreen : ThalaivaaTheme.brandAmber,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),

                const SizedBox(height: 14),

                // 4. Cart Items List
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Column(
                    children: cart.items.map((item) {
                      final localizedInfo = ref.watch(localizedDishInfoProvider(item.product));
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 8),
                        child: Row(
                          children: [
                            Text(item.product.iconEmoji, style: const TextStyle(fontSize: 24)),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    localizedInfo.name,
                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                                  ),
                                  if (item.selectedModifiers.isNotEmpty)
                                    Text(
                                      item.selectedModifiers.map((m) => m.name).join(', '),
                                      style: TextStyle(fontSize: 10, color: isDark ? Colors.white54 : Colors.grey),
                                    ),
                                  Text(
                                    ThalaivaaTheme.formatInr(item.totalPrice),
                                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: ThalaivaaTheme.brandAmber),
                                  ),
                                ],
                              ),
                            ),
                            Container(
                              height: 30,
                              decoration: BoxDecoration(
                                color: ThalaivaaTheme.brandAmber,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  IconButton(
                                    padding: EdgeInsets.zero,
                                    constraints: const BoxConstraints(minWidth: 26, minHeight: 30),
                                    icon: const Icon(Icons.remove, size: 12, color: Colors.white),
                                    onPressed: () => ref.read(cartProvider.notifier).removeOne(item.product),
                                  ),
                                  Text('${item.quantity}', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 11)),
                                  IconButton(
                                    padding: EdgeInsets.zero,
                                    constraints: const BoxConstraints(minWidth: 26, minHeight: 30),
                                    icon: const Icon(Icons.add, size: 12, color: Colors.white),
                                    onPressed: () => ref.read(cartProvider.notifier).addItem(item.product),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      );
                    }).toList(),
                  ),
                ),

                const SizedBox(height: 14),

                // 5. Delivery Instructions & Contactless Toggle
                if (orderType == OrderType.delivery)
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: cardBg,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: cardBorder),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(tr('deliveryInstructions'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: [
                            {'key': 'leave_door', 'label': tr('instr_leave_door')},
                            {'key': 'no_bell', 'label': tr('instr_no_bell')},
                            {'key': 'avoid_call', 'label': tr('instr_avoid_call')},
                            {'key': 'pet', 'label': tr('instr_pet')},
                          ].map((instr) {
                            final isSel = selectedInstructions.contains(instr['key']);
                            return FilterChip(
                              label: Text(instr['label']!, style: const TextStyle(fontSize: 11)),
                              selected: isSel,
                              selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                              checkmarkColor: ThalaivaaTheme.brandAmber,
                              onSelected: (val) {
                                final set = Set<String>.from(selectedInstructions);
                                if (val) {
                                  set.add(instr['key']!);
                                } else {
                                  set.remove(instr['key']!);
                                }
                                ref.read(deliveryInstructionsProvider.notifier).state = set;
                              },
                            );
                          }).toList(),
                        ),
                        const Divider(height: 20),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(tr('contactless'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                                Text(tr('contactless_desc'), style: TextStyle(fontSize: 10, color: isDark ? Colors.white54 : Colors.grey)),
                              ],
                            ),
                            Switch(
                              value: contactless,
                              activeColor: ThalaivaaTheme.brandAmber,
                              onChanged: (val) => ref.read(contactlessDeliveryProvider.notifier).state = val,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                const SizedBox(height: 14),

                // 6. Delivery Partner Tip Selector
                if (orderType == OrderType.delivery)
                  Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: cardBg,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: cardBorder),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(tr('tipTitle'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                        const SizedBox(height: 3),
                        Text(tr('tipSubtitle'), style: TextStyle(fontSize: 11, color: isDark ? Colors.white54 : Colors.grey)),
                        const SizedBox(height: 10),
                        Row(
                          children: [0.0, 20.0, 30.0, 50.0, 100.0].map((tip) {
                            final isSel = cart.tipAmount == tip;
                            return Padding(
                              padding: const EdgeInsets.only(right: 8),
                              child: ChoiceChip(
                                label: Text(tip == 0.0 ? tr('noTip') : '₹${tip.toInt()}'),
                                selected: isSel,
                                selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                                checkmarkColor: ThalaivaaTheme.brandAmber,
                                onSelected: (_) => ref.read(cartProvider.notifier).setTip(tip),
                              ),
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),

                const SizedBox(height: 14),

                // 7. Coupon Card
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: cardBorder),
                  ),
                  child: cart.appliedCoupon != null
                      ? Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Row(
                              children: [
                                const Icon(Icons.discount_rounded, color: ThalaivaaTheme.vegGreen, size: 20),
                                const SizedBox(width: 8),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(cart.appliedCoupon!.code, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                                    Text(cart.appliedCoupon!.description, style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.vegGreen)),
                                  ],
                                ),
                              ],
                            ),
                            TextButton(
                              onPressed: () => ref.read(cartProvider.notifier).removeCoupon(),
                              child: Text(tr('remove'), style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold)),
                            ),
                          ],
                        )
                      : Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: _couponController,
                                textCapitalization: TextCapitalization.characters,
                                decoration: InputDecoration(
                                  hintText: 'THALAIVAA50 / FEAST100',
                                  hintStyle: TextStyle(fontSize: 12, color: isDark ? Colors.white30 : Colors.grey),
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                                  contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                                  isDense: true,
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
                            ElevatedButton(
                              onPressed: () {
                                final ok = ref.read(cartProvider.notifier).applyCoupon(_couponController.text);
                                if (!ok) {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(content: Text('Invalid coupon. Try THALAIVAA50 or FEAST100')),
                                  );
                                }
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: ThalaivaaTheme.brandAmber,
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                              ),
                              child: Text(tr('apply'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                            ),
                          ],
                        ),
                ),

                const SizedBox(height: 14),

                // 8. Bill Breakdown
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(tr('billDetails'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      const SizedBox(height: 12),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(tr('subtotal'), style: const TextStyle(fontSize: 13)),
                          Text(ThalaivaaTheme.formatInr(cart.subtotal), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(tr('gst'), style: const TextStyle(fontSize: 13)),
                          Text(ThalaivaaTheme.formatInr(cart.tax), style: const TextStyle(fontSize: 13)),
                        ],
                      ),
                      if (orderType == OrderType.delivery) ...[
                        const SizedBox(height: 6),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(tr('deliveryFee'), style: const TextStyle(fontSize: 13)),
                            Text(
                              cart.deliveryFee == 0 ? tr('free') : ThalaivaaTheme.formatInr(cart.deliveryFee),
                              style: TextStyle(
                                fontSize: 13,
                                color: cart.deliveryFee == 0 ? ThalaivaaTheme.vegGreen : null,
                                fontWeight: cart.deliveryFee == 0 ? FontWeight.bold : FontWeight.normal,
                              ),
                            ),
                          ],
                        ),
                      ],
                      if (cart.tipAmount > 0) ...[
                        const SizedBox(height: 6),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(tr('deliveryTip'), style: const TextStyle(fontSize: 13)),
                            Text(ThalaivaaTheme.formatInr(cart.tipAmount), style: const TextStyle(fontSize: 13)),
                          ],
                        ),
                      ],
                      if (cart.discountAmount > 0) ...[
                        const SizedBox(height: 6),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(tr('discount'), style: const TextStyle(fontSize: 13, color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold)),
                            Text('-${ThalaivaaTheme.formatInr(cart.discountAmount)}', style: const TextStyle(fontSize: 13, color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold)),
                          ],
                        ),
                      ],
                      const Divider(height: 20),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(tr('grandTotal'), style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
                          Text(
                            ThalaivaaTheme.formatInr(cart.grandTotal),
                            style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 18, color: ThalaivaaTheme.brandAmber),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 20),

                // 9. Place Order CTA
                ElevatedButton(
                  onPressed: () {
                    ref.read(ordersProvider.notifier).placeOrder(cart, selectedBranch, selectedAddress);
                    ref.read(cartProvider.notifier).clearCart();
                    ref.read(liveTrackingStageProvider.notifier).state = LiveTrackingStage.confirmed;
                    ref.read(bottomNavIndexProvider.notifier).state = 2; // Switch to Orders tab
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('🎉 Order Confirmed! Live tracking initiated.'),
                        backgroundColor: ThalaivaaTheme.vegGreen,
                        behavior: SnackBarBehavior.floating,
                      ),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: ThalaivaaTheme.brandAmber,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text('${tr('checkout')} • ', style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15)),
                      Text(
                        ThalaivaaTheme.formatInr(cart.grandTotal),
                        style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 16),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
'''

# 4. OrderScreen.dart (Full Live Delivery Tracking & Simulator)
ORDER_SCREEN_CODE = r'''import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../providers/app_providers.dart';

class OrderScreen extends ConsumerWidget {
  const OrderScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final orders = ref.watch(ordersProvider);
    final stage = ref.watch(liveTrackingStageProvider);
    final eta = ref.watch(etaMinutesProvider);
    final rider = ref.watch(activeRiderProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final selectedAddress = ref.watch(selectedAddressProvider);
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        title: Text(tr('trackingTitle'), style: const TextStyle(fontWeight: FontWeight.bold)),
        elevation: 0,
        backgroundColor: cardBg,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 40),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // 1. ETA Card
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: isDark
                          ? [const Color(0xFF1E1B4B), const Color(0xFF311042)]
                          : [const Color(0xFFFFF7ED), const Color(0xFFFFEDD5)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.4)),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: isDark ? 0.3 : 0.05),
                        blurRadius: 14,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.2),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.delivery_dining_rounded, color: ThalaivaaTheme.vegGreen, size: 28),
                          ),
                          const SizedBox(width: 14),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                tr('estimatedDelivery'),
                                style: TextStyle(fontSize: 11, color: isDark ? Colors.white60 : Colors.black54, fontWeight: FontWeight.w600),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                stage == LiveTrackingStage.delivered ? '🎉 Delivered Hot & Fresh' : '$eta ${tr('mins')}',
                                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900),
                              ),
                            ],
                          ),
                        ],
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.2),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Text(
                          tr('onTime'),
                          style: const TextStyle(color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold, fontSize: 11),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 2. 4-Stage Visual Timeline
                Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Column(
                    children: [
                      _buildTimelineRow(
                        icon: Icons.check_circle_rounded,
                        title: tr('stage_confirmed_title'),
                        subtitle: '${tr('stage_confirmed_sub')} (${selectedBranch.name})',
                        isDone: true,
                        isCurrent: stage == LiveTrackingStage.confirmed,
                        isDark: isDark,
                      ),
                      _buildTimelineDivider(isDone: stage != LiveTrackingStage.confirmed, isDark: isDark),
                      _buildTimelineRow(
                        icon: Icons.soup_kitchen_rounded,
                        title: tr('stage_prep_title'),
                        subtitle: tr('stage_prep_sub'),
                        isDone: stage == LiveTrackingStage.preparing || stage == LiveTrackingStage.onTheWay || stage == LiveTrackingStage.delivered,
                        isCurrent: stage == LiveTrackingStage.preparing,
                        isDark: isDark,
                      ),
                      _buildTimelineDivider(isDone: stage == LiveTrackingStage.onTheWay || stage == LiveTrackingStage.delivered, isDark: isDark),
                      _buildTimelineRow(
                        icon: Icons.two_wheeler_rounded,
                        title: tr('stage_out_title'),
                        subtitle: '${tr('stage_out_sub')} • ${rider.name}',
                        isDone: stage == LiveTrackingStage.onTheWay || stage == LiveTrackingStage.delivered,
                        isCurrent: stage == LiveTrackingStage.onTheWay,
                        isDark: isDark,
                      ),
                      _buildTimelineDivider(isDone: stage == LiveTrackingStage.delivered, isDark: isDark),
                      _buildTimelineRow(
                        icon: Icons.celebration_rounded,
                        title: tr('stage_delivered_title'),
                        subtitle: '${tr('stage_delivered_sub')} (${selectedAddress.addressLine})',
                        isDone: stage == LiveTrackingStage.delivered,
                        isCurrent: stage == LiveTrackingStage.delivered,
                        isDark: isDark,
                        isLast: true,
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 3. Delivery Partner Contact Card
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 24,
                        backgroundColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                        child: Text(rider.photoEmoji, style: const TextStyle(fontSize: 24)),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(rider.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                            const SizedBox(height: 2),
                            Text(
                              '${rider.vehicle} • ★ ${rider.rating}',
                              style: TextStyle(fontSize: 11, color: isDark ? Colors.white60 : Colors.black54),
                            ),
                          ],
                        ),
                      ),
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          IconButton(
                            icon: const Icon(Icons.phone_rounded, color: ThalaivaaTheme.vegGreen),
                            onPressed: () {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text('Calling ${rider.name} at ${rider.phone}...')),
                              );
                            },
                          ),
                          IconButton(
                            icon: const Icon(Icons.chat_bubble_outline_rounded, color: ThalaivaaTheme.brandAmber),
                            onPressed: () {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text('Starting chat with ${rider.name}...')),
                              );
                            },
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 4. Interactive Simulation Control Button
                ElevatedButton.icon(
                  onPressed: () {
                    switch (stage) {
                      case LiveTrackingStage.confirmed:
                        ref.read(liveTrackingStageProvider.notifier).state = LiveTrackingStage.preparing;
                        ref.read(etaMinutesProvider.notifier).state = 14;
                        break;
                      case LiveTrackingStage.preparing:
                        ref.read(liveTrackingStageProvider.notifier).state = LiveTrackingStage.onTheWay;
                        ref.read(etaMinutesProvider.notifier).state = 8;
                        break;
                      case LiveTrackingStage.onTheWay:
                        ref.read(liveTrackingStageProvider.notifier).state = LiveTrackingStage.delivered;
                        ref.read(etaMinutesProvider.notifier).state = 0;
                        break;
                      case LiveTrackingStage.delivered:
                        ref.read(liveTrackingStageProvider.notifier).state = LiveTrackingStage.confirmed;
                        ref.read(etaMinutesProvider.notifier).state = 22;
                        break;
                    }
                  },
                  icon: const Icon(Icons.bolt_rounded),
                  label: Text(tr('simulateAdvance')),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: ThalaivaaTheme.primaryDeep,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  ),
                ),

                const SizedBox(height: 16),

                // 5. Order Items Summary (if active)
                if (orders.isNotEmpty)
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: cardBg,
                      borderRadius: BorderRadius.circular(18),
                      border: Border.all(color: cardBorder),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(tr('orderSummary'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        const SizedBox(height: 10),
                        ...orders.first.items.map((item) {
                          final localizedInfo = ref.watch(localizedDishInfoProvider(item.product));
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text('${item.quantity}x ${localizedInfo.name}', style: const TextStyle(fontSize: 13)),
                                Text(ThalaivaaTheme.formatInr(item.totalPrice), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                              ],
                            ),
                          );
                        }).toList(),
                        const Divider(height: 20),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(tr('totalPaid'), style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 14)),
                            Text(
                              ThalaivaaTheme.formatInr(orders.first.grandTotal),
                              style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15, color: ThalaivaaTheme.brandAmber),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTimelineRow({
    required IconData icon,
    required String title,
    required String subtitle,
    required bool isDone,
    required bool isCurrent,
    required bool isDark,
    bool isLast = false,
  }) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(6),
          decoration: BoxDecoration(
            color: isDone
                ? ThalaivaaTheme.vegGreen
                : (isDark ? Colors.white10 : const Color(0xFFE2E8F0)),
            shape: BoxShape.circle,
            border: isCurrent ? Border.all(color: ThalaivaaTheme.brandAmber, width: 3) : null,
          ),
          child: Icon(
            icon,
            size: 16,
            color: isDone ? Colors.white : (isDark ? Colors.white38 : Colors.grey),
          ),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 13,
                  color: isDone ? (isDark ? Colors.white : const Color(0xFF0F172A)) : Colors.grey,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                subtitle,
                style: TextStyle(fontSize: 11, color: isDark ? Colors.white54 : const Color(0xFF64748B)),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildTimelineDivider({required bool isDone, required bool isDark}) {
    return Container(
      margin: const EdgeInsets.only(left: 13),
      width: 2,
      height: 24,
      color: isDone ? ThalaivaaTheme.vegGreen : (isDark ? Colors.white10 : const Color(0xFFE2E8F0)),
    );
  }
}
'''

# 5. ProfileScreen.dart
PROFILE_SCREEN_CODE = r'''import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../providers/app_providers.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);
    final language = ref.watch(languageProvider);
    final branches = ref.watch(branchesProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final addresses = ref.watch(savedAddressesProvider);
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        title: Text(tr('profile'), style: const TextStyle(fontWeight: FontWeight.bold)),
        elevation: 0,
        backgroundColor: cardBg,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(16, 12, 16, 40),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // 1. Theme Switcher (Obsidian Dark vs Clean Light)
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.palette_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                          const SizedBox(width: 8),
                          Text(tr('themeMode'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: ChoiceChip(
                              label: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const Icon(Icons.light_mode_rounded, size: 16),
                                  const SizedBox(width: 6),
                                  Text(tr('lightMode')),
                                ],
                              ),
                              selected: themeMode == ThemeMode.light,
                              selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                              onSelected: (_) => ref.read(themeModeProvider.notifier).state = ThemeMode.light,
                            ),
                          ),
                          const SizedBox(width: 10),
                          Expanded(
                            child: ChoiceChip(
                              label: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const Icon(Icons.dark_mode_rounded, size: 16),
                                  const SizedBox(width: 6),
                                  Text(tr('darkMode')),
                                ],
                              ),
                              selected: themeMode == ThemeMode.dark,
                              selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                              onSelected: (_) => ref.read(themeModeProvider.notifier).state = ThemeMode.dark,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 2. Multi-Language Switcher (EN, HI, GU, TA)
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.translate_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                          const SizedBox(width: 8),
                          Text(tr('language'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          {'code': 'en', 'label': 'English'},
                          {'code': 'hi', 'label': 'हिन्दी (Hindi)'},
                          {'code': 'gu', 'label': 'ગુજરાતી (Gujarati)'},
                          {'code': 'ta', 'label': 'தமிழ் (Tamil)'},
                        ].map((item) {
                          final isSel = language == item['code'];
                          return ChoiceChip(
                            label: Text(item['label']!),
                            selected: isSel,
                            selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                            onSelected: (_) => ref.read(languageProvider.notifier).state = item['code']!,
                          );
                        }).toList(),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 3. Saved Addresses
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.location_on_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                          const SizedBox(width: 8),
                          Text(tr('savedAddresses'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        ],
                      ),
                      const SizedBox(height: 10),
                      ...addresses.map((addr) {
                        return Container(
                          margin: const EdgeInsets.only(bottom: 8),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: isDark ? Colors.white10 : const Color(0xFFE2E8F0)),
                          ),
                          child: Material(
                            color: Colors.transparent,
                            child: ListTile(
                              leading: Icon(
                                addr.label == 'Home' ? Icons.home_rounded : (addr.label == 'Work' ? Icons.business_rounded : Icons.place_rounded),
                                color: ThalaivaaTheme.brandAmber,
                              ),
                              title: Text(addr.label, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                              subtitle: Text('${addr.addressLine} • ${addr.landmark}', style: const TextStyle(fontSize: 11)),
                            ),
                          ),
                        );
                      }).toList(),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 4. Branch Selector
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.storefront_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                          const SizedBox(width: 8),
                          Text(tr('operatingBranch'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        ],
                      ),
                      const SizedBox(height: 10),
                      ...branches.map((b) {
                        final isSel = selectedBranch.id == b.id;
                        return Material(
                          color: Colors.transparent,
                          child: ListTile(
                            leading: Icon(
                              isSel ? Icons.radio_button_checked : Icons.radio_button_unchecked,
                              color: isSel ? ThalaivaaTheme.brandAmber : Colors.grey,
                            ),
                            title: Text(b.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                            subtitle: Text('${b.address} • ${b.deliveryTime}', style: const TextStyle(fontSize: 11)),
                            onTap: () {
                              ref.read(selectedBranchProvider.notifier).state = b;
                            },
                          ),
                        );
                      }).toList(),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
'''

with open(r'C:\Users\Admin\thalaivaa_flutter\lib\main.dart', 'w', encoding='utf-8') as f:
    f.write(MAIN_DART_CODE)

with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\menu\menu_screen.dart', 'w', encoding='utf-8') as f:
    f.write(MENU_SCREEN_CODE)

with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\cart\cart_screen.dart', 'w', encoding='utf-8') as f:
    f.write(CART_SCREEN_CODE)

with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\order\order_screen.dart', 'w', encoding='utf-8') as f:
    f.write(ORDER_SCREEN_CODE)

with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\profile\profile_screen.dart', 'w', encoding='utf-8') as f:
    f.write(PROFILE_SCREEN_CODE)

print('All UI screens written successfully.')
