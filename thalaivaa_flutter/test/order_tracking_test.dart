import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thalaivaa_flutter/providers/app_providers.dart';
import 'package:thalaivaa_flutter/features/order/order_screen.dart';

void main() {
  group('Live Order Tracking & Driver Visibility Tests', () {
    testWidgets('1. Confirmed Stage: Driver name is HIDDEN and assigning card is shown', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            liveTrackingStageProvider.overrideWith((ref) => LiveTrackingStage.confirmed),
          ],
          child: const MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      expect(find.text('Ramesh Patel'), findsNothing);
      expect(find.text('Assigning Delivery Partner'), findsOneWidget);
      expect(find.text('1. Order Confirmed'), findsOneWidget);
      expect(find.text('Call Partner'), findsNothing);
      expect(find.text('Chat with Partner'), findsNothing);
    });

    testWidgets('2. Preparing Stage: Driver name is HIDDEN and assigning card is shown', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            liveTrackingStageProvider.overrideWith((ref) => LiveTrackingStage.preparing),
          ],
          child: const MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      expect(find.text('Ramesh Patel'), findsNothing);
      expect(find.text('Assigning Delivery Partner'), findsOneWidget);
      expect(find.text('2. In the Kitchen'), findsOneWidget);
      expect(find.text('Call Partner'), findsNothing);
      expect(find.text('Chat with Partner'), findsNothing);
    });

    testWidgets('3. Out for Delivery Stage: Driver name is VISIBLE with call/chat buttons', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            liveTrackingStageProvider.overrideWith((ref) => LiveTrackingStage.onTheWay),
          ],
          child: const MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      expect(find.text('Ramesh Patel'), findsWidgets);
      expect(find.text('Verified Delivery Partner'), findsOneWidget);
      expect(find.text('Call Partner'), findsOneWidget);
      expect(find.text('Chat with Partner'), findsOneWidget);
      expect(find.text('Assigning Delivery Partner'), findsNothing);
    });

    testWidgets('4. Delivered Stage: Shows Delivered by summary and rating interaction', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            liveTrackingStageProvider.overrideWith((ref) => LiveTrackingStage.delivered),
          ],
          child: const MaterialApp(
            home: OrderScreen(),
          ),
        ),
      );
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      expect(find.text('Delivered by Ramesh Patel'), findsOneWidget);
      expect(find.text('Rate your delivery experience'), findsOneWidget);
      expect(find.byIcon(Icons.star_rounded), findsWidgets);
    });
  });
}
