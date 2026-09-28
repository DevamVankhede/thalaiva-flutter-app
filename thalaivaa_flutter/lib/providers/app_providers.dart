import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/models.dart';

// 1. Branches Provider (Surat Locations)
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

// 2. 30 Varieties of Authentic South Indian Delicacies
final sampleProducts = <Product>[
  // --- DOSAS & CRISPY ROASTS (6) ---
  const Product(
    id: 'p-1',
    name: 'Ghee Roast Masala Dosa',
    description: 'Crispy golden crepe roasted in pure desi ghee, stuffed with seasoned spiced potato masala.',
    price: 180.0,
    category: 'Dosas & Crispy Roasts',
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
    category: 'Dosas & Crispy Roasts',
    iconEmoji: '🧀',
    isVeg: true,
    isBestseller: true,
    rating: 4.8,
    ratingCount: 290,
  ),
  const Product(
    id: 'p-3',
    name: 'Rava Onion Masala Dosa',
    description: 'Semolina-rice batter laced with finely chopped shallots, crushed cumin, and whole cashews.',
    price: 190.0,
    category: 'Dosas & Crispy Roasts',
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
    category: 'Dosas & Crispy Roasts',
    iconEmoji: '🌶️',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 310,
  ),
  const Product(
    id: 'p-5',
    name: 'Paper Thin Plain Golden Roast',
    description: 'Ultra-thin, crispy long golden crepe served with Madras sambar and 3 freshly ground chutneys.',
    price: 160.0,
    category: 'Dosas & Crispy Roasts',
    iconEmoji: '📜',
    isVeg: true,
    isBestseller: false,
    rating: 4.6,
    ratingCount: 140,
  ),
  const Product(
    id: 'p-6',
    name: 'Chettinad Mushroom Dosa',
    description: 'Stuffed with fresh button mushrooms sautéed in crushed black pepper and stone-ground Chettinad spices.',
    price: 230.0,
    category: 'Dosas & Crispy Roasts',
    iconEmoji: '🍄',
    isVeg: true,
    isBestseller: false,
    rating: 4.8,
    ratingCount: 215,
  ),

  // --- MORNING TIFFIN & TIFFIN (5) ---
  const Product(
    id: 'p-7',
    name: 'Steamed Button Ghee Idli (14 Pcs)',
    description: 'Bite-sized melt-in-mouth rice dumplings floating in steaming hot Drumstick Sambar and ghee.',
    price: 140.0,
    category: 'Morning Tiffin & Tiffin',
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
    category: 'Morning Tiffin & Tiffin',
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
    category: 'Morning Tiffin & Tiffin',
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
    category: 'Morning Tiffin & Tiffin',
    iconEmoji: '🥣',
    isVeg: true,
    isBestseller: false,
    rating: 4.6,
    ratingCount: 160,
  ),
  const Product(
    id: 'p-11',
    name: 'Thatte Idli with Podi & Butter Slab',
    description: 'Large Bangalore-style plate idli topped with dollop of fresh white butter and spicy gunpowder.',
    price: 170.0,
    category: 'Morning Tiffin & Tiffin',
    iconEmoji: '🧈',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 340,
  ),

  // --- SOUTH INDIAN MEALS & THALI / RICE (5) ---
  const Product(
    id: 'p-12',
    name: 'Ambur Veg Dum Biryani',
    description: 'Fragrant Jeeraga Samba rice slow-cooked with garden vegetables, mint, and curd-based gravy.',
    price: 250.0,
    category: 'South Indian Meals & Thali',
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
    category: 'South Indian Meals & Thali',
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
    category: 'South Indian Meals & Thali',
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
    category: 'South Indian Meals & Thali',
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
    category: 'South Indian Meals & Thali',
    iconEmoji: '🍄',
    isVeg: true,
    isBestseller: false,
    rating: 4.8,
    ratingCount: 190,
  ),

  // --- CHETTINAD CURRIES & GRAVIES (5) ---
  const Product(
    id: 'p-17',
    name: 'Chettinad Paneer Kurma',
    description: 'Rich roasted coconut, poppy seeds, and stone flower spiced gravy with cottage cheese.',
    price: 240.0,
    category: 'Chettinad Curries & Gravies',
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
    category: 'Chettinad Curries & Gravies',
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
    category: 'Chettinad Curries & Gravies',
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
    category: 'Chettinad Curries & Gravies',
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
    category: 'Chettinad Curries & Gravies',
    iconEmoji: '🥞',
    isVeg: true,
    isBestseller: true,
    rating: 4.9,
    ratingCount: 280,
  ),

  // --- TRADITIONAL SWEETS & DESSERTS (5) ---
  const Product(
    id: 'p-22',
    name: 'Mysore Pak Melt (Desi Ghee)',
    description: 'Decadent royal sweet made from pure ghee, gram flour, and caramelized sugar.',
    price: 130.0,
    category: 'Traditional Sweets & Desserts',
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
    category: 'Traditional Sweets & Desserts',
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
    category: 'Traditional Sweets & Desserts',
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
    category: 'Traditional Sweets & Desserts',
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
    category: 'Traditional Sweets & Desserts',
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

// Available Categories List
final availableCategoriesProvider = Provider<List<String>>((ref) => const [
  'All',
  'Morning Tiffin & Tiffin',
  'Dosas & Crispy Roasts',
  'South Indian Meals & Thali',
  'Chettinad Curries & Gravies',
  'Traditional Sweets & Desserts',
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
final languageProvider = StateProvider<String>((ref) => 'en');
final deliveryTipProvider = StateProvider<double>((ref) => 0.0);

// Multi-Language Localization Dictionary
final translationsProvider = Provider<Map<String, Map<String, String>>>((ref) {
  return {
    'en': {
      'appName': 'THALAIVAA',
      'tagline': 'Authentic South Indian Cuisine',
      'searchHint': 'Search Dosas, Idlis, Filter Kaapi, Thali...',
      'all': 'All',
      'pureVeg': 'Pure Veg',
      'bestsellers': '⭐ Bestsellers',
      'sort': 'Sort',
      'add': 'ADD +',
      'addToTray': 'Add to Tray',
      'cart': 'Tray',
      'order': 'Live Order',
      'profile': 'Settings',
      'checkout': 'Proceed to Pay',
      'subtotal': 'Item Total',
      'gst': 'GST & Restaurant Taxes (5%)',
      'deliveryFee': 'Delivery Partner Fee',
      'discount': 'Special Coupon Discount',
      'grandTotal': 'To Pay',
      'applyCoupon': 'Apply Coupon',
      'selectBranch': 'Select Branch',
      'tracking': 'Live Order Tracking',
      'reorder': 'Reorder',
      'lightMode': 'Light Theme',
      'darkMode': 'Dark Theme',
      'language': 'Language',
    },
    'hi': {
      'appName': 'थलाइवा',
      'tagline': 'प्रामाणिक दक्षिण भारतीय व्यंजन',
      'searchHint': 'डोसा, इडली, फिल्टर कॉफी, बिरयानी खोजें...',
      'all': 'सभी',
      'pureVeg': 'शुद्ध शाकाहारी',
      'bestsellers': '⭐ सबसे लोकप्रिय',
      'sort': 'क्रमबद्ध करें',
      'add': 'जोड़ें +',
      'addToTray': 'ट्रे में जोड़ें',
      'cart': 'ट्रे',
      'order': 'ऑर्डर ट्रैक',
      'profile': 'सेटिंग्स',
      'checkout': 'भुगतान करें',
      'subtotal': 'कुल मूल्य',
      'gst': 'जीएसटी और रेस्टोरेंट टैक्स (5%)',
      'deliveryFee': 'डिलीवरी शुल्क',
      'discount': 'कूपन छूट',
      'grandTotal': 'कुल देय',
      'applyCoupon': 'कूपन लागू करें',
      'selectBranch': 'शाखा चुनें',
      'tracking': 'लाइव ऑर्डर ट्रैकिंग',
      'reorder': 'पुनः ऑर्डर करें',
      'lightMode': 'लाइट थीम',
      'darkMode': 'डार्क थीम',
      'language': 'भाषा',
    },
    'gu': {
      'appName': 'થલાઈવા',
      'tagline': 'અસલી દક્ષિણ ભારતીય સ્વાદ',
      'searchHint': 'ઢોસા, ઈડલી, ફિલ્ટર કોફી, બિરયાની શોધો...',
      'all': 'બધું',
      'pureVeg': 'શુદ્ધ શાકાહારી',
      'bestsellers': '⭐ લોકપ્રિય',
      'sort': 'ક્રમ',
      'add': 'ઉમેરો +',
      'addToTray': 'ટ્રેમાં ઉમેરો',
      'cart': 'ટ્રે',
      'order': 'ઓર્ડર ટ્રેકિંગ',
      'profile': 'સેટિંગ્સ',
      'checkout': 'પેમેન્ટ કરો',
      'subtotal': 'કુલ કિંમત',
      'gst': 'જીએસટી અને ટેક્સ (5%)',
      'deliveryFee': 'ડિલિવરી ચાર્જ',
      'discount': 'કૂપન ડિસ્કાઉન્ટ',
      'grandTotal': 'ચૂકવવાપાત્ર',
      'applyCoupon': 'કૂપન લાગુ કરો',
      'selectBranch': 'શાખા પસંદ કરો',
      'tracking': 'લાઈવ ઓર્ડર ટ્રેક',
      'reorder': 'ફરી ઓર્ડર કરો',
      'lightMode': 'લાઇટ થીમ',
      'darkMode': 'ડાર્ક થીમ',
      'language': 'ભાષા',
    },
    'ta': {
      'appName': 'தலைவா',
      'tagline': 'பாரம்பரிய தென்னிந்திய சுவை',
      'searchHint': 'தோசை, இட்லி, பில்டர் காபி, பிரியாணி தேடுங்கள்...',
      'all': 'அனைத்தும்',
      'pureVeg': 'சைவம் மட்டும்',
      'bestsellers': '⭐ பிரபல உணவுகள்',
      'sort': 'வரிசைப்படுத்து',
      'add': 'சேர் +',
      'addToTray': 'கூடையில் சேர்',
      'cart': 'கூடை',
      'order': 'ஆர்டர் நிலை',
      'profile': 'அமைப்புகள்',
      'checkout': 'பணம் செலுத்துக',
      'subtotal': 'உணவு மொத்தம்',
      'gst': 'ஜிஎஸ்டி வரிகள் (5%)',
      'deliveryFee': 'டெலிவரி கட்டணம்',
      'discount': 'தள்ளுபடி',
      'grandTotal': 'செலுத்த வேண்டியது',
      'applyCoupon': 'கூப்பன் சேர்',
      'selectBranch': 'கிளையை தேர்ந்தெடுக்கவும்',
      'tracking': 'நேரலை கண்காணிப்பு',
      'reorder': 'மீண்டும் ஆர்டர் செய்க',
      'lightMode': 'வெளிச்ச தீம்',
      'darkMode': 'இருண்ட தீம்',
      'language': 'மொழி',
    },
  };
});

final trProvider = Provider<String Function(String)>((ref) {
  final lang = ref.watch(languageProvider);
  final map = ref.watch(translationsProvider);
  final currentMap = map[lang] ?? map['en']!;
  return (String key) => currentMap[key] ?? map['en']![key] ?? key;
});

bool matchCategory(String productCat, String selectedCat) {
  if (selectedCat == 'All' || selectedCat.isEmpty) return true;
  final s = selectedCat.toLowerCase();
  final p = productCat.toLowerCase();
  if (p == s) return true;
  if (s.contains('dosa') && (p.contains('dosa') || p.contains('roast'))) return true;
  if ((s.contains('tiffin') || s.contains('idli') || s.contains('vada')) && (p.contains('idli') || p.contains('vada') || p.contains('tiffin'))) return true;
  if ((s.contains('rice') || s.contains('meal') || s.contains('biryani') || s.contains('thali') || s.contains('bread')) && (p.contains('biryani') || p.contains('rice') || p.contains('meal') || p.contains('thali'))) return true;
  if ((s.contains('curri') || s.contains('gravi') || s.contains('kurma') || s.contains('sambar') || s.contains('stew')) && (p.contains('curri') || p.contains('gravi') || p.contains('kurma') || p.contains('sambar') || p.contains('stew'))) return true;
  if ((s.contains('sweet') || s.contains('dessert') || s.contains('payasam') || s.contains('kesari') || s.contains('pak')) && (p.contains('sweet') || p.contains('dessert') || p.contains('payasam') || p.contains('kesari') || p.contains('pak'))) return true;
  if ((s.contains('beverage') || s.contains('kaapi') || s.contains('drink') || s.contains('cooler') || s.contains('coffee')) && (p.contains('beverage') || p.contains('kaapi') || p.contains('drink') || p.contains('cooler') || p.contains('coffee'))) return true;
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
    final matchesCategory = matchCategory(p.category, category);
    final matchesQuery = query.isEmpty ||
        p.name.toLowerCase().contains(query) ||
        p.description.toLowerCase().contains(query) ||
        p.category.toLowerCase().contains(query);
    final matchesDietary = dietary == DietaryFilter.all || (dietary == DietaryFilter.vegOnly && p.isVeg);
    final matchesBestseller = !bestsellerOnly || p.isBestseller;

    return matchesCategory && matchesQuery && matchesDietary && matchesBestseller;
  }).toList();

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
      break;
  }

  return list;
});

// Category item counter helper for badge chips
final categoryCountProvider = Provider.family<int, String>((ref, cat) {
  if (cat == 'All') return sampleProducts.length;
  return sampleProducts.where((p) => matchCategory(p.category, cat)).length;
});

// 3. Cart State Management
class CartState {
  final List<CartItem> items;
  final String? appliedCoupon;
  final double discountAmount;
  final String deliveryAddress;
  final bool isDelivery;
  final double tipAmount;

  const CartState({
    this.items = const [],
    this.appliedCoupon,
    this.discountAmount = 0.0,
    this.deliveryAddress = 'Flat 402, Royal Palms, City Light, Surat',
    this.isDelivery = true,
    this.tipAmount = 0.0,
  });

  int get totalItemCount => items.fold(0, (sum, item) => sum + item.quantity);
  double get subtotal => items.fold(0.0, (sum, item) => sum + item.totalPrice);
  double get tax => subtotal * 0.05;
  double get deliveryFee => (subtotal > 499.0 || !isDelivery || items.isEmpty) ? 0.0 : 40.0;

  double get grandTotal {
    final total = subtotal + tax + deliveryFee + tipAmount - discountAmount;
    return total > 0 ? total : 0;
  }

  CartState copyWith({
    List<CartItem>? items,
    String? appliedCoupon,
    double? discountAmount,
    String? deliveryAddress,
    bool? isDelivery,
    double? tipAmount,
  }) {
    return CartState(
      items: items ?? this.items,
      appliedCoupon: appliedCoupon,
      discountAmount: discountAmount ?? this.discountAmount,
      deliveryAddress: deliveryAddress ?? this.deliveryAddress,
      isDelivery: isDelivery ?? this.isDelivery,
      tipAmount: tipAmount ?? this.tipAmount,
    );
  }
}

class CartNotifier extends StateNotifier<CartState> {
  CartNotifier() : super(const CartState());

  void addItem(Product product, {List<ModifierOption> modifiers = const [], String? instructions}) {
    final existingIndex = state.items.indexWhere((i) =>
        i.product.id == product.id &&
        listEquals(i.selectedModifiers.map((m) => m.id).toList(), modifiers.map((m) => m.id).toList()));

    if (existingIndex >= 0) {
      final updatedList = List<CartItem>.from(state.items);
      final item = updatedList[existingIndex];
      updatedList[existingIndex] = item.copyWith(quantity: item.quantity + 1);
      state = state.copyWith(items: updatedList);
    } else {
      final newItem = CartItem(
        id: 'cart-${DateTime.now().millisecondsSinceEpoch}',
        product: product,
        quantity: 1,
        selectedModifiers: modifiers,
        instructions: instructions,
      );
      state = state.copyWith(items: [...state.items, newItem]);
    }
    _recalculateDiscount();
  }

  void updateQuantity(String itemId, int delta) {
    final updatedList = <CartItem>[];
    for (final item in state.items) {
      if (item.id == itemId) {
        final newQty = item.quantity + delta;
        if (newQty > 0) {
          updatedList.add(item.copyWith(quantity: newQty));
        }
      } else {
        updatedList.add(item);
      }
    }
    state = state.copyWith(items: updatedList);
    _recalculateDiscount();
  }

  void removeItem(String itemId) {
    state = state.copyWith(items: state.items.where((i) => i.id != itemId).toList());
    _recalculateDiscount();
  }

  void setTip(double amount) {
    state = state.copyWith(tipAmount: amount);
  }

  void clearCart() {
    state = const CartState();
  }

  bool applyCoupon(String code) {
    final clean = code.trim().toUpperCase();
    if (clean == 'THALAIVAA50' && state.subtotal >= 200) {
      state = state.copyWith(appliedCoupon: clean, discountAmount: 50.0);
      return true;
    } else if (clean == 'FEAST100' && state.subtotal >= 500) {
      state = state.copyWith(appliedCoupon: clean, discountAmount: 100.0);
      return true;
    }
    return false;
  }

  void removeCoupon() {
    state = state.copyWith(appliedCoupon: null, discountAmount: 0.0);
  }

  void toggleDelivery(bool isDelivery) {
    state = state.copyWith(isDelivery: isDelivery);
  }

  void setDeliveryAddress(String address) {
    state = state.copyWith(deliveryAddress: address);
  }

  void _recalculateDiscount() {
    if (state.appliedCoupon == 'THALAIVAA50' && state.subtotal < 200) {
      removeCoupon();
    } else if (state.appliedCoupon == 'FEAST100' && state.subtotal < 500) {
      removeCoupon();
    }
  }
}

final cartProvider = StateNotifierProvider<CartNotifier, CartState>((ref) {
  return CartNotifier();
});

// 4. Order Tracking State
class OrdersNotifier extends StateNotifier<List<OrderModel>> {
  OrdersNotifier()
      : super([
          OrderModel(
            id: 'ord-101',
            orderNumber: 'THL-9482',
            items: [
              CartItem(
                id: 'ci-1',
                product: sampleProducts[0],
                quantity: 2,
              ),
              CartItem(
                id: 'ci-2',
                product: sampleProducts[26],
                quantity: 2,
              ),
            ],
            subtotal: 500.0,
            tax: 25.0,
            deliveryFee: 0.0,
            discount: 50.0,
            grandTotal: 475.0,
            status: OrderStatus.preparing,
            createdAt: DateTime.now().subtract(const Duration(minutes: 12)),
            branch: const Branch(
              id: 'br-1',
              name: 'Thalaivaa - City Light (Main)',
              address: 'Shop 12-14, City Light Town, Surat',
              phone: '+91 92170 02598',
            ),
            deliveryAddress: 'Flat 402, Royal Palms, City Light, Surat',
          ),
        ]);

  void placeOrder(CartState cart, Branch branch) {
    final newOrder = OrderModel(
      id: 'ord-${DateTime.now().millisecondsSinceEpoch}',
      orderNumber: 'THL-${1000 + (DateTime.now().millisecond % 9000)}',
      items: List.from(cart.items),
      subtotal: cart.subtotal,
      tax: cart.tax,
      deliveryFee: cart.deliveryFee,
      discount: cart.discountAmount,
      grandTotal: cart.grandTotal,
      status: OrderStatus.confirmed,
      createdAt: DateTime.now(),
      branch: branch,
      deliveryAddress: cart.deliveryAddress,
    );
    state = [newOrder, ...state];
  }
}

final ordersProvider = StateNotifierProvider<OrdersNotifier, List<OrderModel>>((ref) {
  return OrdersNotifier();
});

// 5. Navigation Provider (0: Menu, 1: Cart, 2: Orders, 3: Profile)
final bottomNavIndexProvider = StateProvider<int>((ref) => 0);
