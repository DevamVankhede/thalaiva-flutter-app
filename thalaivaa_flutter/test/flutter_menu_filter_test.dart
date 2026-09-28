import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';
import 'package:thalaivaa_flutter/core/theme.dart';

void main() {
  group('Thalaivaa Filter, Delivery & Business Logic Tests', () {
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
      expect(products.every((p) => p.category == 'Dosas'), isTrue);
    });

    test('Category filter isolates Idlis & Vadas category', () {
      final container = ProviderContainer();
      container.read(selectedCategoryProvider.notifier).state = 'Idlis & Vadas';
      final products = container.read(filteredProductsProvider);
      expect(products.length, 5);
      expect(products.every((p) => p.category == 'Idlis & Vadas'), isTrue);
    });

    test('Category filter isolates Beverages category', () {
      final container = ProviderContainer();
      container.read(selectedCategoryProvider.notifier).state = 'Beverages';
      final products = container.read(filteredProductsProvider);
      expect(products.length, 4);
    });

    test('Search query matches dish name and description', () {
      final container = ProviderContainer();
      container.read(searchQueryProvider.notifier).state = 'Ghee Roast';
      final products = container.read(filteredProductsProvider);
      expect(products.length, greaterThanOrEqualTo(1));
      expect(products.first.name.contains('Ghee Roast'), isTrue);
    });

    test('Bestseller filter only returns bestseller products', () {
      final container = ProviderContainer();
      container.read(bestsellerOnlyProvider.notifier).state = true;
      final products = container.read(filteredProductsProvider);
      expect(products.every((p) => p.isBestseller), isTrue);
      expect(products.length, greaterThan(0));
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
        expect(products[i].price <= products[i + 1].price, isTrue);
      }
    });

    test('Cart state correctly calculates subtotal, GST (5%), delivery fee & tip', () {
      final container = ProviderContainer();
      final p1 = sampleProducts.first; // Price: 180
      container.read(cartProvider.notifier).addItem(p1);
      container.read(cartProvider.notifier).setTip(30.0);

      final cart = container.read(cartProvider);
      expect(cart.subtotal, 180.0);
      expect(cart.tax, 180.0 * 0.05);
      expect(cart.deliveryFee, 40.0);
      expect(cart.tipAmount, 30.0);
      expect(cart.grandTotal, 180.0 + 9.0 + 40.0 + 30.0);
    });

    test('Delivery Address & OrderType state verify properly', () {
      final container = ProviderContainer();
      final addresses = container.read(savedAddressesProvider);
      expect(addresses.length, 3);
      expect(addresses.first.label, 'Home');

      final orderType = container.read(orderTypeProvider);
      expect(orderType, OrderType.delivery);
    });

    test('Multi-language translation returns expected values for all 4 languages', () {
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

    test('Dish name & description localization works across languages', () {
      final container = ProviderContainer();
      final p1 = sampleProducts.first;

      // English
      container.read(languageProvider.notifier).state = 'en';
      var dishInfo = container.read(localizedDishInfoProvider(p1));
      expect(dishInfo.name, 'Ghee Roast Masala Dosa');

      // Hindi
      container.read(languageProvider.notifier).state = 'hi';
      dishInfo = container.read(localizedDishInfoProvider(p1));
      expect(dishInfo.name, 'घी रोस्ट मसाला डोसा');

      // Gujarati
      container.read(languageProvider.notifier).state = 'gu';
      dishInfo = container.read(localizedDishInfoProvider(p1));
      expect(dishInfo.name, 'ઘી રોસ્ટ મસાલા ઢોસા');

      // Tamil
      container.read(languageProvider.notifier).state = 'ta';
      dishInfo = container.read(localizedDishInfoProvider(p1));
      expect(dishInfo.name, 'நெய் ரோஸ்ட் மசாலா தோசை');
    });

    test('ThalaivaaTheme formats INR currency cleanly with rupee symbol', () {
      expect(ThalaivaaTheme.formatInr(180.0), '₹180');
      expect(ThalaivaaTheme.formatInr(240.0), '₹240');
    });
  });
}
