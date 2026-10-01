import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/models/models.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';
import 'package:thalaivaa_flutter/features/order/past_orders_screen.dart';
import 'package:thalaivaa_flutter/features/profile/profile_screen.dart';

void main() {
  group('PastOrdersScreen & Profile Navigation Tests', () {
    final testBranch = const Branch(
      id: 'br-1',
      name: 'Thalaivaa - City Light (Main)',
      address: 'City Light, Surat',
      phone: '+91 92170 02598',
    );

    final userA = const UserModel(
      id: 'uuid-a',
      name: 'Aarav Sharma',
      email: 'usera@test.com',
      phone: '+919800000001',
      token: 'token-a',
    );

    final ordersA = [
      OrderModel(
        id: 'ord-1',
        orderNumber: 'THL-1722',
        items: [
          CartItem(
            id: 'ci-1',
            product: sampleProducts[0],
            quantity: 1,
          ),
        ],
        subtotal: 180.0,
        tax: 9.0,
        deliveryFee: 40.0,
        discount: 0.0,
        grandTotal: 229.0,
        status: OrderStatus.confirmed,
        createdAt: DateTime(2026, 10, 1),
        branch: testBranch,
        deliveryAddress: 'Flat 402, Royal Palms, City Light, Surat',
      ),
      OrderModel(
        id: 'ord-2',
        orderNumber: 'ORD-003',
        items: [
          CartItem(
            id: 'ci-2',
            product: sampleProducts[1],
            quantity: 1,
          ),
        ],
        subtotal: 140.0,
        tax: 7.0,
        deliveryFee: 40.0,
        discount: 0.0,
        grandTotal: 187.0,
        status: OrderStatus.confirmed,
        createdAt: DateTime(2026, 9, 30),
        branch: testBranch,
        deliveryAddress: 'Flat 402, Royal Palms, City Light, Surat',
      ),
    ];

    testWidgets('1. ProfileScreen contains "My Past Orders" button when user is logged in', (tester) async {
      final container = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final n = AuthNotifier(ref);
            n.state = userA;
            return n;
          }),
          ordersProvider.overrideWith((ref) {
            final n = OrdersNotifier(ref);
            n.state = ordersA;
            return n;
          }),
        ],
      );

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: ProfileScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('My Past Orders'), findsOneWidget);
      expect(find.text('View complete order history, past meals & invoices'), findsOneWidget);
    });

    testWidgets('2. PastOrdersScreen lists all past orders with status badges and totals', (tester) async {
      final container = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final n = AuthNotifier(ref);
            n.state = userA;
            return n;
          }),
          ordersProvider.overrideWith((ref) {
            final n = OrdersNotifier(ref);
            n.state = ordersA;
            return n;
          }),
        ],
      );

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: PastOrdersScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Past Orders & History'), findsOneWidget);
      expect(find.text('Order #THL-1722'), findsOneWidget);
      expect(find.text('Order #ORD-003'), findsOneWidget);
      expect(find.text('Live Tracking'), findsNWidgets(2));
    });

    testWidgets('3. PastOrdersScreen does NOT show Live Tracking button for delivered orders', (tester) async {
      final deliveredOrder = OrderModel(
        id: 'ord-del',
        orderNumber: 'ORD-001',
        items: [],
        subtotal: 360.0,
        tax: 0.0,
        deliveryFee: 0.0,
        discount: 0.0,
        grandTotal: 368.0,
        status: OrderStatus.delivered,
        createdAt: DateTime(2026, 9, 29),
        branch: testBranch,
        deliveryAddress: 'Surat',
      );

      final container = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final n = AuthNotifier(ref);
            n.state = userA;
            return n;
          }),
          ordersProvider.overrideWith((ref) {
            final n = OrdersNotifier(ref);
            n.state = [deliveredOrder];
            return n;
          }),
        ],
      );

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: container,
          child: const MaterialApp(
            home: PastOrdersScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Past Orders & History'), findsOneWidget);
      expect(find.text('Order #ORD-001'), findsOneWidget);
      expect(find.text('Live Tracking'), findsNothing);
      expect(find.text('DELIVERED'), findsOneWidget); // Header badge
      expect(find.text('Delivered'), findsOneWidget); // Bottom check badge
    });
  });
}

