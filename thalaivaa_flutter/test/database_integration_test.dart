import 'package:flutter_test/flutter_test.dart';
import 'package:thalaivaa_flutter/models/models.dart';

void main() {
  group('Database Data Models & JSON Deserialization Tests', () {
    test('1. Deserializes Branch model from Laravel Database JSON response', () {
      final json = {
        'id': 1,
        'name': 'Thalaivaa - T. Nagar Flagship',
        'address_line': '45 South Usman Road, T. Nagar, Chennai, TN 600017',
        'phone': '+91 44 2434 8899',
        'rating': 4.8,
        'delivery_time': '25 min',
        'is_active': true,
      };

      final branch = Branch.fromJson(json);
      expect(branch.id, '1');
      expect(branch.name, 'Thalaivaa - T. Nagar Flagship');
      expect(branch.address, contains('T. Nagar'));
      expect(branch.rating, 4.8);
      expect(branch.isOpen, isTrue);
    });

    test('2. Deserializes Product model with Modifier Groups from Database JSON', () {
      final json = {
        'id': 101,
        'name': 'Ghee Roast Special Dosa',
        'category_name': 'Dosas & Crisps',
        'price_inr': 160.0,
        'rating': 4.9,
        'rating_count': 342,
        'description': 'Crispy golden crepe roasted in pure A2 desi ghee.',
        'icon_emoji': '🥞',
        'is_veg': true,
        'is_bestseller': true,
        'modifier_groups': [
          {
            'id': 'mg-1',
            'name': 'Chutney Selection',
            'min_select': 1,
            'max_select': 3,
            'options': [
              {'id': 'o-1', 'name': 'Coconut Chutney', 'price_inr': 0.0},
              {'id': 'o-2', 'name': 'Tomato Kara Chutney', 'price_inr': 0.0},
            ]
          },
          {
            'id': 'mg-2',
            'name': 'Add-ons',
            'min_select': 0,
            'max_select': 2,
            'options': [
              {'id': 'o-3', 'name': 'Extra Ghee Cup', 'price_inr': 30.0},
              {'id': 'o-4', 'name': 'Gunpowder (Podi) with Ghee', 'price_inr': 40.0},
            ]
          }
        ]
      };

      final product = Product.fromJson(json);
      expect(product.id, '101');
      expect(product.name, 'Ghee Roast Special Dosa');
      expect(product.category, 'Dosas & Crisps');
      expect(product.price, 160.0);
      expect(product.isVeg, isTrue);
      expect(product.modifierGroups.length, 2);
      expect(product.modifierGroups[0].title, 'Chutney Selection');
      expect(product.modifierGroups[0].options.length, 2);
      expect(product.modifierGroups[1].options[1].price, 40.0);
    });

    test('3. Deserializes OrderModel with items & branch from Database JSON', () {
      final json = {
        'id': 10,
        'order_number': 'ORD-98214',
        'branch_name': 'Thalaivaa - T. Nagar Flagship',
        'items': [
          {
            'id': 1,
            'product_name': 'Ghee Roast Special Dosa',
            'quantity': 2,
            'unit_price_inr': 160.0,
          }
        ],
        'total_amount_inr': 320.0,
        'status': 'out_for_delivery',
        'delivery_address': 'Flat 4B, Emerald Heights, T. Nagar, Chennai',
        'created_at': '2026-10-01T12:30:00Z',
      };

      final order = OrderModel.fromJson(json);
      expect(order.id, '10');
      expect(order.orderNumber, 'ORD-98214');
      expect(order.branch.name, 'Thalaivaa - T. Nagar Flagship');
      expect(order.items.length, 1);
      expect(order.items[0].product.name, 'Ghee Roast Special Dosa');
      expect(order.grandTotal, 320.0);
      expect(order.status, OrderStatus.outForDelivery);
      expect(order.deliveryAddress, contains('T. Nagar'));
    });

    test('4. Deserializes UserModel and Token from Authentication JSON', () {
      final json = {
        'id': 1,
        'name': 'User A (Arun Kumar)',
        'phone': '+91 98765 43210',
        'email': 'arun@thalaivaa.com',
      };

      final user = UserModel.fromJson(json, token: 'test_sanctum_token_123');
      expect(user.id, '1');
      expect(user.name, 'User A (Arun Kumar)');
      expect(user.email, 'arun@thalaivaa.com');
      expect(user.phone, '+91 98765 43210');
      expect(user.token, 'test_sanctum_token_123');
    });
  });
}
