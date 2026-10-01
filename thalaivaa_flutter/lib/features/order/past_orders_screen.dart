import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../models/models.dart';
import '../../providers/app_providers.dart';

class PastOrdersScreen extends ConsumerWidget {
  const PastOrdersScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider);
    final orders = ref.watch(ordersProvider);
    final isLoading = ref.watch(ordersLoadingProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        title: const Text('Past Orders & History', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: user == null
              ? _buildUnauthenticatedState(context, ref, isDark)
              : isLoading
                  ? const Center(child: CircularProgressIndicator(color: ThalaivaaTheme.brandAmber))
                  : orders.isEmpty
                      ? _buildEmptyState(context, ref, isDark, user)
                      : ListView.builder(
                          padding: const EdgeInsets.all(16),
                          itemCount: orders.length,
                          itemBuilder: (context, index) {
                            final order = orders[index];
                            return _buildOrderCard(context, ref, order, cardBg, cardBorder, isDark);
                          },
                        ),
        ),
      ),
    );
  }

  Widget _buildUnauthenticatedState(BuildContext context, WidgetRef ref, bool isDark) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.12),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.lock_person_rounded, size: 56, color: ThalaivaaTheme.brandAmber),
          ),
          const SizedBox(height: 16),
          const Text('Please Sign In', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
          const SizedBox(height: 8),
          const Text('Sign in to view your complete database order history.', style: TextStyle(color: Colors.grey, fontSize: 13)),
        ],
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context, WidgetRef ref, bool isDark, UserModel user) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: isDark ? Colors.white10 : const Color(0xFFF1F5F9),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.receipt_long_outlined, size: 60, color: Colors.grey),
            ),
            const SizedBox(height: 16),
            const Text('No Past Orders Found', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 6),
            Text('Account: ${user.name} (${user.email.isNotEmpty ? user.email : user.phone})', style: const TextStyle(fontSize: 12, color: Colors.grey)),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.of(context).pop();
                ref.read(bottomNavIndexProvider.notifier).state = 0; // Go to Menu
              },
              icon: const Icon(Icons.restaurant_menu_rounded, size: 16),
              label: const Text('Explore Menu & Order', style: TextStyle(fontWeight: FontWeight.bold)),
              style: ElevatedButton.styleFrom(
                backgroundColor: ThalaivaaTheme.brandAmber,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOrderCard(BuildContext context, WidgetRef ref, OrderModel order, Color cardBg, Color cardBorder, bool isDark) {
    final statusColor = _getStatusColor(order.status);
    final statusLabel = _getStatusLabel(order.status);
    final isDelivered = order.status == OrderStatus.delivered;

    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: cardBorder),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: isDark ? 0.25 : 0.03),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Order Header (ID, Date, Status Badge)
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Order #${order.orderNumber}',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        '${order.createdAt.day}/${order.createdAt.month}/${order.createdAt.year} • ${order.branch.name}',
                        style: TextStyle(color: isDark ? Colors.white60 : Colors.black54, fontSize: 11),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: statusColor.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: statusColor),
                  ),
                  child: Text(
                    statusLabel.toUpperCase(),
                    style: TextStyle(color: statusColor, fontSize: 10, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            const Divider(height: 1),
            const SizedBox(height: 10),

            // Items Summary
            if (order.items.isNotEmpty) ...[
              ...order.items.map((item) {
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 3),
                  child: Row(
                    children: [
                      Text(
                        '${item.quantity}x',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: ThalaivaaTheme.brandAmber),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          item.product.name,
                          style: const TextStyle(fontSize: 13),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        ThalaivaaTheme.formatInr(item.totalPrice),
                        style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                );
              }),
            ] else ...[
              Text('Authentic South Indian Meal Combo', style: TextStyle(fontSize: 12, color: isDark ? Colors.white70 : Colors.black87)),
            ],

            const SizedBox(height: 10),
            const Divider(height: 1),
            const SizedBox(height: 10),

            // Total and Action Buttons
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Total Amount', style: TextStyle(fontSize: 10, color: Colors.grey)),
                    Text(
                      ThalaivaaTheme.formatInr(order.grandTotal),
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: ThalaivaaTheme.brandAmber),
                    ),
                  ],
                ),
                if (!isDelivered)
                  OutlinedButton.icon(
                    onPressed: () {
                      // Track Live Order: select this order and switch to Tab 2
                      ref.read(selectedOrderProvider.notifier).state = order;
                      Navigator.of(context).pop();
                      ref.read(bottomNavIndexProvider.notifier).state = 2; // Switch to Order tab
                    },
                    icon: const Icon(Icons.delivery_dining_rounded, size: 16, color: ThalaivaaTheme.brandAmber),
                    label: const Text('Live Tracking', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: ThalaivaaTheme.brandAmber)),
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: ThalaivaaTheme.brandAmber),
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                  )
                else
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                      color: Colors.green.withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.green.withValues(alpha: 0.4)),
                    ),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.check_circle_rounded, color: Colors.green, size: 14),
                        SizedBox(width: 4),
                        Text('Delivered', style: TextStyle(color: Colors.green, fontSize: 11, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Color _getStatusColor(OrderStatus status) {
    switch (status) {
      case OrderStatus.confirmed:
        return ThalaivaaTheme.brandAmber;
      case OrderStatus.preparing:
        return const Color(0xFF3B82F6);
      case OrderStatus.outForDelivery:
        return const Color(0xFF8B5CF6);
      case OrderStatus.delivered:
        return Colors.green;
      case OrderStatus.placed:
      default:
        return Colors.orange;
    }
  }

  String _getStatusLabel(OrderStatus status) {
    switch (status) {
      case OrderStatus.confirmed:
        return 'Confirmed';
      case OrderStatus.preparing:
        return 'Preparing';
      case OrderStatus.outForDelivery:
        return 'Out for Delivery';
      case OrderStatus.delivered:
        return 'Delivered';
      case OrderStatus.placed:
      default:
        return 'Placed';
    }
  }
}
