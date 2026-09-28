import os, re

# 1. Update web/index.html with aggressive cache-busting & service-worker unregister
index_html = '''<!DOCTYPE html>
<html>
<head>
  <base href="$FLUTTER_BASE_HREF">
  <meta charset="UTF-8">
  <meta content="IE=Edge" http-equiv="X-UA-Compatible">
  <meta name="description" content="Thalaivaa Food-Tech Platform">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
  <meta http-equiv="Pragma" content="no-cache" />
  <meta http-equiv="Expires" content="0" />

  <!-- iOS meta tags & icons -->
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <meta name="apple-mobile-web-app-title" content="thalaivaa_flutter">
  <link rel="apple-touch-icon" href="icons/Icon-192.png">

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="favicon.png"/>

  <title>Thalaivaa - Authentic South Indian Cuisine</title>
  <link rel="manifest" href="manifest.json">
  <script>
    // Force unregister stale service worker to guarantee immediate updates
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.getRegistrations().then(function(registrations) {
        for(let registration of registrations) {
          registration.unregister();
        }
      });
    }
    if ('caches' in window) {
      caches.keys().then(function(names) {
        for (let name of names) caches.delete(name);
      });
    }
  </script>
</head>
<body>
  <script src="flutter_bootstrap.js?v=2.0" async></script>
</body>
</html>
'''

with open(r"C:\Users\Admin\thalaivaa_flutter\web\index.html", 'w', encoding='utf-8') as f:
    f.write(index_html)
print("Updated web/index.html")

# 2. Add resilient bidirectional category matching to app_providers.dart
with open(r"C:\Users\Admin\thalaivaa_flutter\lib\providers\app_providers.dart", 'r', encoding='utf-8') as f:
    app_providers_code = f.read()

robust_matcher = '''bool matchCategory(String productCat, String selectedCat) {
  if (selectedCat == 'All' || selectedCat.isEmpty) return true;
  final s = selectedCat.toLowerCase();
  final p = productCat.toLowerCase();
  if (p == s) return true;
  if (s.contains('dosa') && p.contains('dosa')) return true;
  if ((s.contains('tiffin') || s.contains('idli') || s.contains('vada')) && (p.contains('idli') || p.contains('vada') || p.contains('tiffin'))) return true;
  if ((s.contains('rice') || s.contains('meal') || s.contains('biryani') || s.contains('thali') || s.contains('bread')) && (p.contains('biryani') || p.contains('rice') || p.contains('meal'))) return true;
  if ((s.contains('curri') || s.contains('gravi') || s.contains('kurma') || s.contains('sambar')) && p.contains('curri')) return true;
  if ((s.contains('sweet') || s.contains('dessert') || s.contains('payasam')) && p.contains('dessert')) return true;
  if ((s.contains('beverage') || s.contains('kaapi') || s.contains('drink') || s.contains('cooler')) && p.contains('beverage')) return true;
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
'''

# Replace the filteredProductsProvider in app_providers.dart
pattern = r'// Comprehensive Filtered & Sorted Products Engine\s+final filteredProductsProvider = Provider<List<Product>>\(.+?\n\}\);\n'
app_providers_code = re.sub(pattern, robust_matcher, app_providers_code, flags=re.DOTALL)

with open(r"C:\Users\Admin\thalaivaa_flutter\lib\providers\app_providers.dart", 'w', encoding='utf-8') as f:
    f.write(app_providers_code)
print("Updated app_providers.dart with matchCategory")
