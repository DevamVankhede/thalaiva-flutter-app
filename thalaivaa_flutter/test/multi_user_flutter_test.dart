import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/models/models.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';
import 'package:thalaivaa_flutter/features/order/order_screen.dart';
import 'package:thalaivaa_flutter/features/profile/profile_screen.dart';

void main() {
  group('Multi-User Flutter Authentication & Order History Tests', () {
    testWidgets('1. ProfileScreen renders sign-in form when logged out and hides it when logged in', (tester) async {
      final loggedOutContainer = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final n = AuthNotifier(ref);
            n.state = null;
            return n;
          }),
          ordersProvider.overrideWith((ref) {
            final n = OrdersNotifier(ref);
            n.state = [];
            return n;
          }),
        ],
      );

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: loggedOutContainer,
          child: const MaterialApp(
            home: ProfileScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Logged out: sign-in things are present
      expect(find.text('Sign In to Your Account'), findsOneWidget);
      expect(find.text('User A (3 Orders)'), findsOneWidget);
      expect(find.text('User B (1 Order)'), findsOneWidget);
      expect(find.text('User C (0 Orders)'), findsOneWidget);
      expect(find.text('Password Authentication (Database Validated)'), findsOneWidget);
      expect(find.text('Sign In with Database Credentials'), findsOneWidget);
      expect(find.text('Alternative: Mobile OTP Authentication'), findsOneWidget);

      // Now test with a logged in user: sign-in things MUST NOT be present
      final user = const UserModel(
        id: 'uuid-test',
        name: 'Test Customer',
        email: 'test@example.com',
        phone: '+919999999999',
        token: 'sample-token',
      );

      final loggedInContainer = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final n = AuthNotifier(ref);
            n.state = user;
            return n;
          }),
          ordersProvider.overrideWith((ref) {
            final n = OrdersNotifier(ref);
            n.state = [];
            return n;
          }),
        ],
      );

      await tester.pumpWidget(
        UncontrolledProviderScope(
          container: loggedInContainer,
          child: const MaterialApp(
            home: ProfileScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Logged in: user profile is visible, NO sign-in things are present
      expect(find.text('Test Customer'), findsOneWidget);
      expect(find.text('Signed In'), findsOneWidget);
      expect(find.text('Sign Out / Switch Account'), findsOneWidget);
      expect(find.text('Sign In to Your Account'), findsNothing);
      expect(find.text('Password Authentication (Database Validated)'), findsNothing);
      expect(find.text('Sign In with Database Credentials'), findsNothing);
      expect(find.text('Alternative: Mobile OTP Authentication'), findsNothing);
      expect(find.text('User A (3 Orders)'), findsNothing);
    });

    testWidgets('2. Switching to User A displays User A profile & 3 orders in OrderScreen', (tester) async {
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
          orderNumber: 'ORD-001',
          items: [],
          subtotal: 360.0,
          tax: 18.0,
          deliveryFee: 40.0,
          discount: 50.0,
          grandTotal: 368.0,
          status: OrderStatus.delivered,
          createdAt: DateTime.now().subtract(const Duration(days: 2)),
          branch: const Branch(id: 'br-1', name: 'Thalaivaa - City Light', address: 'Surat', phone: '+91 92170 02598'),
          deliveryAddress: 'Flat 402, City Light',
        ),
        OrderModel(
          id: 'ord-2',
          orderNumber: 'ORD-002',
          items: [],
          subtotal: 240.0,
          tax: 12.0,
          deliveryFee: 40.0,
          discount: 0.0,
          grandTotal: 292.0,
          status: OrderStatus.preparing,
          createdAt: DateTime.now().subtract(const Duration(minutes: 20)),
          branch: const Branch(id: 'br-1', name: 'Thalaivaa - City Light', address: 'Surat', phone: '+91 92170 02598'),
          deliveryAddress: 'Flat 402, City Light',
        ),
        OrderModel(
          id: 'ord-3',
          orderNumber: 'ORD-003',
          items: [],
          subtotal: 140.0,
          tax: 7.0,
          deliveryFee: 40.0,
          discount: 0.0,
          grandTotal: 187.0,
          status: OrderStatus.confirmed,
          createdAt: DateTime.now().subtract(const Duration(minutes: 5)),
          branch: const Branch(id: 'br-1', name: 'Thalaivaa - City Light', address: 'Surat', phone: '+91 92170 02598'),
          deliveryAddress: 'Flat 402, City Light',
        ),
      ];

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
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Welcome, Aarav Sharma'), findsOneWidget);
      expect(find.textContaining('3 orders found in database'), findsOneWidget);
    });

    testWidgets('3. Switching to User B displays User B profile & single order in OrderScreen', (tester) async {
      final userB = const UserModel(
        id: 'uuid-b',
        name: 'Bhavna Patel',
        email: 'userb@test.com',
        phone: '+919800000002',
        token: 'token-b',
      );

      final ordersB = [
        OrderModel(
          id: 'ord-4',
          orderNumber: 'ORD-004',
          items: [],
          subtotal: 480.0,
          tax: 24.0,
          deliveryFee: 0.0,
          discount: 100.0,
          grandTotal: 404.0,
          status: OrderStatus.outForDelivery,
          createdAt: DateTime.now().subtract(const Duration(minutes: 40)),
          branch: const Branch(id: 'br-2', name: 'Thalaivaa - Vesu Branch', address: 'VIP Road, Vesu', phone: '+91 92170 02599'),
          deliveryAddress: '102 Green Acres, Vesu',
        ),
      ];

      final container = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final n = AuthNotifier(ref);
            n.state = userB;
            return n;
          }),
          ordersProvider.overrideWith((ref) {
            final n = OrdersNotifier(ref);
            n.state = ordersB;
            return n;
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

      expect(find.text('Welcome, Bhavna Patel'), findsOneWidget);
      expect(find.text('Order #ORD-004'), findsOneWidget);
    });

    testWidgets('4. Switching to User C displays "No orders found." without crash', (tester) async {
      final userC = const UserModel(
        id: 'uuid-c',
        name: 'Chirag Mehta',
        email: 'userc@test.com',
        phone: '+919800000003',
        token: 'token-c',
      );

      final container = ProviderContainer(
        overrides: [
          authProvider.overrideWith((ref) {
            final n = AuthNotifier(ref);
            n.state = userC;
            return n;
          }),
          ordersProvider.overrideWith((ref) {
            final n = OrdersNotifier(ref);
            n.state = [];
            return n;
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

      expect(find.text('Welcome, Chirag Mehta'), findsOneWidget);
      expect(find.text('No orders found.'), findsOneWidget);
      expect(find.text('Browse Menu'), findsOneWidget);
    });

    testWidgets('5. Logout revokes state and redirects OrderScreen to unauthenticated view', (tester) async {
      final userA = const UserModel(
        id: 'uuid-a',
        name: 'Aarav Sharma',
        email: 'usera@test.com',
        phone: '+919800000001',
        token: 'token-a',
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
            n.state = [
              OrderModel(
                id: 'ord-1',
                orderNumber: 'ORD-001',
                items: [],
                subtotal: 360.0,
                tax: 18.0,
                deliveryFee: 40.0,
                discount: 50.0,
                grandTotal: 368.0,
                status: OrderStatus.delivered,
                createdAt: DateTime.now(),
                branch: const Branch(id: 'br-1', name: 'Main', address: 'Surat', phone: '+91 92170 02598'),
                deliveryAddress: 'Surat',
              ),
            ];
            return n;
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

      expect(find.text('Welcome, Aarav Sharma'), findsOneWidget);

      // Perform logout
      await container.read(authProvider.notifier).logout();
      await tester.pumpAndSettle();

      expect(find.text('Authentication Required'), findsOneWidget);
      expect(find.text('Go to Login Screen'), findsOneWidget);
    });
  });
}
