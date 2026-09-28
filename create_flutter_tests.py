import os

test_content = '''import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/core/theme.dart';
import 'package:thalaivaa_flutter/models/models.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';

void main() {
  group('Thalaivaa Filter & Business Logic Tests', () {
    test('Initial filtered list contains all 30 products', () {
      final container = ProviderContainer();
      final products = container.read(filteredProductsProvider);
      expect(products.length, 30);
    });

    test('Category filter accurately isolates Dosas category', () {
      final container = ProviderContainer();
      container.read(selectedCategoryProvider.notifier).state = 'Dosas';
      final products = container.read(filteredProductsProvider);
      expect(products.length, 6);
      for (final p in products) {
        expect(p.category, 'Dosas');
      }
    });

    test('Category filter isolates Idlis & Vadas category', () {
      final container = ProviderContainer();
      container.read(selectedCategoryProvider.notifier).state = 'Idlis & Vadas';
      final products = container.read(filteredProductsProvider);
      expect(products.length, 5);
      for (final p in products) {
        expect(p.category, 'Idlis & Vadas');
      }
    });

    test('Category filter isolates Beverages category', () {
      final container = ProviderContainer();
      container.read(selectedCategoryProvider.notifier).state = 'Beverages';
      final products = container.read(filteredProductsProvider);
      expect(products.length, 4);
      for (final p in products) {
        expect(p.category, 'Beverages');
      }
    });

    test('Search query matches dish name and description', () {
      final container = ProviderContainer();
      container.read(searchQueryProvider.notifier).state = 'Ghee Roast';
      final products = container.read(filteredProductsProvider);
      expect(products.isNotEmpty, true);
      expect(products.first.name, contains('Ghee Roast'));
    });

    test('Bestseller filter only returns bestseller products', () {
      final container = ProviderContainer();
      container.read(bestsellerOnlyProvider.notifier).state = true;
      final products = container.read(filteredProductsProvider);
      for (final p in products) {
        expect(p.isBestseller, true);
      }
    });

    test('Pure Veg dietary filter retains all veg dishes', () {
      final container = ProviderContainer();
      container.read(dietaryFilterProvider.notifier).state = DietaryFilter.vegOnly;
      final products = container.read(filteredProductsProvider);
      expect(products.length, 30);
    });

    test('Price Low to High sorting sorts correctly', () {
      final container = ProviderContainer();
      container.read(sortByProvider.notifier).state = SortOption.priceLowToHigh;
      final products = container.read(filteredProductsProvider);
      for (int i = 0; i < products.length - 1; i++) {
        expect(products[i].price <= products[i + 1].price, true);
      }
    });

    test('Cart state correctly calculates subtotal, GST (5%), and delivery fee', () {
      final container = ProviderContainer();
      final notifier = container.read(cartProvider.notifier);

      // Add product (price: 180)
      notifier.addItem(sampleProducts[0]);
      var cart = container.read(cartProvider);
      expect(cart.totalItemCount, 1);
      expect(cart.subtotal, 180.0);
      expect(cart.tax, 9.0);
      expect(cart.deliveryFee, 40.0);
      expect(cart.grandTotal, 229.0);

      // Apply valid coupon THALAIVAA50 on order >= 200 (add another item: 180 + 240 = 420)
      notifier.addItem(sampleProducts[1]);
      final couponApplied = notifier.applyCoupon('THALAIVAA50');
      expect(couponApplied, true);
      cart = container.read(cartProvider);
      expect(cart.discountAmount, 50.0);
      expect(cart.grandTotal, 420.0 + (420.0 * 0.05) + 40.0 - 50.0);
    });

    test('Multi-language translation returns expected values for all 4 languages', () {
      final container = ProviderContainer();
      final trEn = container.read(trProvider);
      expect(trEn('appName'), 'THALAIVAA');

      container.read(languageProvider.notifier).state = 'hi';
      final trHi = container.read(trProvider);
      expect(trHi('appName'), 'थलाइवा');

      container.read(languageProvider.notifier).state = 'gu';
      final trGu = container.read(trProvider);
      expect(trGu('appName'), 'થલાઈવા');

      container.read(languageProvider.notifier).state = 'ta';
      final trTa = container.read(trProvider);
      expect(trTa('appName'), 'தலைவா');
    });

    test('ThalaivaaTheme formats INR currency cleanly with rupee symbol', () {
      expect(ThalaivaaTheme.formatInr(180), '₹180');
      expect(ThalaivaaTheme.formatInr(1500), '₹1,500');
    });
  });
}
'''

os.makedirs(r"C:\Users\Admin\thalaivaa_flutter\test", exist_ok=True)
with open(r"C:\Users\Admin\thalaivaa_flutter\test\flutter_menu_filter_test.dart", 'w', encoding='utf-8') as f:
    f.write(test_content)
print("Created flutter_menu_filter_test.dart")
