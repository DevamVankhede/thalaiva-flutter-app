import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../models/models.dart';
import '../../providers/app_providers.dart';

class OrderScreen extends ConsumerWidget {
  const OrderScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final orders = ref.watch(ordersProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    if (orders.isEmpty) {
      return Scaffold(
        backgroundColor: bg,
        appBar: AppBar(
          backgroundColor: cardBg,
          title: const Text('Live Order Tracking', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.delivery_dining_outlined, size: 64, color: ThalaivaaTheme.brandAmber),
              const SizedBox(height: 12),
              const Text('No Active Orders', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(height: 6),
              const Text('Place an order from the menu to track live progress!'),
            ],
          ),
        ),
      );
    }

    final activeOrder = orders.first;

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Live Order Tracking', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            Text('Order #${activeOrder.orderNumber}', style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.w600)),
          ],
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              // 1. Live 4-Stage Timeline Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(8),
                              decoration: BoxDecoration(
                                color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(Icons.timer_outlined, color: ThalaivaaTheme.vegGreen, size: 18),
                            ),
                            const SizedBox(width: 10),
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: const [
                                Text('Estimated Delivery', style: TextStyle(fontSize: 11, color: Colors.grey)),
                                Text('20-25 Mins', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                              ],
                            ),
                          ],
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Text('ON TIME', style: TextStyle(color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.bold, fontSize: 11)),
                        ),
                      ],
                    ),
                    const Divider(height: 24),
                    _buildTimelineStep('1. Order Confirmed', 'Received by ${activeOrder.branch.name}', true, isDark),
                    _buildTimelineStep('2. Kitchen Preparing', 'Chef is roasting your dosas in pure desi ghee', true, isDark),
                    _buildTimelineStep('3. Out for Delivery', 'Ramesh Kumar is on the way (Bajaj Chetak EV)', false, isDark),
                    _buildTimelineStep('4. Delivered', 'Delivered at ${activeOrder.deliveryAddress}', false, isDark, isLast: true),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 2. Driver & Branch Contact Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Row(
                  children: [
                    CircleAvatar(
                      radius: 22,
                      backgroundColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                      child: const Text('🛵', style: TextStyle(fontSize: 22)),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text('Ramesh Kumar', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                          Text('Delivery Partner • 4.9 ★ (1,240 Deliveries)', style: TextStyle(fontSize: 11, color: Colors.grey)),
                        ],
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.phone_rounded, color: ThalaivaaTheme.vegGreen),
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Calling Delivery Partner: +91 98250 11223')),
                        );
                      },
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 3. Order Items Summary
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Order Summary', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    const SizedBox(height: 10),
                    ...activeOrder.items.map((item) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text('${item.quantity}x ${item.product.name}', style: const TextStyle(fontSize: 13)),
                            Text(ThalaivaaTheme.formatInr(item.totalPrice), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                          ],
                        ),
                      );
                    }).toList(),
                    const Divider(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Total Paid', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 14)),
                        Text(
                          ThalaivaaTheme.formatInr(activeOrder.grandTotal),
                          style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 15, color: ThalaivaaTheme.brandAmber),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTimelineStep(String title, String subtitle, bool isDone, bool isDark, {bool isLast = false}) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Column(
          children: [
            Container(
              width: 20,
              height: 20,
              decoration: BoxDecoration(
                color: isDone ? ThalaivaaTheme.vegGreen : (isDark ? Colors.white12 : Colors.grey.shade300),
                shape: BoxShape.circle,
              ),
              child: isDone
                  ? const Icon(Icons.check, size: 12, color: Colors.white)
                  : null,
            ),
            if (!isLast)
              Container(
                width: 2,
                height: 36,
                color: isDone ? ThalaivaaTheme.vegGreen : (isDark ? Colors.white12 : Colors.grey.shade300),
              ),
          ],
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 13,
                  color: isDone ? (isDark ? Colors.white : Colors.black87) : Colors.grey,
                ),
              ),
              Text(
                subtitle,
                style: TextStyle(fontSize: 11, color: isDark ? Colors.white54 : Colors.grey.shade600),
              ),
              if (!isLast) const SizedBox(height: 18),
            ],
          ),
        ),
      ],
    );
  }
}
