import 'package:flutter/material.dart';
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
