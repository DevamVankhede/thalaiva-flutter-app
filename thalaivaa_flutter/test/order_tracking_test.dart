import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/models/models.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';
import 'package:thalaivaa_flutter/features/order/order_screen.dart';

void main() {
  group('Live Order Tracking Widget Tests', () {
    testWidgets('1. Displays OrderScreen timeline when user is authenticated with orders', (tester) async {
      final sampleOrder = OrderModel(
        id: 'ord-101',
        orderNumber: 'THL-9482',
        items: [
          CartItem(
            id: 'ci-1',
            product: sampleProducts[0],
            quantity: 2,
          ),
        ],
        subtotal: 360.0,
        tax: 18.0,
        deliveryFee: 40.0,
        discount: 50.0,
        grandTotal: 368.0,
        status: OrderStatus.preparing,
        createdAt: DateTime.now(),
        branch: const Branch(
          id: 'br-1',
          name: 'Thalaivaa - City Light (Main)',
          address: 'City Light, Surat',
          phone: '+91 92170 02598',
        ),
        deliveryAddress: 'Flat 402, Royal Palms, City Light',
      );

      final container = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final notifier = AuthNotifier(ref);
            notifier.state = const UserModel(
              id: 'user-uuid-1',
              name: 'Aarav Sharma',
              email: 'usera@test.com',
              phone: '+919800000001',
              token: 'test-token',
            );
            return notifier;
          }),
          ordersProvider.overrideWith((ref) {
            final notifier = OrdersNotifier(ref);
            notifier.state = [sampleOrder];
            return notifier;
          }),
        ],
      );

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('My Orders & Live Tracking'), findsOneWidget);
      expect(find.text('Order Summary'), findsOneWidget);
      expect(find.text('Assigning Delivery Partner'), findsOneWidget);
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

    testWidgets('3. Displays empty state "No orders found." for User C (zero orders)', (tester) async {
      final container = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final notifier = AuthNotifier(ref);
            notifier.state = const UserModel(
              id: 'user-uuid-3',
              name: 'Chirag Mehta',
              email: 'userc@test.com',
              phone: '+919800000003',
              token: 'test-token-c',
            );
            return notifier;
          }),
          ordersProvider.overrideWith((ref) {
            final notifier = OrdersNotifier(ref);
            notifier.state = [];
            return notifier;
          }),
        ],
      );

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('No orders found.'), findsOneWidget);
      expect(find.text('Welcome, Chirag Mehta'), findsOneWidget);
    });

    testWidgets('4. Displays Authentication Required when unauthenticated', (tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Authentication Required'), findsOneWidget);
      expect(find.text('Go to Login Screen'), findsOneWidget);
    });
  });
}
