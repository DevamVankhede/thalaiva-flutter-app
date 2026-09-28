import 'package:flutter/foundation.dart';

@immutable
class ModifierOption {
  final String id;
  final String name;
  final double price;

  const ModifierOption({
    required this.id,
    required this.name,
    required this.price,
  });
}

@immutable
class ModifierGroup {
  final String id;
  final String title;
  final int minSelect;
  final int maxSelect;
  final List<ModifierOption> options;

  const ModifierGroup({
    required this.id,
    required this.title,
    this.minSelect = 0,
    this.maxSelect = 1,
    required this.options,
  });
}

@immutable
class Product {
  final String id;
  final String name;
  final String description;
  final double price;
  final String category;
  final String iconEmoji;
  final bool isVeg;
  final bool isBestseller;
  final double rating;
  final int ratingCount;
  final List<ModifierGroup> modifierGroups;

  const Product({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.category,
    required this.iconEmoji,
    this.isVeg = true,
    this.isBestseller = false,
    this.rating = 4.8,
    this.ratingCount = 120,
    this.modifierGroups = const [],
  });
}

@immutable
class CartItem {
  final String id;
  final Product product;
  final int quantity;
  final List<ModifierOption> selectedModifiers;
  final String? instructions;

  const CartItem({
    required this.id,
    required this.product,
    this.quantity = 1,
    this.selectedModifiers = const [],
    this.instructions,
  });

  double get unitPrice {
    double total = product.price;
    for (final mod in selectedModifiers) {
      total += mod.price;
    }
    return total;
  }

  double get totalPrice => unitPrice * quantity;

  CartItem copyWith({
    int? quantity,
    List<ModifierOption>? selectedModifiers,
    String? instructions,
  }) {
    return CartItem(
      id: id,
      product: product,
      quantity: quantity ?? this.quantity,
      selectedModifiers: selectedModifiers ?? this.selectedModifiers,
      instructions: instructions ?? this.instructions,
    );
  }
}

@immutable
class Branch {
  final String id;
  final String name;
  final String address;
  final String phone;
  final bool isOpen;
  final double rating;
  final String deliveryTime;

  const Branch({
    required this.id,
    required this.name,
    required this.address,
    required this.phone,
    this.isOpen = true,
    this.rating = 4.9,
    this.deliveryTime = '25-30 min',
  });
}

enum OrderStatus {
  placed,
  confirmed,
  preparing,
  outForDelivery,
  delivered,
}

@immutable
class OrderModel {
  final String id;
  final String orderNumber;
  final List<CartItem> items;
  final double subtotal;
  final double tax;
  final double deliveryFee;
  final double discount;
  final double grandTotal;
  final OrderStatus status;
  final DateTime createdAt;
  final Branch branch;
  final String deliveryAddress;

  const OrderModel({
    required this.id,
    required this.orderNumber,
    required this.items,
    required this.subtotal,
    required this.tax,
    required this.deliveryFee,
    required this.discount,
    required this.grandTotal,
    required this.status,
    required this.createdAt,
    required this.branch,
    required this.deliveryAddress,
  });
}

@immutable
class Coupon {
  final String id;
  final String code;
  final double discountAmount;
  final String description;
  final bool isActive;

  const Coupon({
    required this.id,
    required this.code,
    required this.discountAmount,
    required this.description,
    this.isActive = true,
  });
}
