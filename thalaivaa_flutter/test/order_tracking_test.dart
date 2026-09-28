import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/core/theme.dart';
import 'package:thalaivaa_flutter/models/models.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';
import 'package:thalaivaa_flutter/features/order/order_screen.dart';

void main() {
  group('Live Order Tracking Widget Tests', () {
    testWidgets('1. Displays Empty State when no orders exist', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            ordersProvider.overrideWith((ref) => []),
          ],
          child: const MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('No Active Orders'), findsOneWidget);
      expect(find.text('Live Order Tracking'), findsOneWidget);
    });

    testWidgets('2. Displays Live Order Tracking timeline and summary when order exists', (tester) async {
      final mockBranch = const Branch(
        id: 'br-1',
        name: 'Thalaivaa - City Light (Main)',
        address: 'City Light Town, Surat',
        phone: '+91 92170 02598',
        rating: 4.9,
        deliveryTime: '20-25 min',
      );

      final mockProduct = const Product(
        id: 'p-1',
        name: 'Ghee Roast Masala Dosa',
        description: 'Crispy Dosa',
        price: 180.0,
        category: 'Dosas',
        iconEmoji: '🥞',
      );

      final mockOrder = Order(
        id: 'ord-101',
        orderNumber: 'TH-98201',
        branch: mockBranch,
        items: [OrderItem(product: mockProduct, quantity: 2)],
        subtotal: 360.0,
        tax: 18.0,
        deliveryFee: 40.0,
        discount: 0.0,
        grandTotal: 418.0,
        deliveryAddress: 'City Light, Surat',
        createdAt: DateTime.now(),
        status: 'In Kitchen',
      );

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            ordersProvider.overrideWith((ref) => [mockOrder]),
          ],
          child: const MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Live Order Tracking'), findsOneWidget);
      expect(find.text('Order #TH-98201'), findsOneWidget);
      expect(find.text('Estimated Delivery'), findsOneWidget);
      expect(find.text('2x Ghee Roast Masala Dosa'), findsOneWidget);
      expect(find.text('Ramesh Kumar'), findsOneWidget);
    });
  });
}
