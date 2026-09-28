import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../providers/app_providers.dart';

class CartScreen extends ConsumerStatefulWidget {
  const CartScreen({super.key});

  @override
  ConsumerState<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends ConsumerState<CartScreen> {
  final TextEditingController _couponController = TextEditingController();

  @override
  void dispose() {
    _couponController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final cart = ref.watch(cartProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    if (cart.items.isEmpty) {
      return Scaffold(
        backgroundColor: bg,
        appBar: AppBar(
          backgroundColor: cardBg,
          title: const Text('Your Food Tray', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.1),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.shopping_bag_outlined, size: 64, color: ThalaivaaTheme.brandAmber),
              ),
              const SizedBox(height: 16),
              const Text('Your Tray is Empty', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 6),
              Text(
                'Add freshly prepared dosas, idlis, and meals to start!',
                style: TextStyle(color: isDark ? Colors.white60 : Colors.black54, fontSize: 13),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  ref.read(bottomNavIndexProvider.notifier).state = 0;
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: ThalaivaaTheme.brandAmber,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Browse Menu', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Checkout & Bill Breakdown', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            Text(
              '${cart.totalItemCount} Items from ${selectedBranch.name}',
              style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber, fontWeight: FontWeight.w600),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => ref.read(cartProvider.notifier).clearCart(),
            child: const Text('Clear', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 100),
            children: [
              // 1. Delivery vs Takeaway Switcher
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: cardBorder),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: InkWell(
                        onTap: () => ref.read(cartProvider.notifier).toggleDelivery(true),
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          decoration: BoxDecoration(
                            color: cart.isDelivery ? ThalaivaaTheme.brandAmber : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.delivery_dining_rounded, size: 18, color: cart.isDelivery ? Colors.white : (isDark ? Colors.white60 : Colors.black54)),
                              const SizedBox(width: 6),
                              Text('Delivery', style: TextStyle(fontWeight: FontWeight.bold, color: cart.isDelivery ? Colors.white : (isDark ? Colors.white70 : Colors.black87))),
                            ],
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      child: InkWell(
                        onTap: () => ref.read(cartProvider.notifier).toggleDelivery(false),
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          decoration: BoxDecoration(
                            color: !cart.isDelivery ? ThalaivaaTheme.brandAmber : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.storefront_rounded, size: 18, color: !cart.isDelivery ? Colors.white : (isDark ? Colors.white60 : Colors.black54)),
                              const SizedBox(width: 6),
                              Text('Dine-in / Takeaway', style: TextStyle(fontWeight: FontWeight.bold, color: !cart.isDelivery ? Colors.white : (isDark ? Colors.white70 : Colors.black87))),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 2. Cart Items List
              Container(
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: ListView.separated(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: cart.items.length,
                  separatorBuilder: (_, __) => Divider(height: 1, color: cardBorder),
                  itemBuilder: (ctx, idx) {
                    final item = cart.items[idx];
                    return Padding(
                      padding: const EdgeInsets.all(14),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(item.product.iconEmoji, style: const TextStyle(fontSize: 24)),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(item.product.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                                if (item.selectedModifiers.isNotEmpty)
                                  Text(
                                    item.selectedModifiers.map((m) => '+ ${m.name}').join(', '),
                                    style: const TextStyle(fontSize: 11, color: ThalaivaaTheme.brandAmber),
                                  ),
                                const SizedBox(height: 4),
                                Text(
                                  ThalaivaaTheme.formatInr(item.unitPrice),
                                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: ThalaivaaTheme.brandAmber),
                                ),
                              ],
                            ),
                          ),
                          Container(
                            decoration: BoxDecoration(
                              color: isDark ? const Color(0xFF10141D) : const Color(0xFFF1F5F9),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: cardBorder),
                            ),
                            child: Row(
                              children: [
                                InkWell(
                                  onTap: () => ref.read(cartProvider.notifier).updateQuantity(item.id, -1),
                                  child: const Padding(
                                    padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    child: Icon(Icons.remove, size: 16, color: ThalaivaaTheme.brandAmber),
                                  ),
                                ),
                                Text('${item.quantity}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                                InkWell(
                                  onTap: () => ref.read(cartProvider.notifier).updateQuantity(item.id, 1),
                                  child: const Padding(
                                    padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    child: Icon(Icons.add, size: 16, color: ThalaivaaTheme.brandAmber),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),

              const SizedBox(height: 16),

              // 3. Coupon Promo Code Box
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.discount_rounded, color: ThalaivaaTheme.brandAmber, size: 18),
                        SizedBox(width: 8),
                        Text('Apply Promo Coupon', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                      ],
                    ),
                    const SizedBox(height: 10),
                    if (cart.appliedCoupon != null)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        decoration: BoxDecoration(
                          color: ThalaivaaTheme.vegGreen.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: ThalaivaaTheme.vegGreen),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              'Coupon ${cart.appliedCoupon} applied (-₹${cart.discountAmount.toInt()})',
                              style: const TextStyle(color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold, fontSize: 12),
                            ),
                            InkWell(
                              onTap: () => ref.read(cartProvider.notifier).removeCoupon(),
                              child: const Text('REMOVE', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold, fontSize: 11)),
                            ),
                          ],
                        ),
                      )
                    else
                      Row(
                        children: [
                          Expanded(
                            child: TextField(
                              controller: _couponController,
                              textCapitalization: TextCapitalization.characters,
                              decoration: InputDecoration(
                                hintText: 'Enter THALAIVAA50 or FEAST100',
                                hintStyle: TextStyle(fontSize: 12, color: isDark ? Colors.white38 : Colors.black38),
                                isDense: true,
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                                contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                          ElevatedButton(
                            onPressed: () {
                              final success = ref.read(cartProvider.notifier).applyCoupon(_couponController.text);
                              if (!success) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text('Invalid coupon code or minimum order not met!'),
                                    backgroundColor: Colors.redAccent,
                                  ),
                                );
                              }
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: ThalaivaaTheme.brandAmber,
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                            ),
                            child: const Text('APPLY', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                          ),
                        ],
                      ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 4. Delivery Partner Tip Selector
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Tip your Delivery Partner', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    const SizedBox(height: 4),
                    Text('100% of the tip goes directly to your delivery partner', style: TextStyle(fontSize: 11, color: isDark ? Colors.white60 : Colors.black54)),
                    const SizedBox(height: 10),
                    Row(
                      children: [0.0, 20.0, 30.0, 50.0].map((tip) {
                        final isSel = cart.tipAmount == tip;
                        return Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: ChoiceChip(
                            label: Text(tip == 0.0 ? 'No Tip' : '₹${tip.toInt()}'),
                            selected: isSel,
                            selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                            onSelected: (_) => ref.read(cartProvider.notifier).setTip(tip),
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // 5. Itemized Bill Summary
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
                    const Text('Bill Details', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Item Total', style: TextStyle(fontSize: 13)),
                        Text(ThalaivaaTheme.formatInr(cart.subtotal), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('GST & Restaurant Tax (5%)', style: TextStyle(fontSize: 13)),
                        Text(ThalaivaaTheme.formatInr(cart.tax), style: const TextStyle(fontSize: 13)),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Delivery Fee ${cart.subtotal > 499 ? "(Free above ₹499)" : ""}', style: const TextStyle(fontSize: 13)),
                        Text(
                          cart.deliveryFee == 0 ? 'FREE' : ThalaivaaTheme.formatInr(cart.deliveryFee),
                          style: TextStyle(
                            fontSize: 13,
                            color: cart.deliveryFee == 0 ? ThalaivaaTheme.vegGreen : null,
                            fontWeight: cart.deliveryFee == 0 ? FontWeight.bold : FontWeight.normal,
                          ),
                        ),
                      ],
                    ),
                    if (cart.tipAmount > 0) ...[
                      const SizedBox(height: 6),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Delivery Tip', style: TextStyle(fontSize: 13)),
                          Text(ThalaivaaTheme.formatInr(cart.tipAmount), style: const TextStyle(fontSize: 13)),
                        ],
                      ),
                    ],
                    if (cart.discountAmount > 0) ...[
                      const SizedBox(height: 6),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Coupon Discount', style: TextStyle(fontSize: 13, color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold)),
                          Text('-${ThalaivaaTheme.formatInr(cart.discountAmount)}', style: const TextStyle(fontSize: 13, color: ThalaivaaTheme.vegGreen, fontWeight: FontWeight.bold)),
                        ],
                      ),
                    ],
                    const Divider(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('To Pay', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
                        Text(
                          ThalaivaaTheme.formatInr(cart.grandTotal),
                          style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 18, color: ThalaivaaTheme.brandAmber),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),

              // 6. Checkout CTA
              ElevatedButton(
                onPressed: () {
                  ref.read(ordersProvider.notifier).placeOrder(cart, selectedBranch);
                  ref.read(cartProvider.notifier).clearCart();
                  ref.read(bottomNavIndexProvider.notifier).state = 2; // Switch to Orders tab
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('🎉 Order Confirmed! Live tracking started.'),
                      backgroundColor: ThalaivaaTheme.vegGreen,
                      behavior: SnackBarBehavior.floating,
                    ),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: ThalaivaaTheme.brandAmber,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('PLACE ORDER • ', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 15)),
                    Text(
                      ThalaivaaTheme.formatInr(cart.grandTotal),
                      style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 16),
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
}
