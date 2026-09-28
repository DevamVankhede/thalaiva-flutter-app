import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/models/models.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';
import 'package:thalaivaa_flutter/features/order/order_screen.dart';

void main() {
  group('Live Order Tracking Widget Tests', () {
    testWidgets('1. Displays OrderScreen timeline with active initial order', (tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Live Order Tracking'), findsOneWidget);
      expect(find.text('Order Summary'), findsOneWidget);
      expect(find.text('Ramesh Kumar'), findsOneWidget);
      expect(find.text('1. Order Confirmed'), findsOneWidget);
      expect(find.text('2. Kitchen Preparing'), findsOneWidget);
    });

    testWidgets('2. Calculates CartState item totals accurately', (tester) async {
      final p1 = sampleProducts.first;
      final item = CartItem(id: 'ci-1', product: p1, quantity: 2);
      final cart = CartState(
        items: [item],
        discountAmount: 50.0,
      );

      expect(cart.subtotal, 360.0);
      expect(cart.totalItemCount, 2);
      expect(cart.grandTotal, 360.0 + 18.0 + 40.0 - 50.0);
    });
  });
}
