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

  factory ModifierOption.fromJson(Map<String, dynamic> json) {
    return ModifierOption(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      price: (json['price_inr'] as num?)?.toDouble() ?? (((json['price_adjustment'] ?? json['price']) as num?)?.toDouble() ?? 0.0) / 100.0,
    );
  }
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

  factory ModifierGroup.fromJson(Map<String, dynamic> json) {
    final rawOptions = json['options'] as List<dynamic>? ?? [];
    return ModifierGroup(
      id: json['id']?.toString() ?? '',
      title: json['name']?.toString() ?? (json['title']?.toString() ?? ''),
      minSelect: (json['min_select'] as num?)?.toInt() ?? 0,
      maxSelect: (json['max_select'] as num?)?.toInt() ?? 1,
      options: rawOptions.map((o) => ModifierOption.fromJson(o)).toList(),
    );
  }
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

  factory Product.fromJson(Map<String, dynamic> json) {
    final rawModGroups = json['modifier_groups'] as List<dynamic>? ?? [];
    final pInr = (json['price_inr'] as num?)?.toDouble() ?? (((json['base_price_paise'] ?? json['base_price']) as num?)?.toDouble() ?? 0.0) / 100.0;
    return Product(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      description: json['description']?.toString() ?? '',
      price: pInr > 0 ? pInr : ((json['price'] as num?)?.toDouble() ?? 0.0),
      category: json['category_name']?.toString() ?? (json['category']?.toString() ?? 'South Indian Specialties'),
      iconEmoji: json['icon_emoji']?.toString() ?? (json['emoji']?.toString() ?? '🍲'),
      isVeg: json['is_veg'] == true || json['is_veg'] == 1,
      isBestseller: json['is_bestseller'] == true || json['is_bestseller'] == 1 || ((json['rating'] as num?)?.toDouble() ?? 0) >= 4.9,
      rating: (json['rating'] as num?)?.toDouble() ?? 4.8,
      ratingCount: (json['rating_count'] as num?)?.toInt() ?? 120,
      modifierGroups: rawModGroups.map((g) => ModifierGroup.fromJson(g)).toList(),
    );
  }
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

  factory Branch.fromJson(Map<String, dynamic> json) {
    return Branch(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      address: json['address_line']?.toString() ?? (json['address']?.toString() ?? 'Surat, Gujarat'),
      phone: json['phone']?.toString() ?? '+91 92170 02598',
      isOpen: json['is_active'] == true || json['is_active'] == 1,
      rating: (json['rating'] as num?)?.toDouble() ?? 4.9,
      deliveryTime: json['delivery_time']?.toString() ?? '20-25 min',
    );
  }
}

enum OrderStatus {
  placed,
  confirmed,
  preparing,
  outForDelivery,
  delivered,
}

OrderStatus parseOrderStatus(String? s) {
  switch (s?.toLowerCase()) {
    case 'confirmed':
      return OrderStatus.confirmed;
    case 'preparing':
      return OrderStatus.preparing;
    case 'out_for_delivery':
      return OrderStatus.outForDelivery;
    case 'delivered':
      return OrderStatus.delivered;
    case 'placed':
    case 'pending':
    default:
      return OrderStatus.placed;
  }
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

  factory OrderModel.fromJson(Map<String, dynamic> json) {
    final rawItems = json['items'] as List<dynamic>? ?? [];
    final itemsList = rawItems.map((itemJson) {
      final pName = itemJson['product_name'] ?? 'South Indian Specialty';
      final qty = (itemJson['quantity'] as num?)?.toInt() ?? 1;
      final unitPrice = (itemJson['unit_price_inr'] as num?)?.toDouble() ?? 0.0;
      return CartItem(
        id: itemJson['id']?.toString() ?? 'ci-${DateTime.now().microsecondsSinceEpoch}',
        product: Product(
          id: itemJson['id']?.toString() ?? 'p-gen',
          name: pName,
          description: 'Authentic South Indian preparation',
          price: unitPrice,
          category: 'South Indian Specialties',
          iconEmoji: '🍲',
        ),
        quantity: qty,
      );
    }).toList();

    final totalInr = (json['total_amount_inr'] as num?)?.toDouble() ?? 0.0;

    return OrderModel(
      id: json['id']?.toString() ?? '',
      orderNumber: json['order_number']?.toString() ?? '',
      items: itemsList,
      subtotal: totalInr,
      tax: 0.0,
      deliveryFee: 0.0,
      discount: 0.0,
      grandTotal: totalInr,
      status: parseOrderStatus(json['status']?.toString()),
      createdAt: json['created_at'] != null ? (DateTime.tryParse(json['created_at']) ?? DateTime.now()) : DateTime.now(),
      branch: Branch(
        id: 'br-1',
        name: json['branch_name']?.toString() ?? 'Thalaivaa - City Light (Main)',
        address: 'Surat, Gujarat',
        phone: '+91 92170 02598',
      ),
      deliveryAddress: json['delivery_address']?.toString() ?? 'Surat, Gujarat',
    );
  }

  OrderModel copyWith({
    String? id,
    String? orderNumber,
    List<CartItem>? items,
    double? subtotal,
    double? tax,
    double? deliveryFee,
    double? discount,
    double? grandTotal,
    OrderStatus? status,
    DateTime? createdAt,
    Branch? branch,
    String? deliveryAddress,
  }) {
    return OrderModel(
      id: id ?? this.id,
      orderNumber: orderNumber ?? this.orderNumber,
      items: items ?? this.items,
      subtotal: subtotal ?? this.subtotal,
      tax: tax ?? this.tax,
      deliveryFee: deliveryFee ?? this.deliveryFee,
      discount: discount ?? this.discount,
      grandTotal: grandTotal ?? this.grandTotal,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      branch: branch ?? this.branch,
      deliveryAddress: deliveryAddress ?? this.deliveryAddress,
    );
  }
}

@immutable
class UserModel {
  final String id;
  final String name;
  final String email;
  final String phone;
  final String? token;

  const UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.phone,
    this.token,
  });

  factory UserModel.fromJson(Map<String, dynamic> json, {String? token}) {
    return UserModel(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      email: json['email']?.toString() ?? '',
      phone: json['phone']?.toString() ?? '',
      token: token ?? json['token']?.toString(),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'email': email,
    'phone': phone,
    if (token != null) 'token': token,
  };
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
