# Add theme quick toggle to menu_screen.dart
import os

with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\menu\menu_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

target = r'''            // Quick 1-Tap Language Switcher
            InkWell('''

replacement = r'''            // 1-Tap Quick Theme Toggle (Light / Dark)
            InkWell(
              onTap: () {
                ref.read(themeModeProvider.notifier).state =
                    isDark ? ThemeMode.light : ThemeMode.dark;
              },
              borderRadius: BorderRadius.circular(20),
              child: Container(
                padding: const EdgeInsets.all(7),
                decoration: BoxDecoration(
                  color: isDark ? const Color(0xFF1E293B) : const Color(0xFFFFF7ED),
                  shape: BoxShape.circle,
                  border: Border.all(color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.3)),
                ),
                child: Icon(
                  isDark ? Icons.nightlight_round : Icons.wb_sunny_rounded,
                  size: 16,
                  color: isDark ? const Color(0xFFFBBF24) : const Color(0xFFEA580C),
                ),
              ),
            ),
            const SizedBox(width: 8),
            // Quick 1-Tap Language Switcher
            InkWell('''

if target in code:
    code = code.replace(target, replacement)
    with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\menu\menu_screen.dart', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Added Quick Theme Toggle to Menu Header')
