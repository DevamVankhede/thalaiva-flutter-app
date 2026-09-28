# Clean 2 lints
with open(r'C:\Users\Admin\thalaivaa_flutter\lib\providers\app_providers.dart', 'r', encoding='utf-8') as f:
    c1 = f.read()

c1 = c1.replace("import 'package:flutter/foundation.dart';\n", "")
with open(r'C:\Users\Admin\thalaivaa_flutter\lib\providers\app_providers.dart', 'w', encoding='utf-8') as f:
    f.write(c1)

with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\cart\cart_screen.dart', 'r', encoding='utf-8') as f:
    c2 = f.read()

c2 = c2.replace("activeColor: ThalaivaaTheme.brandAmber,", "activeThumbColor: ThalaivaaTheme.brandAmber,")
with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\cart\cart_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c2)

print('Lints cleaned.')
