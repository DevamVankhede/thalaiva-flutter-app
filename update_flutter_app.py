import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {path}")

# 1. Update main.dart
main_dart = '''import 'package:flutter/material.dart';
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
'''

# 2. Update menu_screen.dart
menu_screen_dart = '''import 'package:flutter/material.dart';
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
                              child: const Text('⚡', style: TextStyle(fontSize: 22)),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      const Text(
                                        'SPECIAL OFFER',
                                        style: TextStyle(
                                          color: ThalaivaaTheme.brandAmber,
                                          fontWeight: FontWeight.w900,
                                          fontSize: 11,
                                          letterSpacing: 0.5,
                                        ),
                                      ),
                                      const SizedBox(width: 8),
                                      Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                                        decoration: BoxDecoration(
                                          color: ThalaivaaTheme.brandAmber,
                                          borderRadius: BorderRadius.circular(4),
                                        ),
                                        child: const Text(
                                          'THALAIVAA50',
                                          style: TextStyle(color: Colors.white, fontSize: 9, fontWeight: FontWeight.bold),
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 2),
                                  Text(
                                    'Flat ₹50 OFF on orders above ₹200 + Free Delivery above ₹499',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w600,
                                      color: isDark ? Colors.white70 : const Color(0xFF334155),
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
                                  items: const [
                                    DropdownMenuItem(value: SortOption.recommended, child: Text('Recommended', style: TextStyle(fontSize: 12))),
                                    DropdownMenuItem(value: SortOption.rating, child: Text('Top Rated ★', style: TextStyle(fontSize: 12))),
                                    DropdownMenuItem(value: SortOption.priceLowToHigh, child: Text('Price: Low to High', style: TextStyle(fontSize: 12))),
                                    DropdownMenuItem(value: SortOption.priceHighToLow, child: Text('Price: High to Low', style: TextStyle(fontSize: 12))),
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

                  // 4. Interactive Category Filter Pills (MATCHING EXACT SLUGS)
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

                          return InkWell(
                            onTap: () {
                              ref.read(selectedCategoryProvider.notifier).state = cat;
                            },
                            borderRadius: BorderRadius.circular(22),
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 200),
                              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                              decoration: BoxDecoration(
                                gradient: isSelected
                                    ? const LinearGradient(
                                        colors: [ThalaivaaTheme.brandAmber, ThalaivaaTheme.primaryDeep],
                                      )
                                    : null,
                                color: isSelected ? null : cardBg,
                                borderRadius: BorderRadius.circular(22),
                                border: Border.all(
                                  color: isSelected ? Colors.transparent : cardBorder,
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
                                    cat == 'All' ? tr('all') : cat,
                                    style: TextStyle(
                                      color: isSelected ? Colors.white : (isDark ? Colors.white70 : const Color(0xFF334155)),
                                      fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                                      fontSize: 13,
                                    ),
                                  ),
                                  const SizedBox(width: 6),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                                    decoration: BoxDecoration(
                                      color: isSelected ? Colors.white.withValues(alpha: 0.25) : (isDark ? Colors.white12 : const Color(0xFFF1F5F9)),
                                      borderRadius: BorderRadius.circular(10),
                                    ),
                                    child: Text(
                                      count.toString(),
                                      style: TextStyle(
                                        color: isSelected ? Colors.white : (isDark ? Colors.white60 : const Color(0xFF64748B)),
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

                  // 5. Dish Grid / Product Cards
                  if (products.isEmpty)
                    SliverToBoxAdapter(
                      child: Padding(
                        padding: const EdgeInsets.all(40),
                        child: Center(
                          child: Column(
                            children: [
                              const Icon(Icons.search_off_rounded, size: 56, color: ThalaivaaTheme.brandAmber),
                              const SizedBox(height: 12),
                              const Text('No dishes found', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                              const SizedBox(height: 6),
                              Text('Try clearing filters or search term', style: TextStyle(color: isDark ? Colors.white54 : Colors.black45)),
                              const SizedBox(height: 16),
                              ElevatedButton(
                                onPressed: () {
                                  ref.read(selectedCategoryProvider.notifier).state = 'All';
                                  ref.read(searchQueryProvider.notifier).state = '';
                                  ref.read(dietaryFilterProvider.notifier).state = DietaryFilter.all;
                                  ref.read(bestsellerOnlyProvider.notifier).state = false;
                                },
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: ThalaivaaTheme.brandAmber,
                                  foregroundColor: Colors.white,
                                ),
                                child: const Text('Reset All Filters'),
                              ),
                            ],
                          ),
                        ),
                      ),
                    )
                  else
                    SliverPadding(
                      padding: const EdgeInsets.fromLTRB(16, 4, 16, 100),
                      sliver: SliverGrid(
                        gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                          maxCrossAxisExtent: 520,
                          mainAxisExtent: 170,
                          mainAxisSpacing: 12,
                          crossAxisSpacing: 12,
                        ),
                        delegate: SliverChildBuilderDelegate(
                          (ctx, idx) {
                            final product = products[idx];
                            return ProductCard(
                              product: product,
                              onCustomize: () => _openCustomizer(product),
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

          // 6. Floating Cart Tray Docked at Bottom
          if (cart.items.isNotEmpty)
            Positioned(
              left: 16,
              right: 16,
              bottom: 16,
              child: Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 600),
                  child: Material(
                    elevation: 12,
                    borderRadius: BorderRadius.circular(16),
                    color: Colors.transparent,
                    child: InkWell(
                      onTap: () {
                        ref.read(bottomNavIndexProvider.notifier).state = 1;
                      },
                      borderRadius: BorderRadius.circular(16),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
                        decoration: BoxDecoration(
                          gradient: const LinearGradient(
                            colors: [Color(0xFF0F172A), Color(0xFF1E293B)],
                          ),
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.5)),
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
                                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 11),
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Text(
                                      ThalaivaaTheme.formatInr(cart.grandTotal),
                                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 15),
                                    ),
                                    const Text('Plus taxes & delivery', style: TextStyle(color: Colors.white60, fontSize: 10)),
                                  ],
                                ),
                              ],
                            ),
                            Row(
                              children: const [
                                Text('VIEW TRAY', style: TextStyle(color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.w900, fontSize: 13)),
                                SizedBox(width: 4),
                                Icon(Icons.arrow_forward_rounded, color: ThalaivaaTheme.brandAmber, size: 16),
                              ],
                            ),
                          ],
                        ),
                      ),
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

class ProductCard extends ConsumerWidget {
  final Product product;
  final VoidCallback onCustomize;

  const ProductCard({
    super.key,
    required this.product,
    required this.onCustomize,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);
    final cart = ref.watch(cartProvider);

    final matchingItems = cart.items.where((i) => i.product.id == product.id).toList();
    final totalInCart = matchingItems.fold(0, (sum, i) => sum + i.quantity);

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: cardBorder),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: isDark ? 0.2 : 0.03),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 72,
            height: 72,
            decoration: BoxDecoration(
              color: isDark ? const Color(0xFF10141D) : const Color(0xFFFFF7ED),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15)),
            ),
            child: Center(
              child: Text(product.iconEmoji, style: const TextStyle(fontSize: 34)),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 13,
                          height: 13,
                          decoration: BoxDecoration(
                            border: Border.all(color: product.isVeg ? ThalaivaaTheme.vegGreen : ThalaivaaTheme.nonVegRed, width: 1.5),
                            borderRadius: BorderRadius.circular(3),
                          ),
                          child: Center(
                            child: Container(
                              width: 5,
                              height: 5,
                              decoration: BoxDecoration(
                                color: product.isVeg ? ThalaivaaTheme.vegGreen : ThalaivaaTheme.nonVegRed,
                                shape: BoxShape.circle,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 6),
                        const Icon(Icons.star_rounded, size: 14, color: ThalaivaaTheme.goldAccent),
                        Text(
                          ' ${product.rating} (${product.ratingCount})',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: isDark ? Colors.white70 : const Color(0xFF475569),
                          ),
                        ),
                        if (product.isBestseller) ...[
                          const SizedBox(width: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                            decoration: BoxDecoration(
                              color: ThalaivaaTheme.goldAccent.withValues(alpha: 0.2),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: const Text('⭐ MUST TRY', style: TextStyle(color: ThalaivaaTheme.goldAccent, fontSize: 8, fontWeight: FontWeight.w900)),
                          ),
                        ],
                      ],
                    ),
                    const SizedBox(height: 3),
                    Text(
                      product.name,
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 2),
                    Text(
                      product.description,
                      style: TextStyle(
                        fontSize: 11,
                        color: isDark ? Colors.white60 : const Color(0xFF64748B),
                        height: 1.25,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      ThalaivaaTheme.formatInr(product.price),
                      style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15, color: ThalaivaaTheme.brandAmber),
                    ),
                    if (totalInCart > 0)
                      Container(
                        decoration: BoxDecoration(
                          color: ThalaivaaTheme.brandAmber,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            InkWell(
                              onTap: () {
                                final first = matchingItems.first;
                                ref.read(cartProvider.notifier).updateQuantity(first.id, -1);
                              },
                              child: const Padding(
                                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                child: Icon(Icons.remove, color: Colors.white, size: 16),
                              ),
                            ),
                            Text(
                              '$totalInCart',
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                            ),
                            InkWell(
                              onTap: onCustomize,
                              child: const Padding(
                                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                child: Icon(Icons.add, color: Colors.white, size: 16),
                              ),
                            ),
                          ],
                        ),
                      )
                    else
                      ElevatedButton(
                        onPressed: onCustomize,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: ThalaivaaTheme.brandAmber,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                          minimumSize: const Size(64, 30),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          elevation: 0,
                        ),
                        child: const Text('ADD +', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 12)),
                      ),
                  ],
                ),
              ],
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
  final List<ModifierOption> _selectedModifiers = [];
  final TextEditingController _noteController = TextEditingController();

  @override
  void dispose() {
    _noteController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final groups = widget.product.modifierGroups;
    double extraPrice = _selectedModifiers.fold(0.0, (sum, m) => sum + m.price);
    double totalPrice = widget.product.price + extraPrice;

    return Container(
      decoration: BoxDecoration(
        color: isDark ? ThalaivaaTheme.surfaceCard : Colors.white,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      padding: const EdgeInsets.all(20),
      child: SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: Colors.grey.shade400,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Text(widget.product.iconEmoji, style: const TextStyle(fontSize: 32)),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(widget.product.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                      Text(
                        ThalaivaaTheme.formatInr(widget.product.price),
                        style: const TextStyle(color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.bold, fontSize: 14),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const Divider(height: 24),
            if (groups.isNotEmpty) ...[
              const Text('CUSTOMIZE YOUR ORDER', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: ThalaivaaTheme.brandAmber)),
              const SizedBox(height: 8),
              ...groups.map((group) {
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(group.title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    const SizedBox(height: 6),
                    Wrap(
                      spacing: 8,
                      children: group.options.map((option) {
                        final isSel = _selectedModifiers.any((m) => m.id == option.id);
                        return FilterChip(
                          label: Text('${option.name} (+₹${option.price.toInt()})', style: const TextStyle(fontSize: 12)),
                          selected: isSel,
                          selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                          checkmarkColor: ThalaivaaTheme.brandAmber,
                          onSelected: (selected) {
                            setState(() {
                              if (selected) {
                                _selectedModifiers.add(option);
                              } else {
                                _selectedModifiers.removeWhere((m) => m.id == option.id);
                              }
                            });
                          },
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 12),
                  ],
                );
              }).toList(),
            ],
            ElevatedButton(
              onPressed: () {
                ref.read(cartProvider.notifier).addItem(
                  widget.product,
                  modifiers: _selectedModifiers,
                  instructions: _noteController.text.trim().isNotEmpty ? _noteController.text.trim() : null,
                );
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Added ${widget.product.name} to Tray!'),
                    backgroundColor: ThalaivaaTheme.brandAmber,
                    behavior: SnackBarBehavior.floating,
                  ),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: ThalaivaaTheme.brandAmber,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                minimumSize: const Size(double.infinity, 48),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text('Add to Tray • ', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                  Text(
                    ThalaivaaTheme.formatInr(totalPrice),
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
'''

# 3. Update cart_screen.dart
cart_screen_dart = '''import 'package:flutter/material.dart';
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

  @override
  Widget build(BuildContext context) {
    final cart = ref.watch(cartProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    if (cart.items.isEmpty) {
      return Scaffold(
        backgroundColor: bg,
        appBar: AppBar(
          backgroundColor: cardBg,
          title: const Text('Your Food Tray', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.1),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.shopping_bag_outlined, size: 64, color: ThalaivaaTheme.brandAmber),
              ),
              const SizedBox(height: 16),
              const Text('Your Tray is Empty', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 6),
              Text(
                'Add freshly prepared dosas, idlis, and meals to start!',
                style: TextStyle(color: isDark ? Colors.white60 : Colors.black54, fontSize: 13),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  ref.read(bottomNavIndexProvider.notifier).state = 0;
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: ThalaivaaTheme.brandAmber,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Browse Menu', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Checkout & Bill Breakdown', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            Text(
              '${cart.totalItemCount} Items from ${selectedBranch.name}',
              style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.w600),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => ref.read(cartProvider.notifier).clearCart(),
            child: const Text('Clear', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 100),
            children: [
              // 1. Delivery vs Takeaway Switcher
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: cardBorder),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: InkWell(
                        onTap: () => ref.read(cartProvider.notifier).toggleDelivery(true),
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          decoration: BoxDecoration(
                            color: cart.isDelivery ? ThalaivaaTheme.brandAmber : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.delivery_dining_rounded, size: 18, color: cart.isDelivery ? Colors.white : (isDark ? Colors.white60 : Colors.black54)),
                              const SizedBox(width: 6),
                              Text('Delivery', style: TextStyle(fontWeight: FontWeight.bold, color: cart.isDelivery ? Colors.white : (isDark ? Colors.white70 : Colors.black87))),
                            ],
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      child: InkWell(
                        onTap: () => ref.read(cartProvider.notifier).toggleDelivery(false),
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          decoration: BoxDecoration(
                            color: !cart.isDelivery ? ThalaivaaTheme.brandAmber : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.storefront_rounded, size: 18, color: !cart.isDelivery ? Colors.white : (isDark ? Colors.white60 : Colors.black54)),
                              const SizedBox(width: 6),
                              Text('Dine-in / Takeaway', style: TextStyle(fontWeight: FontWeight.bold, color: !cart.isDelivery ? Colors.white : (isDark ? Colors.white70 : Colors.black87))),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 2. Cart Items List
              Container(
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: ListView.separated(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: cart.items.length,
                  separatorBuilder: (_, __) => Divider(height: 1, color: cardBorder),
                  itemBuilder: (ctx, idx) {
                    final item = cart.items[idx];
                    return Padding(
                      padding: const EdgeInsets.all(14),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(item.product.iconEmoji, style: const TextStyle(fontSize: 24)),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(item.product.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                                if (item.selectedModifiers.isNotEmpty)
                                  Text(
                                    item.selectedModifiers.map((m) => '+ ${m.name}').join(', '),
                                    style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber),
                                  ),
                                const SizedBox(height: 4),
                                Text(
                                  ThalaivaaTheme.formatInr(item.unitPrice),
                                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: ThalaivaaTheme.brandAmber),
                                ),
                              ],
                            ),
                          ),
                          Container(
                            decoration: BoxDecoration(
                              color: isDark ? const Color(0xFF10141D) : const Color(0xFFF1F5F9),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: cardBorder),
                            ),
                            child: Row(
                              children: [
                                InkWell(
                                  onTap: () => ref.read(cartProvider.notifier).updateQuantity(item.id, -1),
                                  child: const Padding(
                                    padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    child: Icon(Icons.remove, size: 16, color: ThalaivaaTheme.brandAmber),
                                  ),
                                ),
                                Text('${item.quantity}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                                InkWell(
                                  onTap: () => ref.read(cartProvider.notifier).updateQuantity(item.id, 1),
                                  child: const Padding(
                                    padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    child: Icon(Icons.add, size: 16, color: ThalaivaaTheme.brandAmber),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),

              const SizedBox(height: 16),

              // 3. Coupon Promo Code Box
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
                    Row(
                      children: const [
                        Icon(Icons.discount_rounded, color: ThalaivaaTheme.brandAmber, size: 18),
                        SizedBox(width: 8),
                        Text('Apply Promo Coupon', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                      ],
                    ),
                    const SizedBox(height: 10),
                    if (cart.appliedCoupon != null)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        decoration: BoxDecoration(
                          color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: ThalaivaaTheme.vegGreen),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              'Coupon ${cart.appliedCoupon} applied (-₹${cart.discountAmount.toInt()})',
                              style: const TextStyle(color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold, fontSize: 12),
                            ),
                            InkWell(
                              onTap: () => ref.read(cartProvider.notifier).removeCoupon(),
                              child: const Text('REMOVE', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold, fontSize: 11)),
                            ),
                          ],
                        ),
                      )
                    else
                      Row(
                        children: [
                          Expanded(
                            child: TextField(
                              controller: _couponController,
                              textCapitalization: TextCapitalization.characters,
                              decoration: InputDecoration(
                                hintText: 'Enter THALAIVAA50 or FEAST100',
                                hintStyle: TextStyle(fontSize: 12, color: isDark ? Colors.white38 : Colors.black38),
                                isDense: true,
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                                contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                          ElevatedButton(
                            onPressed: () {
                              final success = ref.read(cartProvider.notifier).applyCoupon(_couponController.text);
                              if (!success) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text('Invalid coupon code or minimum order not met!'),
                                    backgroundColor: Colors.redAccent,
                                  ),
                                );
                              }
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: ThalaivaaTheme.brandAmber,
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                            ),
                            child: const Text('APPLY', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                          ),
                        ],
                      ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 4. Delivery Partner Tip Selector
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
                    const Text('Tip your Delivery Partner', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    const SizedBox(height: 4),
                    Text('100% of the tip goes directly to your delivery partner', style: TextStyle(fontSize: 11, color: isDark ? Colors.white60 : Colors.black54)),
                    const SizedBox(height: 10),
                    Row(
                      children: [0.0, 20.0, 30.0, 50.0].map((tip) {
                        final isSel = cart.tipAmount == tip;
                        return Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: ChoiceChip(
                            label: Text(tip == 0.0 ? 'No Tip' : '₹${tip.toInt()}'),
                            selected: isSel,
                            selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                            onSelected: (_) => ref.read(cartProvider.notifier).setTip(tip),
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 5. Itemized Bill Summary
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
                    const Text('Bill Details', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Item Total', style: TextStyle(fontSize: 13)),
                        Text(ThalaivaaTheme.formatInr(cart.subtotal), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('GST & Restaurant Tax (5%)', style: TextStyle(fontSize: 13)),
                        Text(ThalaivaaTheme.formatInr(cart.tax), style: const TextStyle(fontSize: 13)),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Delivery Fee ${cart.subtotal > 499 ? "(Free above ₹499)" : ""}', style: const TextStyle(fontSize: 13)),
                        Text(
                          cart.deliveryFee == 0 ? 'FREE' : ThalaivaaTheme.formatInr(cart.deliveryFee),
                          style: TextStyle(
                            fontSize: 13,
                            color: cart.deliveryFee == 0 ? ThalaivaaTheme.vegGreen : null,
                            fontWeight: cart.deliveryFee == 0 ? FontWeight.bold : FontWeight.normal,
                          ),
                        ),
                      ],
                    ),
                    if (cart.tipAmount > 0) ...[
                      const SizedBox(height: 6),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Delivery Tip', style: TextStyle(fontSize: 13)),
                          Text(ThalaivaaTheme.formatInr(cart.tipAmount), style: const TextStyle(fontSize: 13)),
                        ],
                      ),
                    ],
                    if (cart.discountAmount > 0) ...[
                      const SizedBox(height: 6),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Coupon Discount', style: TextStyle(fontSize: 13, color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold)),
                          Text('-${ThalaivaaTheme.formatInr(cart.discountAmount)}', style: const TextStyle(fontSize: 13, color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold)),
                        ],
                      ),
                    ],
                    const Divider(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('To Pay', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
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

              // 6. Checkout CTA
              ElevatedButton(
                onPressed: () {
                  ref.read(ordersProvider.notifier).placeOrder(cart, selectedBranch);
                  ref.read(cartProvider.notifier).clearCart();
                  ref.read(bottomNavIndexProvider.notifier).state = 2; // Switch to Orders tab
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('🎉 Order Confirmed! Live tracking started.'),
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
                    const Text('PLACE ORDER • ', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 15)),
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
    );
  }
}
'''

# 4. Update order_screen.dart
order_screen_dart = '''import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../models/models.dart';
import '../../providers/app_providers.dart';

class OrderScreen extends ConsumerWidget {
  const OrderScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final orders = ref.watch(ordersProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    if (orders.isEmpty) {
      return Scaffold(
        backgroundColor: bg,
        appBar: AppBar(
          backgroundColor: cardBg,
          title: const Text('Live Order Tracking', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.delivery_dining_outlined, size: 64, color: ThalaivaaTheme.brandAmber),
              const SizedBox(height: 12),
              const Text('No Active Orders', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(height: 6),
              const Text('Place an order from the menu to track live progress!'),
            ],
          ),
        ),
      );
    }

    final activeOrder = orders.first;

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Live Order Tracking', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            Text('Order #${activeOrder.orderNumber}', style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.w600)),
          ],
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              // 1. Live 4-Stage Timeline Card
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
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(8),
                              decoration: BoxDecoration(
                                color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(Icons.timer_outlined, color: ThalaivaaTheme.vegGreen, size: 18),
                            ),
                            const SizedBox(width: 10),
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: const [
                                Text('Estimated Delivery', style: TextStyle(fontSize: 11, color: Colors.grey)),
                                Text('20-25 Mins', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                              ],
                            ),
                          ],
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Text('ON TIME', style: TextStyle(color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.bold, fontSize: 11)),
                        ),
                      ],
                    ),
                    const Divider(height: 24),
                    _buildTimelineStep('1. Order Confirmed', 'Received by ${activeOrder.branch.name}', true, isDark),
                    _buildTimelineStep('2. Kitchen Preparing', 'Chef is roasting your dosas in pure desi ghee', true, isDark),
                    _buildTimelineStep('3. Out for Delivery', 'Ramesh Kumar is on the way (Bajaj Chetak EV)', false, isDark),
                    _buildTimelineStep('4. Delivered', 'Delivered at ${activeOrder.deliveryAddress}', false, isDark, isLast: true),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 2. Driver & Branch Contact Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Row(
                  children: [
                    CircleAvatar(
                      radius: 22,
                      backgroundColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                      child: const Text('🛵', style: TextStyle(fontSize: 22)),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text('Ramesh Kumar', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                          Text('Delivery Partner • 4.9 ★ (1,240 Deliveries)', style: TextStyle(fontSize: 11, color: Colors.grey)),
                        ],
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.phone_rounded, color: ThalaivaaTheme.vegGreen),
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Calling Delivery Partner: +91 98250 11223')),
                        );
                      },
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 3. Order Items Summary
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
                    const Text('Order Summary', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    const SizedBox(height: 10),
                    ...activeOrder.items.map((item) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text('${item.quantity}x ${item.product.name}', style: const TextStyle(fontSize: 13)),
                            Text(ThalaivaaTheme.formatInr(item.totalPrice), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                          ],
                        ),
                      );
                    }).toList(),
                    const Divider(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Total Paid', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 14)),
                        Text(
                          ThalaivaaTheme.formatInr(activeOrder.grandTotal),
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
    );
  }

  Widget _buildTimelineStep(String title, String subtitle, bool isDone, bool isDark, {bool isLast = false}) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Column(
          children: [
            Container(
              width: 20,
              height: 20,
              decoration: BoxDecoration(
                color: isDone ? ThalaivaaTheme.vegGreen : (isDark ? Colors.white12 : Colors.grey.shade300),
                shape: BoxShape.circle,
              ),
              child: isDone
                  ? const Icon(Icons.check, size: 12, color: Colors.white)
                  : null,
            ),
            if (!isLast)
              Container(
                width: 2,
                height: 36,
                color: isDone ? ThalaivaaTheme.vegGreen : (isDark ? Colors.white12 : Colors.grey.shade300),
              ),
          ],
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 13,
                  color: isDone ? (isDark ? Colors.white : Colors.black87) : Colors.grey,
                ),
              ),
              Text(
                subtitle,
                style: TextStyle(fontSize: 11, color: isDark ? Colors.white54 : Colors.grey.shade600),
              ),
              if (!isLast) const SizedBox(height: 18),
            ],
          ),
        ),
      ],
    );
  }
}
'''

# 5. Update profile_screen.dart
profile_screen_dart = '''import 'package:flutter/material.dart';
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
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        title: Text(tr('profile'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              // User Account & Interactive OTP Login Card
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
                    Row(
                      children: [
                        CircleAvatar(
                          radius: 26,
                          backgroundColor: ThalaivaaTheme.brandAmber,
                          child: const Text('T', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('Ramesh Patel', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                              Text('+91 92170 02598 • Surat Outlet', style: TextStyle(color: isDark ? Colors.white60 : Colors.black54, fontSize: 12)),
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.green.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: Colors.green),
                          ),
                          child: const Text('🔐 Logged In', style: TextStyle(color: Colors.green, fontSize: 11, fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                    const SizedBox(height: 14),
                    const Divider(),
                    const SizedBox(height: 10),
                    const Text('Mobile OTP Authentication', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: TextEditingController(text: '+91 92170 02598'),
                            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                            decoration: InputDecoration(
                              labelText: 'Mobile Phone',
                              labelStyle: const TextStyle(fontSize: 11),
                              prefixIcon: const Icon(Icons.phone_android_rounded, size: 16),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton.icon(
                          onPressed: () {},
                          icon: const Icon(Icons.send_rounded, size: 14),
                          label: const Text('Send OTP', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: ThalaivaaTheme.brandAmber,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: TextEditingController(text: '123456'),
                            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, letterSpacing: 3),
                            decoration: InputDecoration(
                              labelText: '6-Digit OTP (Dev: 123456)',
                              labelStyle: const TextStyle(fontSize: 11),
                              prefixIcon: const Icon(Icons.lock_clock_rounded, size: 16),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton.icon(
                          onPressed: () {},
                          icon: const Icon(Icons.verified_user_rounded, size: 14),
                          label: const Text('Verify', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Logout & Session Management Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.red.withValues(alpha: 0.3)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text('Session & Account', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        SizedBox(height: 2),
                        Text('Revoke Sanctum token & sign out', style: TextStyle(fontSize: 11, color: Colors.grey)),
                      ],
                    ),
                    ElevatedButton.icon(
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('🚪 Logged Out Successfully. Please log in to place orders.'))
                        );
                      },
                      icon: const Icon(Icons.logout_rounded, size: 16),
                      label: const Text('Logout', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.redAccent,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Theme Settings (Dark / Light)
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
                    const Text('Appearance & Theme', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            Icon(isDark ? Icons.dark_mode_rounded : Icons.light_mode_rounded, color: ThalaivaaTheme.brandAmber),
                            const SizedBox(width: 10),
                            Text(isDark ? tr('darkMode') : tr('lightMode'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                          ],
                        ),
                        Switch(
                          value: themeMode == ThemeMode.dark,
                          activeColor: ThalaivaaTheme.brandAmber,
                          onChanged: (val) {
                            ref.read(themeModeProvider.notifier).state = val ? ThemeMode.dark : ThemeMode.light;
                          },
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Language Selector (i18n)
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
                    Row(
                      children: const [
                        Icon(Icons.translate_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                        SizedBox(width: 8),
                        Text('Language (ભાષા / भाषा / மொழி)', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
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

              // Branch Selector
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
                    Row(
                      children: const [
                        Icon(Icons.storefront_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                        SizedBox(width: 8),
                        Text('Select Operating Branch', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      ],
                    ),
                    const SizedBox(height: 10),
                    ...branches.map((b) {
                      final isSel = selectedBranch.id == b.id;
                      return RadioListTile<Branch>(
                        value: b,
                        groupValue: selectedBranch,
                        title: Text(b.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                        subtitle: Text('${b.address} • ${b.deliveryTime}', style: const TextStyle(fontSize: 11)),
                        activeColor: ThalaivaaTheme.brandAmber,
                        onChanged: (val) {
                          if (val != null) ref.read(selectedBranchProvider.notifier).state = val;
                        },
                      );
                    }).toList(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
'''

# Write files
base_dir = r"C:\Users\Admin\thalaivaa_flutter\lib"
write_file(os.path.join(base_dir, "main.dart"), main_dart)
write_file(os.path.join(base_dir, "features", "menu", "menu_screen.dart"), menu_screen_dart)
write_file(os.path.join(base_dir, "features", "cart", "cart_screen.dart"), cart_screen_dart)
write_file(os.path.join(base_dir, "features", "order", "order_screen.dart"), order_screen_dart)
write_file(os.path.join(base_dir, "features", "profile", "profile_screen.dart"), profile_screen_dart)
print("All Flutter components updated successfully!")
