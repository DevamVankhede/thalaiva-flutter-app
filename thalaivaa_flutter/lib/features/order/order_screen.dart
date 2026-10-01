import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../models/models.dart';
import '../../providers/app_providers.dart';
import 'past_orders_screen.dart';

class OrderScreen extends ConsumerStatefulWidget {
  const OrderScreen({super.key});

  @override
  ConsumerState<OrderScreen> createState() => _OrderScreenState();
}

class _OrderScreenState extends ConsumerState<OrderScreen> {
  OrderModel? _selectedOrder;

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(authProvider);
    final orders = ref.watch(ordersProvider);
    final isLoading = ref.watch(ordersLoadingProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    // If unauthenticated state
    if (user == null) {
      return Scaffold(
        backgroundColor: bg,
        appBar: AppBar(
          backgroundColor: cardBg,
          title: const Text('My Orders', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        ),
        body: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 500),
            child: Padding(
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
                  const SizedBox(height: 18),
                  const Text('Authentication Required', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                  const SizedBox(height: 8),
                  const Text(
                    'Please sign in with your account to view your real-time database orders and tracking history.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 13, color: Colors.grey),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton.icon(
                    onPressed: () {
                      ref.read(bottomNavIndexProvider.notifier).state = 3; // Switch to Profile tab
                    },
                    icon: const Icon(Icons.login_rounded, size: 16),
                    label: const Text('Go to Login Screen', style: TextStyle(fontWeight: FontWeight.bold)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: ThalaivaaTheme.brandAmber,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      );
    }

    // Authenticated state with 0 orders (User C)
    if (orders.isEmpty && !isLoading) {
      return Scaffold(
        backgroundColor: bg,
        appBar: AppBar(
          backgroundColor: cardBg,
          title: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('My Orders', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Text('Welcome, ${user.name}', style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber)),
            ],
          ),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: isDark ? Colors.white10 : const Color(0xFFF1F5F9),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.receipt_long_outlined, size: 64, color: Colors.grey),
              ),
              const SizedBox(height: 16),
              const Text('No orders found.', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              const SizedBox(height: 8),
              Text(
                'Account: ${user.email.isNotEmpty ? user.email : user.phone}',
                style: const TextStyle(fontSize: 12, color: Colors.grey),
              ),
              const SizedBox(height: 6),
              const Text('You haven\'t placed any orders yet.\nExplore our delicious South Indian menu!', textAlign: TextAlign.center, style: TextStyle(fontSize: 13, color: Colors.grey)),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: () {
                  ref.read(bottomNavIndexProvider.notifier).state = 0; // Go to Menu
                },
                icon: const Icon(Icons.restaurant_menu_rounded, size: 16),
                label: const Text('Browse Menu', style: TextStyle(fontWeight: FontWeight.bold)),
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

    final globalSelectedOrder = ref.watch(selectedOrderProvider);
    final activeOrder = globalSelectedOrder ?? _selectedOrder ?? orders.first;

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('My Orders & Live Tracking', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            Text('Welcome, ${user.name}', style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.w600)),
          ],
        ),
        actions: [
          TextButton.icon(
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const PastOrdersScreen()),
              );
            },
            icon: const Icon(Icons.history_rounded, size: 18, color: ThalaivaaTheme.brandAmber),
            label: const Text('Past Orders', style: TextStyle(color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.bold, fontSize: 12)),
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              // 1. Active Order Header Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: cardBorder),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Order #${activeOrder.orderNumber}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                        const SizedBox(height: 3),
                        Text(activeOrder.branch.name, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                      ],
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                      decoration: BoxDecoration(
                        color: _statusColor(activeOrder.status).withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: _statusColor(activeOrder.status)),
                      ),
                      child: Text(
                        _statusLabel(activeOrder.status).toUpperCase(),
                        style: TextStyle(color: _statusColor(activeOrder.status), fontWeight: FontWeight.bold, fontSize: 11),
                      ),
                    ),
                  ],
                ),
              ),

              if (orders.length > 1) ...[
                const SizedBox(height: 10),
                InkWell(
                  borderRadius: BorderRadius.circular(10),
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const PastOrdersScreen()),
                    );
                  },
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                    decoration: BoxDecoration(
                      color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.08),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.25)),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Row(
                            children: [
                              const Icon(Icons.receipt_long_rounded, color: ThalaivaaTheme.brandAmber, size: 16),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  'Active Order (${orders.length} orders found in database)',
                                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 8),
                        Row(
                          mainAxisSize: MainAxisSize.min,
                          children: const [
                            Text('See All Past Orders', style: TextStyle(color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.bold, fontSize: 12)),
                            SizedBox(width: 4),
                            Icon(Icons.arrow_forward_ios_rounded, size: 12, color: ThalaivaaTheme.brandAmber),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ],

              const SizedBox(height: 14),

              // 3. Live 4-Stage Timeline Card
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
                        Expanded(
                          child: Row(
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
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const Text('Estimated Delivery', style: TextStyle(fontSize: 11, color: Colors.grey)),
                                    Text(
                                      _getDynamicEta(activeOrder.status),
                                      style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            _getEtaStatusBadge(activeOrder.status),
                            style: const TextStyle(color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.bold, fontSize: 11),
                          ),
                        ),
                      ],
                    ),
                    const Divider(height: 24),
                    _buildTimelineStep(
                      '1. Order Confirmed',
                      'Received by ${activeOrder.branch.name}',
                      true,
                      isDark,
                    ),
                    _buildTimelineStep(
                      '2. Kitchen Preparing',
                      'Chef is roasting your dosas in pure desi ghee',
                      activeOrder.status == OrderStatus.preparing || activeOrder.status == OrderStatus.outForDelivery || activeOrder.status == OrderStatus.delivered,
                      isDark,
                    ),
                    _buildTimelineStep(
                      '3. Out for Delivery',
                      activeOrder.status == OrderStatus.outForDelivery || activeOrder.status == OrderStatus.delivered
                          ? 'Ramesh Kumar is on the way (Bajaj Chetak EV)'
                          : 'Delivery partner will be assigned once packed',
                      activeOrder.status == OrderStatus.outForDelivery || activeOrder.status == OrderStatus.delivered,
                      isDark,
                    ),
                    _buildTimelineStep(
                      '4. Delivered',
                      'Delivered at ${activeOrder.deliveryAddress}',
                      activeOrder.status == OrderStatus.delivered,
                      isDark,
                      isLast: true,
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 4. Driver & Branch Contact Card
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
                      child: Text(
                        activeOrder.status == OrderStatus.outForDelivery || activeOrder.status == OrderStatus.delivered ? '🛵' : '👨‍🍳',
                        style: const TextStyle(fontSize: 22),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            activeOrder.status == OrderStatus.outForDelivery || activeOrder.status == OrderStatus.delivered
                                ? 'Ramesh Kumar'
                                : 'Assigning Delivery Partner',
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const SizedBox(height: 2),
                          Text(
                            activeOrder.status == OrderStatus.outForDelivery || activeOrder.status == OrderStatus.delivered
                                ? 'Delivery Partner • 4.9 ★ (1,240 Deliveries)'
                                : 'Chef is preparing your fresh meal',
                            style: TextStyle(fontSize: 11, color: isDark ? Colors.white60 : Colors.black54),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                    ),
                    if (activeOrder.status == OrderStatus.outForDelivery || activeOrder.status == OrderStatus.delivered)
                      IconButton(
                        icon: const Icon(Icons.phone_rounded, color: ThalaivaaTheme.vegGreen),
                        onPressed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Calling Delivery Partner: +91 98250 11223')),
                          );
                        },
                      )
                    else
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Text('Preparing', style: TextStyle(color: ThalaivaaTheme.brandAmber, fontSize: 10, fontWeight: FontWeight.bold)),
                      ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 5. Order Items Summary
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
                            Expanded(
                              child: Text(
                                '${item.quantity}x ${item.product.name}',
                                style: const TextStyle(fontSize: 13),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            const SizedBox(width: 8),
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

  String _getDynamicEta(OrderStatus status) {
    switch (status) {
      case OrderStatus.confirmed:
        return '20-25 Mins';
      case OrderStatus.preparing:
        return '12-15 Mins';
      case OrderStatus.outForDelivery:
        return '5-8 Mins';
      case OrderStatus.delivered:
        return 'Delivered';
      case OrderStatus.placed:
      default:
        return '25-30 Mins';
    }
  }

  String _getEtaStatusBadge(OrderStatus status) {
    switch (status) {
      case OrderStatus.delivered:
        return 'COMPLETED';
      case OrderStatus.outForDelivery:
        return 'ARRIVING';
      case OrderStatus.preparing:
        return 'IN KITCHEN';
      case OrderStatus.confirmed:
      default:
        return 'ON TIME';
    }
  }

  Color _statusColor(OrderStatus status) {
    switch (status) {
      case OrderStatus.delivered:
        return Colors.green;
      case OrderStatus.outForDelivery:
        return Colors.blue;
      case OrderStatus.preparing:
        return ThalaivaaTheme.brandAmber;
      case OrderStatus.confirmed:
      case OrderStatus.placed:
      default:
        return Colors.orange;
    }
  }

  String _statusLabel(OrderStatus status) {
    switch (status) {
      case OrderStatus.delivered:
        return 'Delivered';
      case OrderStatus.outForDelivery:
        return 'Out For Delivery';
      case OrderStatus.preparing:
        return 'Preparing';
      case OrderStatus.confirmed:
        return 'Confirmed';
      case OrderStatus.placed:
      default:
        return 'Placed';
    }
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
