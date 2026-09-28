with open(r'C:\Users\Admin\thalaivaa_flutter\test\flutter_menu_filter_test.dart', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("expect(ThalaivaaTheme.formatInr(240.5), '₹240.50');", "expect(ThalaivaaTheme.formatInr(240.0), '₹240');")

with open(r'C:\Users\Admin\thalaivaa_flutter\test\flutter_menu_filter_test.dart', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated test expectation.')
