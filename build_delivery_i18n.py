# Build complete Delivery and Multi-Language (i18n) Engine across Flutter app
import os
import sys

# 1. Write app_providers.dart
app_providers_path = r'C:\Users\Admin\thalaivaa_flutter\lib\providers\app_providers.dart'

APP_PROVIDERS_CODE = r'''import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/models.dart';

// ==========================================
// 1. DELIVERY & BRANCH MODELS & PROVIDERS
// ==========================================

class DeliveryAddress {
  final String id;
  final String label; // Home, Work, Other
  final String addressLine;
  final String landmark;
  final String pincode;
  final bool isDefault;

  const DeliveryAddress({
    required this.id,
    required this.label,
    required this.addressLine,
    required this.landmark,
    required this.pincode,
    this.isDefault = false,
  });
}

final savedAddressesProvider = Provider<List<DeliveryAddress>>((ref) {
  return const [
    DeliveryAddress(
      id: 'addr-1',
      label: 'Home',
      addressLine: 'Flat 402, SNS Atria, VIP Road, Vesu',
      landmark: 'Near Rahul Raj Mall, Surat',
      pincode: '395007',
      isDefault: true,
    ),
    DeliveryAddress(
      id: 'addr-2',
      label: 'Work',
      addressLine: '204, Milestone Temple Building, City Light Town',
      landmark: 'Opposite Science Centre, Surat',
      pincode: '395007',
    ),
    DeliveryAddress(
      id: 'addr-3',
      label: 'Other',
      addressLine: 'Shop 8, Prime Arcade, L.P. Savani Road, Adajan',
      landmark: 'Near Honey Park, Surat',
      pincode: '395009',
    ),
  ];
});

final selectedAddressProvider = StateProvider<DeliveryAddress>((ref) {
  final list = ref.watch(savedAddressesProvider);
  return list.first;
});

enum OrderType { delivery, takeaway, dineIn }
final orderTypeProvider = StateProvider<OrderType>((ref) => OrderType.delivery);

// Delivery Instructions (Multi-select)
final deliveryInstructionsProvider = StateProvider<Set<String>>((ref) => <String>{});
final contactlessDeliveryProvider = StateProvider<bool>((ref) => false);

// Delivery Partner Details
class DeliveryRider {
  final String name;
  final String phone;
  final String vehicle;
  final double rating;
  final int completedTrips;
  final String photoEmoji;

  const DeliveryRider({
    required this.name,
    required this.phone,
    required this.vehicle,
    required this.rating,
    required this.completedTrips,
    required this.photoEmoji,
  });
}

final activeRiderProvider = Provider<DeliveryRider>((ref) {
  return const DeliveryRider(
    name: 'Ramesh Patel',
    phone: '+91 98250 11223',
    vehicle: 'TVS Jupiter EV • GJ-05-KN-8821',
    rating: 4.9,
    completedTrips: 1420,
    photoEmoji: '🛵',
  );
});

// Live Tracking Stages
enum LiveTrackingStage { confirmed, preparing, onTheWay, delivered }
final liveTrackingStageProvider = StateProvider<LiveTrackingStage>((ref) => LiveTrackingStage.onTheWay);
final etaMinutesProvider = StateProvider<int>((ref) => 18);

// Branches Provider (Surat Locations)
final branchesProvider = Provider<List<Branch>>((ref) {
  return const [
    Branch(
      id: 'br-1',
      name: 'Thalaivaa - City Light (Main)',
      address: 'Shop 12-14, City Light Town, Surat, Gujarat 395007',
      phone: '+91 92170 02598',
      rating: 4.9,
      deliveryTime: '20-25 min',
    ),
    Branch(
      id: 'br-2',
      name: 'Thalaivaa - Vesu Branch',
      address: 'VIP Road, Vesu, Surat, Gujarat 395007',
      phone: '+91 92170 02599',
      rating: 4.8,
      deliveryTime: '30-35 min',
    ),
    Branch(
      id: 'br-3',
      name: 'Thalaivaa - Adajan Hub',
      address: 'L.P. Savani Road, Adajan, Surat, Gujarat 395009',
      phone: '+91 92170 02600',
      rating: 4.7,
      deliveryTime: '25-30 min',
    ),
  ];
});

final selectedBranchProvider = StateProvider<Branch>((ref) {
  final branches = ref.watch(branchesProvider);
  return branches.first;
});

// ==========================================
// 2. 30 AUTHENTIC SOUTH INDIAN PRODUCTS
// ==========================================
final sampleProducts = <Product>[
  // --- DOSAS (6) ---
  const Product(
    id: 'p-1',
    name: 'Ghee Roast Masala Dosa',
    description: 'Crispy golden crepe roasted in pure desi ghee, stuffed with seasoned spiced potato masala.',
    price: 180.0,
    category: 'Dosas',
    iconEmoji: '🥞',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 420,
    modifierGroups: [
      ModifierGroup(
        id: 'mg-1',
        title: 'Accompaniments & Ghee Extras',
        minSelect: 0,
        maxSelect: 3,
        options: [
          ModifierOption(id: 'mo-1', name: 'Extra Desi Ghee Topping', price: 30.0),
          ModifierOption(id: 'mo-2', name: 'Gunpowder Podi Spice', price: 25.0),
          ModifierOption(id: 'mo-3', name: 'Extra Coconut & Tomato Chutney', price: 20.0),
        ],
      ),
    ],
  ),
  const Product(
    id: 'p-2',
    name: 'Mysore Cheese Burst Dosa',
    description: 'Spicy red garlic-chutney smeared crepe overflowing with molten mozzarella cheese & spiced veggies.',
    price: 240.0,
    category: 'Dosas',
    iconEmoji: '🧀',
    isVeg: true,
    isBestseller: true,
    rating: 4.8,
    ratingCount: 290,
    modifierGroups: [
      ModifierGroup(
        id: 'mg-2',
        title: 'Cheese Level',
        options: [
          ModifierOption(id: 'mo-4', name: 'Double Mozzarella', price: 40.0),
          ModifierOption(id: 'mo-5', name: 'Jalapeno & Chili Flakes', price: 20.0),
        ],
      ),
    ],
  ),
  const Product(
    id: 'p-3',
    name: 'Rava Onion Masala Dosa',
    description: 'Semolina-rice batter laced with finely chopped shallots, crushed cumin, and whole cashews.',
    price: 190.0,
    category: 'Dosas',
    iconEmoji: '🥞',
    isVeg: true,
    isBestseller: false,
    rating: 4.7,
    ratingCount: 175,
  ),
  const Product(
    id: 'p-4',
    name: 'Podi Ghee Karam Dosa',
    description: 'Crunchy crepe generously dusted with fiery Gunpowder Podi and sizzling hot cow ghee.',
    price: 210.0,
    category: 'Dosas',
    iconEmoji: '🌶️',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 310,
  ),
  const Product(
    id: 'p-5',
    name: 'Paper Plain Roast Dosa (2.5 Ft)',
    description: 'Ultra-thin, mega crispy golden paper dosa served with trio of artisanal coastal chutneys.',
    price: 160.0,
    category: 'Dosas',
    iconEmoji: '📜',
    isVeg: true,
    isBestseller: false,
    rating: 4.6,
    ratingCount: 140,
  ),
  const Product(
    id: 'p-6',
    name: 'Chettinad Paneer Tikka Dosa',
    description: 'Fusion crepe layered with smoky roasted paneer cubes tossed in fiery Chettinad pepper masala.',
    price: 260.0,
    category: 'Dosas',
    iconEmoji: '🍛',
    isVeg: true,
    isBestseller: false,
    rating: 4.8,
    ratingCount: 215,
  ),

  // --- IDLIS & VADAS (5) ---
  const Product(
    id: 'p-7',
    name: 'Steamed Button Ghee Idli (14 Pcs)',
    description: 'Bite-sized melt-in-mouth rice dumplings floating in steaming hot Drumstick Sambar and ghee.',
    price: 140.0,
    category: 'Idlis & Vadas',
    iconEmoji: '⚪',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 512,
  ),
  const Product(
    id: 'p-8',
    name: 'Medu Vada Duo with Sambar Dip',
    description: 'Golden fried crispy black gram lentil doughnuts with crushed peppercorns and fresh ginger.',
    price: 120.0,
    category: 'Idlis & Vadas',
    iconEmoji: '🍩',
    isVeg: true,
    isBestseller: true,
    rating: 4.8,
    ratingCount: 380,
  ),
  const Product(
    id: 'p-9',
    name: 'Kanchipuram Spiced Temple Idli',
    description: 'Traditional fermented idli tempered with dried ginger, peppercorns, curry leaves, and asafoetida.',
    price: 150.0,
    category: 'Idlis & Vadas',
    iconEmoji: '🛕',
    isVeg: true,
    isBestseller: false,
    rating: 4.7,
    ratingCount: 98,
  ),
  const Product(
    id: 'p-10',
    name: 'Dahi Vada South Coastal Style',
    description: 'Soft lentil vadas immersed in whipped sweet yogurt, sprinkled with roasted cumin and boondi.',
    price: 160.0,
    category: 'Idlis & Vadas',
    iconEmoji: '🥣',
    isVeg: true,
    isBestseller: false,
    rating: 4.6,
    ratingCount: 160,
  ),
  const Product(
    id: 'p-11',
    name: 'Thatte Idli with Podi & Butter Slab',
    description: 'Large Bangalore-style plate idli topped with dollop of fresh white butter and spicy gun-powder.',
    price: 170.0,
    category: 'Idlis & Vadas',
    iconEmoji: '🧈',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 340,
  ),

  // --- BIRYANI & RICE (5) ---
  const Product(
    id: 'p-12',
    name: 'Ambur Veg Dum Biryani',
    description: 'Fragrant Jeeraga Samba rice slow-cooked with garden vegetables, mint, and curd-based gravy.',
    price: 250.0,
    category: 'Biryani & Rice',
    iconEmoji: '🍚',
    isVeg: true,
    isBestseller: true,
    rating: 4.8,
    ratingCount: 275,
  ),
  const Product(
    id: 'p-13',
    name: 'Bisi Bele Bath with Boondi Crunch',
    description: 'Traditional Karnataka hot lentil rice concoction cooked with tamarind, nutmeg, and ghee.',
    price: 190.0,
    category: 'Biryani & Rice',
    iconEmoji: '🍲',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 410,
  ),
  const Product(
    id: 'p-14',
    name: 'Tempered Curd Rice (Thayir Sadam)',
    description: 'Comforting creamy yogurt rice tempered with mustard seeds, green chilies, and pomegranate.',
    price: 150.0,
    category: 'Biryani & Rice',
    iconEmoji: '🥣',
    isVeg: true,
    isBestseller: false,
    rating: 4.7,
    ratingCount: 220,
  ),
  const Product(
    id: 'p-15',
    name: 'Tangy Lemon Peanut Rice',
    description: 'Zesty South Indian rice tossed with fresh lemon juice, turmeric, crunchy peanuts, and curry leaves.',
    price: 160.0,
    category: 'Biryani & Rice',
    iconEmoji: '🍋',
    isVeg: true,
    isBestseller: false,
    rating: 4.5,
    ratingCount: 110,
  ),
  const Product(
    id: 'p-16',
    name: 'Chettinad Mushroom Biryani Pot',
    description: 'Spicy black pepper marinated button mushrooms layered with aromatic long-grain basmati rice.',
    price: 280.0,
    category: 'Biryani & Rice',
    iconEmoji: '🍄',
    isVeg: true,
    isBestseller: false,
    rating: 4.8,
    ratingCount: 190,
  ),

  // --- CURRIES (5) ---
  const Product(
    id: 'p-17',
    name: 'Chettinad Paneer Kurma',
    description: 'Rich roasted coconut, poppy seeds, and stone flower spiced gravy with cottage cheese.',
    price: 240.0,
    category: 'Curries',
    iconEmoji: '🥘',
    isVeg: true,
    isBestseller: true,
    rating: 4.8,
    ratingCount: 310,
  ),
  const Product(
    id: 'p-18',
    name: 'Malabar Vegetable Stew',
    description: 'Mild creamy coconut milk simmered with tender carrots, green peas, potatoes, and whole spices.',
    price: 220.0,
    category: 'Curries',
    iconEmoji: '🥥',
    isVeg: true,
    isBestseller: false,
    rating: 4.7,
    ratingCount: 145,
  ),
  const Product(
    id: 'p-19',
    name: 'Madras Drumstick Sambar Pot (500ml)',
    description: 'Thick authentic tamarind lentil stew brewed with baby shallots, drumsticks, and freshly ground sambar masala.',
    price: 130.0,
    category: 'Curries',
    iconEmoji: '🍲',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 620,
  ),
  const Product(
    id: 'p-20',
    name: 'Ennai Kathirikai Kulambu',
    description: 'Baby brinjals cooked in a tangy roasted sesame, tamarind, and spicy red chili reduction.',
    price: 210.0,
    category: 'Curries',
    iconEmoji: '🍆',
    isVeg: true,
    isBestseller: false,
    rating: 4.6,
    ratingCount: 95,
  ),
  const Product(
    id: 'p-21',
    name: 'Appam Basket (4 Pcs) with Stew',
    description: 'Soft-centered lacy fermented rice pancakes paired with delicate coconut milk gravy.',
    price: 230.0,
    category: 'Curries',
    iconEmoji: '🥞',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 280,
  ),

  // --- DESSERTS (5) ---
  const Product(
    id: 'p-22',
    name: 'Mysore Pak Melt (Desi Ghee)',
    description: 'Decadent royal sweet made from pure ghee, gram flour, and caramelized sugar.',
    price: 130.0,
    category: 'Desserts',
    iconEmoji: '🧈',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 380,
  ),
  const Product(
    id: 'p-23',
    name: 'Elaneer Payasam (Tender Coconut Kheer)',
    description: 'Refreshing dessert prepared with pulp of tender green coconuts, sweetened milk, and cardamom.',
    price: 160.0,
    category: 'Desserts',
    iconEmoji: '🥥',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 440,
  ),
  const Product(
    id: 'p-24',
    name: 'Rava Kesari with Roasted Cashews',
    description: 'Saffron-tinted semolina pudding cooked with generous amounts of cow ghee and golden raisins.',
    price: 120.0,
    category: 'Desserts',
    iconEmoji: '🍮',
    isVeg: true,
    isBestseller: false,
    rating: 4.7,
    ratingCount: 160,
  ),
  const Product(
    id: 'p-25',
    name: 'Palada Pradhaman',
    description: 'Kerala festival delicacy of steamed rice flakes cooked in thick condensed milk and jaggery.',
    price: 150.0,
    category: 'Desserts',
    iconEmoji: '🍨',
    isVeg: true,
    isBestseller: false,
    rating: 4.8,
    ratingCount: 190,
  ),
  const Product(
    id: 'p-26',
    name: 'Adhirasam Heritage Sweet (4 Pcs)',
    description: 'Deep-fried donut-shaped pastry crafted from fermented rice dough and palm jaggery.',
    price: 140.0,
    category: 'Desserts',
    iconEmoji: '🍩',
    isVeg: true,
    isBestseller: false,
    rating: 4.5,
    ratingCount: 85,
  ),

  // --- BEVERAGES (4) ---
  const Product(
    id: 'p-27',
    name: 'Thalaivaa Degree Filter Kaapi',
    description: 'Traditional brass tumbler decoction brewed from chicory-infused Coorg coffee beans with frothy hot milk.',
    price: 70.0,
    category: 'Beverages',
    iconEmoji: '☕',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 890,
  ),
  const Product(
    id: 'p-28',
    name: 'Jigarthanda Madurai Special',
    description: 'Famous cooling dessert drink made with almond gum, nannari syrup, basundi, and ice cream scoop.',
    price: 140.0,
    category: 'Beverages',
    iconEmoji: '🥤',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 520,
  ),
  const Product(
    id: 'p-29',
    name: 'Spiced Neer Mor (Buttermilk)',
    description: 'Refreshing churned yogurt cooler tempered with crushed ginger, asafoetida, green chili, and cilantro.',
    price: 60.0,
    category: 'Beverages',
    iconEmoji: '🥛',
    isVeg: true,
    isBestseller: false,
    rating: 4.8,
    ratingCount: 310,
  ),
  const Product(
    id: 'p-30',
    name: 'Fresh Nannari Sarbath with Chia',
    description: 'Heritage sarsaparilla root cooler infused with fresh lime juice, soaked chia seeds, and ice.',
    price: 80.0,
    category: 'Beverages',
    iconEmoji: '🍹',
    isVeg: true,
    isBestseller: false,
    rating: 4.7,
    ratingCount: 195,
  ),
];

// Available Filter Categories (Strictly matches product.category)
final availableCategoriesProvider = Provider<List<String>>((ref) => const [
  'All',
  'Dosas',
  'Idlis & Vadas',
  'Biryani & Rice',
  'Curries',
  'Desserts',
  'Beverages',
]);

// Multi-Criteria Filter Providers
enum DietaryFilter { all, vegOnly }
enum SortOption { recommended, rating, priceLowToHigh, priceHighToLow }

final selectedCategoryProvider = StateProvider<String>((ref) => 'All');
final searchQueryProvider = StateProvider<String>((ref) => '');
final dietaryFilterProvider = StateProvider<DietaryFilter>((ref) => DietaryFilter.all);
final bestsellerOnlyProvider = StateProvider<bool>((ref) => false);
final sortByProvider = StateProvider<SortOption>((ref) => SortOption.recommended);

// App Global Settings (Theme & i18n)
final themeModeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.light);
final languageProvider = StateProvider<String>((ref) => 'en'); // en, hi, gu, ta
final deliveryTipProvider = StateProvider<double>((ref) => 0.0);

// ==========================================
// 3. COMPLETE MULTI-LANGUAGE DICTIONARY (i18n)
// ==========================================
final translationsProvider = Provider<Map<String, Map<String, String>>>((ref) {
  return {
    'en': {
      // Navigation
      'navMenu': 'Menu',
      'navCart': 'Tray',
      'navOrders': 'Live Order',
      'navProfile': 'Profile',
      
      // Header & Branding
      'appName': 'THALAIVAA',
      'tagline': 'Authentic South Indian Cuisine',
      'searchHint': 'Search Dosas, Idlis, Filter Kaapi, Biryani...',
      'outlet': 'Outlet',
      'change': 'CHANGE',
      
      // Categories
      'cat_All': 'All',
      'cat_Dosas': 'Dosas & Roasts',
      'cat_Idlis & Vadas': 'Idlis & Vadas',
      'cat_Biryani & Rice': 'Biryani & Rice Meals',
      'cat_Curries': 'Curries & Sambar',
      'cat_Desserts': 'Desserts & Sweets',
      'cat_Beverages': 'Filter Kaapi & Drinks',
      
      // Quick Filters
      'all': 'All',
      'pureVeg': 'Pure Veg',
      'bestsellers': '⭐ Bestsellers',
      'sort': 'Sort',
      'sort_rec': 'Recommended',
      'sort_rating': 'Top Rated ★',
      'sort_price_low': 'Price: Low to High',
      'sort_price_high': 'Price: High to Low',
      
      // Promotional Banner
      'promo_title': 'Madras Ghee Roast Festival',
      'promo_sub': 'Use code THALAIVAA50 for ₹50 OFF',
      
      // Actions & Buttons
      'add': 'ADD +',
      'added': 'ADDED',
      'addToTray': 'Add to Tray',
      'customize': 'Customizable',
      'clearSearch': 'Clear search',
      
      // Delivery & Cart
      'orderType_delivery': '🛵 Delivery',
      'orderType_takeaway': '🥡 Takeaway',
      'orderType_dineIn': '🍽️ Dine-in',
      'deliveryAddress': 'Delivery Address',
      'deliverTo': 'Deliver to',
      'deliveryInstructions': 'Delivery Instructions',
      'instr_leave_door': '🚪 Leave at door',
      'instr_no_bell': '🔕 Don\'t ring bell',
      'instr_avoid_call': '📵 Avoid calling',
      'instr_pet': '🐾 Pet at home',
      'contactless': 'Contactless Delivery',
      'contactless_desc': 'Rider leaves package at your doorstep safely',
      'free_delivery_above': 'Free delivery on orders above ₹499',
      'free_delivery_unlock': 'Add more for FREE delivery!',
      'tipTitle': 'Tip your Delivery Partner',
      'tipSubtitle': '100% of the tip goes directly to your rider',
      'noTip': 'No Tip',
      'applyCoupon': 'Apply Coupon',
      'couponApplied': 'Coupon Applied!',
      'couponHint': 'Enter Coupon Code',
      'apply': 'APPLY',
      'remove': 'REMOVE',
      
      // Bill Breakdown
      'billDetails': 'Bill Details',
      'subtotal': 'Item Total',
      'gst': 'GST & Restaurant Taxes (5%)',
      'deliveryFee': 'Delivery Partner Fee',
      'deliveryTip': 'Delivery Tip',
      'discount': 'Special Coupon Discount',
      'grandTotal': 'To Pay',
      'free': 'FREE',
      'checkout': 'PLACE ORDER',
      
      // Live Tracking Screen
      'trackingTitle': 'Live Order Tracking',
      'estimatedDelivery': 'Estimated Delivery',
      'mins': 'Mins',
      'onTime': 'ON TIME',
      'stage_confirmed_title': '1. Order Confirmed',
      'stage_confirmed_sub': 'Restaurant has accepted your order',
      'stage_prep_title': '2. In the Kitchen',
      'stage_prep_sub': 'Chef is roasting your dosas in pure desi ghee',
      'stage_out_title': '3. Out for Delivery',
      'stage_out_sub': 'Rider is on the way to your location',
      'stage_delivered_title': '4. Delivered',
      'stage_delivered_sub': 'Delivered hot & fresh at your doorstep',
      'riderDetails': 'Delivery Partner',
      'call': 'Call',
      'chat': 'Chat',
      'simulateAdvance': '⚡ Simulate Next Order Stage',
      'orderSummary': 'Order Summary',
      'totalPaid': 'Total Paid',
      'noActiveOrder': 'No active order currently being tracked.',
      'browseMenu': 'Browse Authentic Menu',
      
      // Profile & Settings Screen
      'profile': 'Settings & Preferences',
      'preferences': 'App Preferences',
      'themeMode': 'Appearance Theme',
      'lightMode': 'Clean Light Mode',
      'darkMode': 'Obsidian Dark Mode',
      'language': 'Display Language',
      'operatingBranch': 'Select Operating Branch',
      'savedAddresses': 'Manage Saved Addresses',
      'support': '24x7 Customer Support',
      'callSupport': 'Call Helpline',
    },
    'hi': {
      // Navigation
      'navMenu': 'मेनू',
      'navCart': 'ट्रे',
      'navOrders': 'लाइव ऑर्डर',
      'navProfile': 'प्रोफ़ाइल',
      
      // Header & Branding
      'appName': 'थलाइवा',
      'tagline': 'प्रामाणिक दक्षिण भारतीय व्यंजन',
      'searchHint': 'डोसा, इडली, फिल्टर कॉफी, बिरयानी खोजें...',
      'outlet': 'शाखा',
      'change': 'बदलें',
      
      // Categories
      'cat_All': 'सभी व्यंजन',
      'cat_Dosas': 'डोसा और रोस्ट',
      'cat_Idlis & Vadas': 'इडली और वड़ा',
      'cat_Biryani & Rice': 'बिरयानी और चावल भोजन',
      'cat_Curries': 'करी और सांभर',
      'cat_Desserts': 'मिठाइयाँ और पायसम',
      'cat_Beverages': 'फिल्टर कॉफी और पेय',
      
      // Quick Filters
      'all': 'सभी',
      'pureVeg': 'शुद्ध शाकाहारी',
      'bestsellers': '⭐ सबसे लोकप्रिय',
      'sort': 'क्रमबद्ध करें',
      'sort_rec': 'सुझाया गया',
      'sort_rating': 'उच्चतम रेटिंग ★',
      'sort_price_low': 'कीमत: कम से ज्यादा',
      'sort_price_high': 'कीमत: ज्यादा से कम',
      
      // Promotional Banner
      'promo_title': 'मद्रास घी रोस्ट महोत्सव',
      'promo_sub': '₹50 की छूट के लिए कोड THALAIVAA50 का उपयोग करें',
      
      // Actions & Buttons
      'add': 'जोड़ें +',
      'added': 'जुड़ गया',
      'addToTray': 'ट्रे में जोड़ें',
      'customize': 'अनुकूलन योग्य',
      'clearSearch': 'खोज साफ़ करें',
      
      // Delivery & Cart
      'orderType_delivery': '🛵 डिलीवरी',
      'orderType_takeaway': '🥡 टेकअवे',
      'orderType_dineIn': '🍽️ डाइन-इन',
      'deliveryAddress': 'डिलीवरी का पता',
      'deliverTo': 'यहाँ डिलीवर करें',
      'deliveryInstructions': 'डिलीवरी निर्देश',
      'instr_leave_door': '🚪 दरवाजे पर छोड़ें',
      'instr_no_bell': '🔕 घंटी न बजाएं',
      'instr_avoid_call': '📵 फोन न करें',
      'instr_pet': '🐾 घर में पालतू जानवर है',
      'contactless': 'संपर्क रहित डिलीवरी',
      'contactless_desc': 'राइडर पैकेज आपके दरवाजे पर सुरक्षित छोड़ देगा',
      'free_delivery_above': '₹499 से अधिक के ऑर्डर पर मुफ़्त डिलीवरी',
      'free_delivery_unlock': 'मुफ़्त डिलीवरी के लिए और जोड़ें!',
      'tipTitle': 'डिलीवरी पार्टनर को टिप दें',
      'tipSubtitle': '100% टिप सीधे आपके राइडर को मिलती है',
      'noTip': 'कोई टिप नहीं',
      'applyCoupon': 'कूपन लागू करें',
      'couponApplied': 'कूपन लागू हुआ!',
      'couponHint': 'कूपन कोड दर्ज करें',
      'apply': 'लागू करें',
      'remove': 'हटाएं',
      
      // Bill Breakdown
      'billDetails': 'बिल विवरण',
      'subtotal': 'कुल मूल्य',
      'gst': 'जीएसटी और टैक्स (5%)',
      'deliveryFee': 'डिलीवरी शुल्क',
      'deliveryTip': 'डिलीवरी टिप',
      'discount': 'कूपन छूट',
      'grandTotal': 'कुल देय',
      'free': 'मुफ़्त',
      'checkout': 'ऑर्डर प्लेस करें',
      
      // Live Tracking Screen
      'trackingTitle': 'लाइव ऑर्डर ट्रैकिंग',
      'estimatedDelivery': 'अनुमानित डिलीवरी',
      'mins': 'मिनट',
      'onTime': 'समय पर',
      'stage_confirmed_title': '1. ऑर्डर स्वीकृत',
      'stage_confirmed_sub': 'रेस्टोरेंट ने आपका ऑर्डर स्वीकार कर लिया है',
      'stage_prep_title': '2. रसोई में तैयारी',
      'stage_prep_sub': 'शेफ शुद्ध देसी घी में आपके डोसे तैयार कर रहे हैं',
      'stage_out_title': '3. डिलीवरी के लिए रवाना',
      'stage_out_sub': 'राइडर आपके पते की ओर निकल चुका है',
      'stage_delivered_title': '4. डिलीवर हो गया',
      'stage_delivered_sub': 'गर्मा-गर्म और ताज़ा आपके दरवाजे पर डिलीवर हुआ',
      'riderDetails': 'डिलीवरी पार्टनर',
      'call': 'कॉल करें',
      'chat': 'चैट',
      'simulateAdvance': '⚡ अगला चरण सिम्युलेट करें',
      'orderSummary': 'ऑर्डर सारांश',
      'totalPaid': 'कुल भुगतान',
      'noActiveOrder': 'वर्तमान में कोई सक्रिय ऑर्डर नहीं है।',
      'browseMenu': 'प्रामाणिक मेनू देखें',
      
      // Profile & Settings Screen
      'profile': 'सेटिंग्स और प्राथमिकताएं',
      'preferences': 'ऐप सेटिंग्स',
      'themeMode': 'थीम स्वरूप',
      'lightMode': 'लाइट मोड',
      'darkMode': 'ऑब्सिडियन डार्क मोड',
      'language': 'भाषा चुनें',
      'operatingBranch': 'सक्रिय शाखा चुनें',
      'savedAddresses': 'सहेजे गए पते',
      'support': '24x7 ग्राहक सहायता',
      'callSupport': 'हेल्पलाइन पर कॉल करें',
    },
    'gu': {
      // Navigation
      'navMenu': 'મેનૂ',
      'navCart': 'ટ્રે',
      'navOrders': 'લાઇવ ઓર્ડર',
      'navProfile': 'પ્રોફાઇલ',
      
      // Header & Branding
      'appName': 'થલાઇવા',
      'tagline': 'અસલી દક્ષિણ ભારતીય સ્વાદ',
      'searchHint': 'ઢોસા, ઈડલી, ફિલ્ટર કોફી, બિરયાની શોધો...',
      'outlet': 'શાખા',
      'change': 'બદલો',
      
      // Categories
      'cat_All': 'બધી વાનગીઓ',
      'cat_Dosas': 'ઢોસા અને રોસ્ટ',
      'cat_Idlis & Vadas': 'ઈડલી અને વડા',
      'cat_Biryani & Rice': 'બિરયાની અને રાઇસ મીલ્સ',
      'cat_Curries': 'કરી અને સંભાર',
      'cat_Desserts': 'મીઠાઈઓ અને પાયસમ',
      'cat_Beverages': 'ફિલ્ટર કોફી અને પીણાં',
      
      // Quick Filters
      'all': 'બધું',
      'pureVeg': 'શુદ્ધ શાકાહારી',
      'bestsellers': '⭐ લોકપ્રિય વાનગીઓ',
      'sort': 'ક્રમબદ્ધ કરો',
      'sort_rec': 'ભલામણ કરેલ',
      'sort_rating': 'ટોપ રેટિંગ ★',
      'sort_price_low': 'કિંમત: ઓછી થી વધુ',
      'sort_price_high': 'કિંમત: વધુ થી ઓછી',
      
      // Promotional Banner
      'promo_title': 'મદ્રાસ ઘી રોસ્ટ મહોત્સવ',
      'promo_sub': '₹50 ના ડિસ્કાઉન્ટ માટે THALAIVAA50 વાપરો',
      
      // Actions & Buttons
      'add': 'ઉમેરો +',
      'added': 'ઉમેરાયું',
      'addToTray': 'ટ્રેમાં ઉમેરો',
      'customize': 'કસ્ટમાઇઝ કરો',
      'clearSearch': 'શોધ સાફ કરો',
      
      // Delivery & Cart
      'orderType_delivery': '🛵 ડિલિવરી',
      'orderType_takeaway': '🥡 ટેકઅવે',
      'orderType_dineIn': '🍽️ ડાઇન-ઇન',
      'deliveryAddress': 'ડિલિવરી સરનામું',
      'deliverTo': 'અહીં ડિલિવર કરો',
      'deliveryInstructions': 'ડિલિવરી સૂચનાઓ',
      'instr_leave_door': '🚪 દરવાજા પર મૂકો',
      'instr_no_bell': '🔕 બેલ ન વગાડો',
      'instr_avoid_call': '📵 ફોન ન કરો',
      'instr_pet': '🐾 પાલતુ પ્રાણી છે',
      'contactless': 'કોન્ટેક્ટલેસ ડિલિવરી',
      'contactless_desc': 'રાઇડર પાર્સલ દરવાજા પર સુરક્ષિત રીતે મૂકશે',
      'free_delivery_above': '₹499 થી વધુના ઓર્ડર પર મફત ડિલિવરી',
      'free_delivery_unlock': 'મફત ડિલિવરી માટે વધુ ઉમેરો!',
      'tipTitle': 'ડિલિવરી પાર્ટનરને ટિપ આપો',
      'tipSubtitle': '100% ટિપ સીધી તમારા રાઇડરને મળે છે',
      'noTip': 'ટિપ નથી',
      'applyCoupon': 'કૂપન લાગુ કરો',
      'couponApplied': 'કૂપન લાગુ થઈ ગયું!',
      'couponHint': 'કૂપન કોડ લખો',
      'apply': 'લાગુ કરો',
      'remove': 'દૂર કરો',
      
      // Bill Breakdown
      'billDetails': 'બિલ વિગતો',
      'subtotal': 'કુલ કિંમત',
      'gst': 'જીએસટી અને ટેક્સ (5%)',
      'deliveryFee': 'ડિલિવરી ચાર્જ',
      'deliveryTip': 'ડિલિવરી ટિપ',
      'discount': 'કૂપન ડિસ્કાઉન્ટ',
      'grandTotal': 'ચૂકવવાપાત્ર કુલ',
      'free': 'મફત',
      'checkout': 'ઓર્ડર કન્ફર્મ કરો',
      
      // Live Tracking Screen
      'trackingTitle': 'લાઇવ ઓર્ડર ટ્રેકિંગ',
      'estimatedDelivery': 'અંદાજિત ડિલિવરી',
      'mins': 'મિનિટ',
      'onTime': 'સમયસર',
      'stage_confirmed_title': '1. ઓર્ડર સ્વીકારાયો',
      'stage_confirmed_sub': 'રેસ્ટોરન્ટે તમારો ઓર્ડર કન્ફર્મ કર્યો છે',
      'stage_prep_title': '2. રસોડામાં તૈયારી',
      'stage_prep_sub': 'શેફ શુદ્ધ દેશી ઘીમાં ઢોસા બનાવી રહ્યા છે',
      'stage_out_title': '3. ડિલિવરી માટે રવાના',
      'stage_out_sub': 'રાઇડર તમારા સરનામે આવી રહ્યો છે',
      'stage_delivered_title': '4. ડિલિવર થઈ ગયું',
      'stage_delivered_sub': 'ગરમાગરમ અને તાજું ડિલિવર થયું છે',
      'riderDetails': 'ડિલિવરી પાર્ટનર',
      'call': 'કોલ કરો',
      'chat': 'ચેટ',
      'simulateAdvance': '⚡ આગળનો તબક્કો સિમ્યુલેટ કરો',
      'orderSummary': 'ઓર્ડર સારાંશ',
      'totalPaid': 'કુલ ચુકવણી',
      'noActiveOrder': 'હાલમાં કોઈ સક્રિય ઓર્ડર નથી.',
      'browseMenu': 'મેનૂ જુઓ',
      
      // Profile & Settings Screen
      'profile': 'સેટિંગ્સ અને પસંદગીઓ',
      'preferences': 'એપ્લિકેશન સેટિંગ્સ',
      'themeMode': 'થીમ લુક',
      'lightMode': 'લાઇટ મોડ',
      'darkMode': 'ઓબ્સિડિયન ડાર્ક મોડ',
      'language': 'ભાષા પસંદ કરો',
      'operatingBranch': 'શાખા પસંદ કરો',
      'savedAddresses': 'સાચવેલા સરનામાં',
      'support': '24x7 ગ્રાહક સહાય',
      'callSupport': 'હેલ્પલાઇન કોલ કરો',
    },
    'ta': {
      // Navigation
      'navMenu': 'மெனு',
      'navCart': 'கூடை',
      'navOrders': 'நேரலை ஆர்டர்',
      'navProfile': 'சுயவிவரம்',
      
      // Header & Branding
      'appName': 'தலைவா',
      'tagline': 'பாரம்பரிய தென்னிந்திய சுவை',
      'searchHint': 'தோசை, இட்லி, பில்டர் காபி, பிரியாணி தேடுங்கள்...',
      'outlet': 'கிளை',
      'change': 'மாற்று',
      
      // Categories
      'cat_All': 'அனைத்து உணவுகள்',
      'cat_Dosas': 'தோசை மற்றும் ரோஸ்ட்',
      'cat_Idlis & Vadas': 'இட்லி மற்றும் வடை',
      'cat_Biryani & Rice': 'பிரியாணி & சாத உணவுகள்',
      'cat_Curries': 'சாம்பார் மற்றும் குழம்பு',
      'cat_Desserts': 'இனிப்புகள் & பாயாசம்',
      'cat_Beverages': 'பில்டர் காபி & பானங்கள்',
      
      // Quick Filters
      'all': 'அனைத்தும்',
      'pureVeg': 'சைவம் மட்டும்',
      'bestsellers': '⭐ பிரபல உணவுகள்',
      'sort': 'வரிசைப்படுத்து',
      'sort_rec': 'பரிந்துரைக்கப்பட்டது',
      'sort_rating': 'உயர்ந்த மதிப்பீடு ★',
      'sort_price_low': 'விலை: குறைந்தது முதல் அதிகம்',
      'sort_price_high': 'விலை: அதிகம் முதல் குறைந்தது',
      
      // Promotional Banner
      'promo_title': 'மெட்ராஸ் நெய் ரோஸ்ட் திருவிழா',
      'promo_sub': '₹50 தள்ளுபடி பெற THALAIVAA50 குறியீட்டைப் பயன்படுத்துங்கள்',
      
      // Actions & Buttons
      'add': 'சேர் +',
      'added': 'சேர்க்கப்பட்டது',
      'addToTray': 'கூடையில் சேர்',
      'customize': 'விருப்பப்படி மாற்றுக',
      'clearSearch': 'தேடலை அழிக்கவும்',
      
      // Delivery & Cart
      'orderType_delivery': '🛵 டெலிவரி',
      'orderType_takeaway': '🥡 பார்சல்',
      'orderType_dineIn': '🍽️ உணவகத்தில்',
      'deliveryAddress': 'டெலிவரி முகவரி',
      'deliverTo': 'இங்கு டெலிவரி செய்',
      'deliveryInstructions': 'டெலிவரி வழிமுறைகள்',
      'instr_leave_door': '🚪 வாசலில் வைக்கவும்',
      'instr_no_bell': '🔕 மணி அடிக்க வேண்டாம்',
      'instr_avoid_call': '📵 போன் செய்ய வேண்டாம்',
      'instr_pet': '🐾 செல்லப்பிராணி உள்ளது',
      'contactless': 'தொடர்பற்ற டெலிவரி',
      'contactless_desc': 'டெலிவரி பார்ட்னர் வாசலில் பாதுகாப்பாக வைப்பார்',
      'free_delivery_above': '₹499க்கு மேல் இலவச டெலிவரி',
      'free_delivery_unlock': 'இலவச டெலிவரிக்கு மேலும் சேர்க்கவும்!',
      'tipTitle': 'டெலிவரி பார்ட்னருக்கு டிப் வழங்குக',
      'tipSubtitle': '100% தொகையும் நேரடியாக டெலிவரி பார்ட்னரைச் சென்றடையும்',
      'noTip': 'டிப் வேண்டாம்',
      'applyCoupon': 'கூப்பன் சேர்',
      'couponApplied': 'கூப்பன் சேர்க்கப்பட்டது!',
      'couponHint': 'கூப்பன் குறியீட்டை உள்ளிடுக',
      'apply': 'சேர்க்கவும்',
      'remove': 'நீக்கு',
      
      // Bill Breakdown
      'billDetails': 'கட்டண விவரங்கள்',
      'subtotal': 'உணவு மொத்தம்',
      'gst': 'ஜிஎஸ்டி வரிகள் (5%)',
      'deliveryFee': 'டெலிவரி கட்டணம்',
      'deliveryTip': 'டெலிவரி டிப்',
      'discount': 'கூப்பன் தள்ளுபடி',
      'grandTotal': 'செலுத்த வேண்டியது',
      'free': 'இலவசம்',
      'checkout': 'ஆர்டர் செய்க',
      
      // Live Tracking Screen
      'trackingTitle': 'நேரலை ஆர்டர் கண்காணிப்பு',
      'estimatedDelivery': 'எதிர்பார்க்கப்படும் டெலிவரி',
      'mins': 'நிமிடங்கள்',
      'onTime': 'நேரத்திற்கு',
      'stage_confirmed_title': '1. ஆர்டர் உறுதியானது',
      'stage_confirmed_sub': 'உணவகம் உங்கள் ஆர்டரை ஏற்றுக்கொண்டது',
      'stage_prep_title': '2. சமையலறையில் தயாராகிறது',
      'stage_prep_sub': 'சுத்தமான நெய்யில் தோசைகள் தயாராகின்றன',
      'stage_out_title': '3. டெலிவரிக்கு புறப்பட்டது',
      'stage_out_sub': 'டெலிவரி பார்ட்னர் உங்கள் முகவரிக்கு வருகிறார்',
      'stage_delivered_title': '4. டெலிவரி செய்யப்பட்டது',
      'stage_delivered_sub': 'சூடாகவும் சுவையாகவும் டெலிவரி செய்யப்பட்டது',
      'riderDetails': 'டெலிவரி பார்ட்னர்',
      'call': 'அழைக்க',
      'chat': 'செய்தி',
      'simulateAdvance': '⚡ அடுத்த நிலையை இயக்குக',
      'orderSummary': 'ஆர்டர் விவரங்கள்',
      'totalPaid': 'செலுத்திய மொத்தத் தொகை',
      'noActiveOrder': 'தற்போது நேரலை ஆர்டர் எதுவும் இல்லை.',
      'browseMenu': 'சுவையான மெனுவை காண்க',
      
      // Profile & Settings Screen
      'profile': 'அமைப்புகள் & விருப்பங்கள்',
      'preferences': 'பயன்பாட்டு அமைப்புகள்',
      'themeMode': 'தீம் தேர்வு',
      'lightMode': 'வெளிச்ச தீம்',
      'darkMode': 'இருண்ட தீம்',
      'language': 'மொழியைத் தேர்ந்தெடுக்கவும்',
      'operatingBranch': 'கிளையை தேர்ந்தெடுக்கவும்',
      'savedAddresses': 'சேமிக்கப்பட்ட முகவரிகள்',
      'support': '24x7 வாடிக்கையாளர் சேவை',
      'callSupport': 'உதவி எண்ணை அழைக்கவும்',
    },
  };
});

// Helper for UI Text
final trProvider = Provider<String Function(String)>((ref) {
  final lang = ref.watch(languageProvider);
  final map = ref.watch(translationsProvider);
  final currentMap = map[lang] ?? map['en']!;
  return (String key) => currentMap[key] ?? map['en']![key] ?? key;
});

// Localized Product Title & Description Resolver
class LocalizedProductInfo {
  final String name;
  final String description;
  const LocalizedProductInfo(this.name, this.description);
}

final localizedDishInfoProvider = Provider.family<LocalizedProductInfo, Product>((ref, product) {
  final lang = ref.watch(languageProvider);
  
  if (lang == 'hi') {
    switch (product.id) {
      case 'p-1': return const LocalizedProductInfo('घी रोस्ट मसाला डोसा', 'शुद्ध देसी घी में भुना हुआ कुरकुरा डोसा, आलू मसाले के साथ।');
      case 'p-2': return const LocalizedProductInfo('मैसूर चीज़ बर्स्ट डोसा', 'तीखी लाल लहसुन चटनी और पिघले हुए मोज़ेरेला चीज़ से भरपूर डोसा।');
      case 'p-3': return const LocalizedProductInfo('रवा अनियन मसाला डोसा', 'बारीक कटे प्याज, जीरा और काजू से बना कुरकुरा सूजी डोसा।');
      case 'p-4': return const LocalizedProductInfo('पोडी घी करम डोसा', 'गनपाउडर पोडी मसाले और गर्म देसी घी से सजा कुरकुरा डोसा।');
      case 'p-5': return const LocalizedProductInfo('पेपर प्लेन रोस्ट डोसा (2.5 फीट)', 'अत्यंत पतला, कुरकुरा 2.5 फीट लंबा गोल्डन डोसा 3 चटनी के साथ।');
      case 'p-6': return const LocalizedProductInfo('चेट्टीनाड पनीर टिक्का डोसा', 'स्मोकी रोस्टेड पनीर क्यूब्स और चेट्टीनाड काली मिर्च मसालेदार डोसा।');
      case 'p-7': return const LocalizedProductInfo('स्टीम्ड बटन घी इडली (14 नग)', 'गरमा-गरम सांभर और घी में तैरती 14 मुलायम मिनी इडली।');
      case 'p-8': return const LocalizedProductInfo('मेदु वड़ा जोड़ी (सांभर डिप)', 'काली मिर्च और ताजे अदरक के साथ सुनहरे कुरकुरे मेदु वड़े।');
      case 'p-9': return const LocalizedProductInfo('कांचीपुरम स्पाइस्ड मंदिर इडली', 'अदरक, काली मिर्च और कढ़ी पत्ते से तड़का लगाई गई पारंपरिक इडली।');
      case 'p-10': return const LocalizedProductInfo('दही वड़ा दक्षिण तटीय शैली', 'मीठे फेंटे हुए दही, भुने जीरे और बूंदी में डूबे हुए मुलायम वड़े।');
      case 'p-11': return const LocalizedProductInfo('थट्टे इडली (पोडी और सफेद मक्खन)', 'ताजे सफेद मक्खन और तीखे पोडी मसाले के साथ बड़ी प्लेट इडली।');
      case 'p-12': return const LocalizedProductInfo('अंबूर वेज दम बिरयानी', 'सुगंधित जीरा सांबा चावल में ताजी सब्जियों के साथ पकी प्रामाणिक बिरयानी।');
      case 'p-13': return const LocalizedProductInfo('बिसी बेले बाथ (बूंदी क्रंच)', 'इमली, जायफल और घी में पकी कर्नाटक की पारंपरिक दाल-चावल खिचड़ी।');
      case 'p-14': return const LocalizedProductInfo('तड़का कर्ड राइस (थायिर सादम)', 'राई, हरी मिर्च और अनार के दानों से तड़का लगाया हुआ मलाईदार दही चावल।');
      case 'p-15': return const LocalizedProductInfo('टैंगी लेमन पीनट राइस', 'नींबू के रस, हल्दी और कुरकुरी मूंगफली के साथ स्वादिष्ट साउथ इंडियन चावल।');
      case 'p-16': return const LocalizedProductInfo('चेट्टीनाड मशरूम बिरयानी पॉट', 'काली मिर्च मैरीनेटेड मशरूम और खुशबूदार बासमती चावल की बिरयानी।');
      case 'p-17': return const LocalizedProductInfo('चेट्टीनाड पनीर कूरमा', 'भुने हुए नारियल और मसालों की समृद्ध ग्रेवी में पनीर।');
      case 'p-18': return const LocalizedProductInfo('मालाबार वेजीटेबल स्टू', 'नारियल के दूध में गाजर, मटर और आलू के साथ पकाया गया सौम्य स्टू।');
      case 'p-19': return const LocalizedProductInfo('मद्रास ड्रमस्टिक सांभर पॉट (500ml)', 'सहजन और ताजे पिसे मसालों के साथ पारंपरिक मद्रास सांभर।');
      case 'p-20': return const LocalizedProductInfo('एन्नई कथिरीकाई कुलम्बु', 'तिल और इमली की चटपटी तीखी ग्रेवी में छोटे बैंगन की सब्जी।');
      case 'p-21': return const LocalizedProductInfo('अप्पम बास्केट (4 नग) स्टू के साथ', 'मुलायम जालीदार अप्पम नारियल के दूध वाले स्वादिष्ट स्टू के साथ।');
      case 'p-22': return const LocalizedProductInfo('मैसूर पाक (शुद्ध देसी घी)', 'शुद्ध घी, बेसन और चीनी से बनी मुंह में घुल जाने वाली शाही मिठाई।');
      case 'p-23': return const LocalizedProductInfo('इलानीर पायसम (नारियल खीर)', 'ताजे नारियल की मलाई, मीठे दूध और इलायची से बनी लाजवाब खीर।');
      case 'p-24': return const LocalizedProductInfo('रवा केसरी (काजू और किशमिश)', 'केसर और गाय के शुद्ध घी में पकी स्वादिष्ट सूजी की मिठाई।');
      case 'p-25': return const LocalizedProductInfo('पालदा प्रधमन', 'केरल की प्रसिद्ध उबले चावल के गुच्छों और गाढ़े दूध की खीर।');
      case 'p-26': return const LocalizedProductInfo('अधिरसम हेरिटेज स्वीट (4 नग)', 'चावल के आटे और ताड़ के गुड़ से तली हुई पारंपरिक दक्षिण भारतीय मिठाई।');
      case 'p-27': return const LocalizedProductInfo('थलाइवा डिग्री फिल्टर कॉफी', 'कूर्ग कॉफी बीन्स से पीतल के गिलास में तैयार झागदार फिल्टर कॉफी।');
      case 'p-28': return const LocalizedProductInfo('जिगरथंडा मदुरै स्पेशल', 'बादाम गोंद, नन्नारी सिरप, बासुंदी और आइसक्रीम से बना मशहूर कूल ड्रिंक।');
      case 'p-29': return const LocalizedProductInfo('स्पाइस्ड नीर मोर (मसाला छाछ)', 'अदरक, हींग, हरी मिर्च और धनिए से तड़का लगाई हुई ठंडी छाछ।');
      case 'p-30': return const LocalizedProductInfo('ताजा नन्नारी शरबत (चिया सीड्स)', 'नन्नारी की जड़ का अर्क, नींबू का रस और भीगे हुए चिया सीड्स।');
    }
  } else if (lang == 'gu') {
    switch (product.id) {
      case 'p-1': return const LocalizedProductInfo('ઘી રોસ્ટ મસાલા ઢોસા', 'શુદ્ધ દેશી ઘીમાં શેકેલો કુરકુરો ઢોસા, ટેસ્ટી બટાકાના મસાલા સાથે.');
      case 'p-2': return const LocalizedProductInfo('મૈસૂર ચીઝ બર્સ્ટ ઢોસા', 'લાલ લસણની ચટણી અને પીગળેલા મોઝેરેલા ચીઝથી ભરપૂર સ્વાદિષ્ટ ઢોસા.');
      case 'p-3': return const LocalizedProductInfo('રવા ઓનિયન મસાલા ઢોસા', 'ઝીણી સમારેલી ડુંગળી, જીરું અને કાજુ સાથે ક્રિસ્પી રવા ઢોસા.');
      case 'p-4': return const LocalizedProductInfo('પોડી ઘી કરમ ઢોસા', 'ગનપાઉડર પોડી મસાલો અને ગરમ ઘીથી ભરપૂર ક્રન્ચી ઢોસા.');
      case 'p-5': return const LocalizedProductInfo('પેપર પ્લેન રોસ્ટ ઢોસા (2.5 ફૂટ)', 'અતિશય પાતળો અને 2.5 ફૂટ લાંબો કુરકુરો પેપર ઢોસા 3 ચટણી સાથે.');
      case 'p-6': return const LocalizedProductInfo('ચેટ્ટીનાડ પનીર ટિક્કા ઢોસા', 'સ્મોકી પનીર ટુકડા અને ચેટ્ટીનાડ મરી મસાલાથી બનેલો ફ્યુઝન ઢોસા.');
      case 'p-7': return const LocalizedProductInfo('સ્ટીમ્ડ બટન ઘી ઈડલી (14 નંગ)', 'ગરમાગરમ સંભાર અને ઘીમાં ડૂબેલી 14 મિનિ નરમ ઈડલી.');
      case 'p-8': return const LocalizedProductInfo('મેદુ વડા જોડી (સંભાર ડીપ)', 'કાળા મરી અને તાજા આદુ સાથે સોનેરી તળેલા ક્રિસ્પી મેદુ વડા.');
      case 'p-9': return const LocalizedProductInfo('કાંચીપુરમ સ્પાઈસ્ડ મંદિર ઈડલી', 'સૂકા આદુ, મરી અને મીઠા લીમડાનો વઘાર કરેલી સ્વાદિષ્ટ ઈડલી.');
      case 'p-10': return const LocalizedProductInfo('દહીં વડા સાઉથ કોસ્ટલ સ્ટાઈલ', 'મીઠા દહીં અને શેકેલા જીરા સાથે નરમ મેદુ વડા.');
      case 'p-11': return const LocalizedProductInfo('થટ્ટે ઈડલી (પોડી અને સફેદ માખણ)', 'તાજા સફેદ માખણ અને મસાલેદાર પોડી સાથે મોટી પ્લેટ ઈડલી.');
      case 'p-12': return const LocalizedProductInfo('અંબુર વેજ દમ બિરયાની', 'જીરા સાંબા ચોખા અને તાજા શાકભાજીથી ધીમા તાપે રાંધેલી બિરયાની.');
      case 'p-13': return const LocalizedProductInfo('બિસી બેલે બાથ (બૂંદી ક્રન્ચ)', 'કર્ણાટકની પ્રખ્યાત દાળ-ભાત અને મસાલાની ગરમાગરમ વાનગી.');
      case 'p-14': return const LocalizedProductInfo('વઘારેલા દહીં ભાત (થાયિર સાદમ)', 'રાઈ, લીલા મરચા અને દાડમના દાણા સાથે ક્રીમી દહીં ભાત.');
      case 'p-15': return const LocalizedProductInfo('ટેન્ગી લેમન પીનટ રાઈસ', 'લીંબુનો રસ, હળદર અને ક્રન્ચી સીંગદાણાવાળા સ્વાદિષ્ટ ભાત.');
      case 'p-16': return const LocalizedProductInfo('ચેટ્ટીનાડ મશરૂમ બિરયાની પોટ', 'કાળા મરીના મસાલાવાળા મશરૂમ અને બાસમતી ચોખાની બિરયાની.');
      case 'p-17': return const LocalizedProductInfo('ચેટ્ટીનાડ પનીર કુરમા', 'શેકેલા નાળિયેર અને મસાલાની રિચ ગ્રેવીમાં પનીર.');
      case 'p-18': return const LocalizedProductInfo('મલાબાર વેજીટેબલ સ્ટ્યૂ', 'નાળિયેરના દૂધમાં ગાજર, વટાણા અને બટાકા સાથે બનાવેલો સ્ટ્યૂ.');
      case 'p-19': return const LocalizedProductInfo('મદ્રાસ સરગવો સંભાર પોટ (500ml)', 'સરગવો અને તાજા પીસેલા મસાલા સાથેનો અસલી મદ્રાસી સંભાર.');
      case 'p-20': return const LocalizedProductInfo('એન્નાઈ કથિરીકાઈ કુલમ્બુ', 'તલ અને આમલીની તીખી-ખાટી ગ્રેવીમાં નાના રીંગણનું શાક.');
      case 'p-21': return const LocalizedProductInfo('અપ્પમ બાસ્કેટ (4 નંગ) સ્ટ્યૂ સાથે', 'નરમ જાળીદાર અપ્પમ મલાઈદાર નાળિયેરના સ્ટ્યૂ સાથે.');
      case 'p-22': return const LocalizedProductInfo('મૈસૂર પાક (શુદ્ધ દેશી ઘી)', 'શુદ્ધ ઘી અને બેસનમાંથી બનેલી મોંમાં ઓગળી જતી શાહી મીઠાઈ.');
      case 'p-23': return const LocalizedProductInfo('ઇલાનીર પાયસમ (નાળિયેર ખીર)', 'તાજા નાળિયેરની મલાઈ, દૂધ અને એલચીની સ્વાદિષ્ટ ખીર.');
      case 'p-24': return const LocalizedProductInfo('રવા કેસરી (કાજુ અને કિસમિસ)', 'કેસર અને શુદ્ધ ગાયના ઘીમાં રાંધેલો રવાનો શીરો.');
      case 'p-25': return const LocalizedProductInfo('પાલદા પ્રધમન', 'કેરળની પ્રખ્યાત ચોખાના ફ્લેક્સ અને ઘટ્ટ દૂધની પરંપરાગત ખીર.');
      case 'p-26': return const LocalizedProductInfo('અધિરસમ હેરિટેજ સ્વીટ (4 નંગ)', 'ચોખાના લોટ અને ગોળમાંથી તળેલી સાઉથ ઇન્ડિયન મીઠાઈ.');
      case 'p-27': return const LocalizedProductInfo('થલાઇવા ડિગ્રી ફિલ્ટર કોફી', 'કૂર્ગ કોફી બીન્સમાંથી પિત્તળના ગ્લાસમાં ફીણવાળી ફિલ્ટર કોફી.');
      case 'p-28': return const LocalizedProductInfo('જીગરઠંડા મદુરાઈ સ્પેશિયલ', 'બદામ ગુંદર, નન્નારી સીરપ અને આઈસ્ક્રીમ સાથેનું ઠંડું પીણું.');
      case 'p-29': return const LocalizedProductInfo('સ્પાઈસ્ડ નીર મોર (મસાલા છાશ)', 'આદુ, હિંગ અને લીલા મરચાનો વઘાર કરેલી તાજી છાશ.');
      case 'p-30': return const LocalizedProductInfo('તાજુ નન્નારી શરબત (ચિયા સીડ્સ)', 'નન્નારીના મૂળનો અર્ક, લીંબુનો રસ અને ચિયા સીડ્સ વાળું શરબત.');
    }
  } else if (lang == 'ta') {
    switch (product.id) {
      case 'p-1': return const LocalizedProductInfo('நெய் ரோஸ்ட் மசாலா தோசை', 'சுத்தமான நெய்யில் வறுத்த மொறுமொறு தோசை, உருளைக்கிழங்கு மசாலாவுடன்.');
      case 'p-2': return const LocalizedProductInfo('மைசூர் சீஸ் பர்ஸ்ட் தோசை', 'பூண்டு சட்னி மற்றும் சீஸ் நிறைந்த சுவையான மசாலா தோசை.');
      case 'p-3': return const LocalizedProductInfo('ரவா வெங்காய மசாலா தோசை', 'நறுக்கிய வெங்காயம், சீரகம் மற்றும் முந்திரி கலந்த ரவா தோசை.');
      case 'p-4': return const LocalizedProductInfo('பொடி நெய் கார தோசை', 'காரசாரமான இட்லி பொடி மற்றும் சூடான நெய் தூவிய மொறுமொறு தோசை.');
      case 'p-5': return const LocalizedProductInfo('பேப்பர் பிளேன் ரோஸ்ட் (2.5 அடி)', 'மிகவும் மெல்லிய, மொறுமொறுப்பான 2.5 அடி நீள தோசை 3 வகை சட்னியுடன்.');
      case 'p-6': return const LocalizedProductInfo('செட்டிநாடு பன்னீர் டிக்கா தோசை', 'செட்டிநாடு மிளகு மசாலாவில் வறுத்த பன்னீர் துண்டுகள் கொண்ட தோசை.');
      case 'p-7': return const LocalizedProductInfo('மினி நெய் இட்லி (14 துண்டுகள்)', 'சூடான சாம்பார் மற்றும் நெய்யில் மிதக்கும் 14 பஞ்சு போன்ற மினி இட்லிகள்.');
      case 'p-8': return const LocalizedProductInfo('மெது வடை ஜோடி (சாம்பார் டிப்)', 'மிளகு மற்றும் இஞ்சி நறுமணத்துடன் பொன்னிறமாக வறுத்த மெது வடை.');
      case 'p-9': return const LocalizedProductInfo('காஞ்சிபுரம் கோவில் இட்லி', 'சுக்கு, மிளகு, கறிவேப்பிலை தாளித்த பாரம்பரிய கோவில் இட்லி.');
      case 'p-10': return const LocalizedProductInfo('தென்னிந்திய தயிர் வடை', 'இனிப்பு தயிர் மற்றும் வறுத்த சீரகம் தூவிய மென்மையான வடை.');
      case 'p-11': return const LocalizedProductInfo('தட்டே இட்லி (பொடி & வெண்ணெய்)', 'வெள்ளை வெண்ணெய் மற்றும் பொடி தூவிய பெரிய பெங்களூரு தட்டு இட்லி.');
      case 'p-12': return const LocalizedProductInfo('ஆம்பூர் வெஜ் தம் பிரியாணி', 'சீரக சம்பா அரிசியில் காய்கறிகளுடன் மெதுவாக சமைக்கப்பட்ட பிரியாணி.');
      case 'p-13': return const LocalizedProductInfo('பிசி பேலே பாத் (பூந்தி நறுவல்)', 'கர்நாடக பாரம்பரிய பருப்பு சாதம் நெய் மற்றும் மசாலாவுடன்.');
      case 'p-14': return const LocalizedProductInfo('தாளித்த தயிர் சாதம் (தயிர் சாதம்)', 'கடுகு, பச்சை மிளகாய், மாதுளை தாளித்த கிரீமி தயிர் சாதம்.');
      case 'p-15': return const LocalizedProductInfo('எலுமிச்சை வேர்க்கடலை சாதம்', 'எலுமிச்சை சாறு, மஞ்சள் மற்றும் வறுத்த வேர்க்கடலை சாதம்.');
      case 'p-16': return const LocalizedProductInfo('செட்டிநாடு காளான் பிரியாணி', 'மிளகு மசாலா காளான் மற்றும் வாசனை பாசுமதி அரிசி பிரியாணி.');
      case 'p-17': return const LocalizedProductInfo('செட்டிநாடு பன்னீர் குருமா', 'வறுத்த தேங்காய் மற்றும் மசாலா அரைத்த செட்டிநாடு பன்னீர் குருமா.');
      case 'p-18': return const LocalizedProductInfo('மலபார் காய்கறி ஸ்டூ', 'தேங்காய்ப்பாலில் கேரட், பட்டாணி, உருளைக்கிழங்கு வெந்த மென்மையான ஸ்டூ.');
      case 'p-19': return const LocalizedProductInfo('மெட்ராஸ் முருங்கைக்காய் சாம்பார் (500ml)', 'சின்ன வெங்காயம், முருங்கைக்காய் சேர்த்த பாரம்பரிய மெட்ராஸ் சாம்பார்.');
      case 'p-20': return const LocalizedProductInfo('எண்ணெய் கத்திரிக்காய் குழம்பு', 'எள் மற்றும் புளி மசாலாவில் வதக்கிய சுவையான கத்திரிக்காய் குழம்பு.');
      case 'p-21': return const LocalizedProductInfo('ஆப்பம் கூடை (4 துண்டுகள்) ஸ்டூவுடன்', 'மென்மையான ஆப்பம் சுவையான தேங்காய்ப்பால் ஸ்டூவுடன்.');
      case 'p-22': return const LocalizedProductInfo('மைசூர் பாக் (சுத்தமான நெய்)', 'சுத்தமான நெய் மற்றும் கடலை மாவில் வாயில் கரையும் இனிப்பு.');
      case 'p-23': return const LocalizedProductInfo('இளநீர் பாயாசம் (தேங்காய் பாயாசம்)', 'வழுக்கை இளநீர் மற்றும் ஏலக்காய் மணக்கும் இனிப்பு பாயாசம்.');
      case 'p-24': return const LocalizedProductInfo('ரவா கேசரி (முந்திரி & திராட்சை)', 'குங்குமப்பூ மற்றும் பசு நெய்யில் செய்த சுவையான ரவா கேசரி.');
      case 'p-25': return const LocalizedProductInfo('பாலடை பிரதமன்', 'கேரளாவின் புகழ்பெற்ற அடை மற்றும் கெட்டிப்பால் பாயாசம்.');
      case 'p-26': return const LocalizedProductInfo('அதிரசம் பாரம்பரிய இனிப்பு (4 துண்டுகள்)', 'பச்சரிசி மாவு மற்றும் பனை வெல்லத்தில் செய்த பாரம்பரிய இனிப்பு.');
      case 'p-27': return const LocalizedProductInfo('தலைவா டிகிரி பில்டர் காபி', 'கூர்க் காபி கொட்டைகளில் பித்தளை டம்ளரில் நுரைத்த பில்டர் காபி.');
      case 'p-28': return const LocalizedProductInfo('ஜிகர்தண்டா மதுரை ஸ்பெஷல்', 'பாதாம் பிசின், நன்னாரி சிரப் மற்றும் ஐஸ்கிரீம் குளுமை பானம்.');
      case 'p-29': return const LocalizedProductInfo('மசாலா நீர் மோர்', 'இஞ்சி, பெருங்காயம், பச்சை மிளகாய் தாளித்த குளுமையான மோர்.');
      case 'p-30': return const LocalizedProductInfo('நன்னாரி சர்பத் (சியா விதைகள்)', 'நன்னாரி வேர் சாறு, எலுமிச்சை மற்றும் சியா விதைகள் கலந்த சர்பத்.');
    }
  }
  
  return LocalizedProductInfo(product.name, product.description);
});

bool matchCategory(String productCat, String selectedCat) {
  if (selectedCat == 'All' || selectedCat.isEmpty) return true;
  final s = selectedCat.toLowerCase();
  final p = productCat.toLowerCase();
  if (p == s) return true;
  if (s.contains('dosa') && p.contains('dosa')) return true;
  if ((s.contains('tiffin') || s.contains('idli') || s.contains('vada')) && (p.contains('idli') || p.contains('vada') || p.contains('tiffin'))) return true;
  if ((s.contains('rice') || s.contains('meal') || s.contains('biryani') || s.contains('thali') || s.contains('bread')) && (p.contains('biryani') || p.contains('rice') || p.contains('meal'))) return true;
  if ((s.contains('curri') || s.contains('gravi') || s.contains('kurma') || s.contains('sambar')) && (p.contains('curri') || p.contains('curries'))) return true;
  if ((s.contains('sweet') || s.contains('dessert') || s.contains('payasam')) && (p.contains('dessert') || p.contains('desserts'))) return true;
  if ((s.contains('beverage') || s.contains('kaapi') || s.contains('drink') || s.contains('cooler')) && (p.contains('beverage') || p.contains('beverages'))) return true;
  return false;
}

// Comprehensive Filtered & Sorted Products Engine
final filteredProductsProvider = Provider<List<Product>>((ref) {
  final category = ref.watch(selectedCategoryProvider);
  final query = ref.watch(searchQueryProvider).trim().toLowerCase();
  final dietary = ref.watch(dietaryFilterProvider);
  final bestsellerOnly = ref.watch(bestsellerOnlyProvider);
  final sort = ref.watch(sortByProvider);

  var list = sampleProducts.where((p) {
    // 1. Resilient Category Matching
    final matchesCategory = matchCategory(p.category, category);

    // 2. Search Query Matching
    final matchesQuery = query.isEmpty ||
        p.name.toLowerCase().contains(query) ||
        p.description.toLowerCase().contains(query) ||
        p.category.toLowerCase().contains(query);

    // 3. Dietary Filter
    final matchesDietary = dietary == DietaryFilter.all || (dietary == DietaryFilter.vegOnly && p.isVeg);

    // 4. Bestseller Filter
    final matchesBestseller = !bestsellerOnly || p.isBestseller;

    return matchesCategory && matchesQuery && matchesDietary && matchesBestseller;
  }).toList();

  // 5. Sorting Engine
  switch (sort) {
    case SortOption.rating:
      list.sort((a, b) => b.rating.compareTo(a.rating));
      break;
    case SortOption.priceLowToHigh:
      list.sort((a, b) => a.price.compareTo(b.price));
      break;
    case SortOption.priceHighToLow:
      list.sort((a, b) => b.price.compareTo(a.price));
      break;
    case SortOption.recommended:
      // Default curated order
      break;
  }

  return list;
});

// Category item counter helper for badge chips
final categoryCountProvider = Provider.family<int, String>((ref, cat) {
  if (cat == 'All') return sampleProducts.length;
  return sampleProducts.where((p) => matchCategory(p.category, cat)).length;
});

// ==========================================
// 4. CART & ORDER STATE ENGINE
// ==========================================
class CartState {
  final List<CartItem> items;
  final Coupon? appliedCoupon;
  final double tipAmount;
  final OrderType orderType;

  const CartState({
    this.items = const [],
    this.appliedCoupon,
    this.tipAmount = 0.0,
    this.orderType = OrderType.delivery,
  });

  int get totalItemCount => items.fold(0, (sum, i) => sum + i.quantity);

  double get subtotal => items.fold(0.0, (sum, i) => sum + i.totalPrice);

  double get tax => subtotal * 0.05; // 5% GST

  double get deliveryFee {
    if (orderType != OrderType.delivery) return 0.0;
    if (subtotal == 0) return 0.0;
    return subtotal > 499 ? 0.0 : 40.0; // Free delivery above 499
  }

  double get discountAmount {
    if (appliedCoupon == null) return 0.0;
    if (appliedCoupon!.code == 'THALAIVAA50') return 50.0.clamp(0.0, subtotal);
    if (appliedCoupon!.code == 'FEAST100') return 100.0.clamp(0.0, subtotal);
    return 0.0;
  }

  double get grandTotal {
    final raw = subtotal + tax + deliveryFee + tipAmount - discountAmount;
    return raw > 0 ? raw : 0.0;
  }

  CartState copyWith({
    List<CartItem>? items,
    Coupon? appliedCoupon,
    bool clearCoupon = false,
    double? tipAmount,
    OrderType? orderType,
  }) {
    return CartState(
      items: items ?? this.items,
      appliedCoupon: clearCoupon ? null : (appliedCoupon ?? this.appliedCoupon),
      tipAmount: tipAmount ?? this.tipAmount,
      orderType: orderType ?? this.orderType,
    );
  }
}

class CartNotifier extends StateNotifier<CartState> {
  CartNotifier() : super(const CartState());

  void addItem(Product product, {List<ModifierOption> selectedModifiers = const []}) {
    final existingIndex = state.items.indexWhere(
      (item) => item.product.id == product.id && _modifiersMatch(item.selectedModifiers, selectedModifiers),
    );

    if (existingIndex >= 0) {
      final updated = List<CartItem>.from(state.items);
      final current = updated[existingIndex];
      updated[existingIndex] = current.copyWith(quantity: current.quantity + 1);
      state = state.copyWith(items: updated);
    } else {
      final newItem = CartItem(
        id: 'ci-${DateTime.now().millisecondsSinceEpoch}',
        product: product,
        quantity: 1,
        selectedModifiers: selectedModifiers,
      );
      state = state.copyWith(items: [...state.items, newItem]);
    }
  }

  void removeOne(Product product) {
    final index = state.items.indexWhere((i) => i.product.id == product.id);
    if (index >= 0) {
      final current = state.items[index];
      final updated = List<CartItem>.from(state.items);
      if (current.quantity > 1) {
        updated[index] = current.copyWith(quantity: current.quantity - 1);
      } else {
        updated.removeAt(index);
      }
      state = state.copyWith(items: updated);
    }
  }

  void setTip(double amount) {
    state = state.copyWith(tipAmount: amount);
  }

  void setOrderType(OrderType type) {
    state = state.copyWith(orderType: type);
  }

  bool applyCoupon(String code) {
    final c = code.trim().toUpperCase();
    if (c == 'THALAIVAA50') {
      state = state.copyWith(
        appliedCoupon: const Coupon(id: 'c-1', code: 'THALAIVAA50', discountAmount: 50.0, description: '₹50 Flat Discount'),
      );
      return true;
    } else if (c == 'FEAST100') {
      state = state.copyWith(
        appliedCoupon: const Coupon(id: 'c-2', code: 'FEAST100', discountAmount: 100.0, description: '₹100 Grand Feast Discount'),
      );
      return true;
    }
    return false;
  }

  void removeCoupon() {
    state = state.copyWith(clearCoupon: true);
  }

  void clearCart() {
    state = const CartState();
  }

  int getProductQuantity(String productId) {
    return state.items
        .where((i) => i.product.id == productId)
        .fold(0, (sum, i) => sum + i.quantity);
  }

  bool _modifiersMatch(List<ModifierOption> a, List<ModifierOption> b) {
    if (a.length != b.length) return false;
    final aIds = a.map((e) => e.id).toSet();
    final bIds = b.map((e) => e.id).toSet();
    return aIds.containsAll(bIds);
  }
}

final cartProvider = StateNotifierProvider<CartNotifier, CartState>((ref) {
  return CartNotifier();
});

// Order Tracker
class ActiveOrder {
  final String orderId;
  final Branch branch;
  final List<CartItem> items;
  final double grandTotal;
  final DateTime orderTime;
  final String deliveryAddress;
  final OrderType orderType;

  const ActiveOrder({
    required this.orderId,
    required this.branch,
    required this.items,
    required this.grandTotal,
    required this.orderTime,
    required this.deliveryAddress,
    this.orderType = OrderType.delivery,
  });
}

class OrdersNotifier extends StateNotifier<List<ActiveOrder>> {
  OrdersNotifier() : super([]);

  void placeOrder(CartState cart, Branch branch, DeliveryAddress address) {
    final newOrder = ActiveOrder(
      orderId: 'ORD-${1000 + state.length + 1}',
      branch: branch,
      items: List.from(cart.items),
      grandTotal: cart.grandTotal,
      orderTime: DateTime.now(),
      deliveryAddress: '${address.label}: ${address.addressLine}',
      orderType: cart.orderType,
    );
    state = [newOrder, ...state];
  }
}

final ordersProvider = StateNotifierProvider<OrdersNotifier, List<ActiveOrder>>((ref) {
  return OrdersNotifier();
});

final bottomNavIndexProvider = StateProvider<int>((ref) => 0);
'''

with open(app_providers_path, 'w', encoding='utf-8') as f:
    f.write(APP_PROVIDERS_CODE)

print('app_providers.dart written successfully.')
