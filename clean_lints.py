import os

# 1. Clean order_screen.dart
order_path = r"C:\Users\Admin\thalaivaa_flutter\lib\features\order\order_screen.dart"
with open(order_path, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("import '../../models/models.dart';\n", "")
c = c.replace("import '../../models/cart_item.dart';\n", "")
with open(order_path, 'w', encoding='utf-8') as f:
    f.write(c)

# 2. Clean profile_screen.dart
prof_path = r"C:\Users\Admin\thalaivaa_flutter\lib\features\profile\profile_screen.dart"
with open(prof_path, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("import '../../models/models.dart';\n", "")
with open(prof_path, 'w', encoding='utf-8') as f:
    f.write(c)

# 3. Clean app_providers.dart switch default
prov_path = r"C:\Users\Admin\thalaivaa_flutter\lib\providers\app_providers.dart"
with open(prov_path, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("    case SortOption.recommended:\n    default:\n      // Default curated order\n      break;", "    case SortOption.recommended:\n      // Default curated order\n      break;")
with open(prov_path, 'w', encoding='utf-8') as f:
    f.write(c)

# 4. Clean test/flutter_menu_filter_test.dart
test_path = r"C:\Users\Admin\thalaivaa_flutter\test\flutter_menu_filter_test.dart"
with open(test_path, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("import 'package:flutter/material.dart';\n", "")
c = c.replace("import 'package:thalaivaa_flutter/models/models.dart';\n", "")
with open(test_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Cleaned up unused imports & warnings")
