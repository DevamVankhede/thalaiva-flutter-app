import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/core/theme.dart';
import 'package:thalaivaa_flutter/models/models.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';

void main() {
  group('Thalaivaa Flutter Menu & Cart Unit Tests', () {
    test('1. Sample Products count & category distribution', () {
      expect(sampleProducts.length, 30);
      final categories = sampleProducts.map((p) => p.category).toSet();
      expect(categories.length, greaterThanOrEqualTo(5));
      expect(categories.contains('Dosas & Crispy Roasts'), isTrue);
    });

    test('2. Filtered products search functionality', () {
      final container = ProviderContainer();
      container.read(searchQueryProvider.notifier).state = 'Ghee Roast';

      final filtered = container.read(filteredProductsProvider);
      expect(filtered.every((p) => p.name.contains('Ghee Roast') || p.description.contains('Ghee Roast')), isTrue);
    });

    test('3. Branch selection updates active operating branch', () {
      final container = ProviderContainer();
      final branches = container.read(branchesProvider);
      expect(branches.length, 3);
      expect(branches.first.name, 'Thalaivaa - City Light (Main)');

      container.read(selectedBranchProvider.notifier).state = branches[1];
      final activeBranch = container.read(selectedBranchProvider);
      expect(activeBranch.id, 'br-2');
      expect(activeBranch.name, 'Thalaivaa - Vesu Branch');
    });

    test('4. Cart calculations: Subtotal, Tax, Delivery Fee & Grand Total', () {
      final container = ProviderContainer();
      final p1 = sampleProducts.first; // Price: 180.0
      container.read(cartProvider.notifier).addItem(p1);
      container.read(cartProvider.notifier).setTip(30.0);

      final cart = container.read(cartProvider);
      expect(cart.subtotal, 180.0);
      expect(cart.tax, 180.0 * 0.05);
      expect(cart.deliveryFee, 40.0);
      expect(cart.tipAmount, 30.0);
      expect(cart.grandTotal, 180.0 + 9.0 + 40.0 + 30.0);
    });

    test('5. Multi-language translation support for all 4 languages', () {
      final container = ProviderContainer();
      final translations = container.read(translationsProvider);

      expect(translations.containsKey('en'), isTrue);
      expect(translations.containsKey('hi'), isTrue);
      expect(translations.containsKey('gu'), isTrue);
      expect(translations.containsKey('ta'), isTrue);

      expect(translations['en']!['appName'], 'THALAIVAA');
      expect(translations['hi']!['appName'], 'थलाइवा');
      expect(translations['gu']!['appName'], 'થલાઇવા');
      expect(translations['ta']!['appName'], 'தலைவா');
    });

    test('6. ThalaivaaTheme formats INR currency cleanly', () {
      expect(ThalaivaaTheme.formatInr(180.0), '₹180');
      expect(ThalaivaaTheme.formatInr(240.0), '₹240');
    });
  });
}
