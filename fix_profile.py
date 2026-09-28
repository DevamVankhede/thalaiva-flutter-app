import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

profile_screen_dart = '''import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../models/models.dart';
import '../../providers/app_providers.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);
    final language = ref.watch(languageProvider);
    final branches = ref.watch(branchesProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        backgroundColor: cardBg,
        title: Text(tr('profile'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 800),
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              // User Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Row(
                  children: [
                    const CircleAvatar(
                      radius: 28,
                      backgroundColor: ThalaivaaTheme.brandAmber,
                      child: Text('T', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                    ),
                    const SizedBox(width: 14),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Thalaivaa Customer', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                        Text('+91 92170 02598 • Surat, Gujarat', style: TextStyle(color: isDark ? Colors.white60 : Colors.black54, fontSize: 12)),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Theme Settings (Dark / Light)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Appearance & Theme', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            Icon(isDark ? Icons.dark_mode_rounded : Icons.light_mode_rounded, color: ThalaivaaTheme.brandAmber),
                            const SizedBox(width: 10),
                            Text(isDark ? tr('darkMode') : tr('lightMode'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                          ],
                        ),
                        Switch(
                          value: themeMode == ThemeMode.dark,
                          activeThumbColor: ThalaivaaTheme.brandAmber,
                          onChanged: (val) {
                            ref.read(themeModeProvider.notifier).state = val ? ThemeMode.dark : ThemeMode.light;
                          },
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Language Selector (i18n)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.translate_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                        SizedBox(width: 8),
                        Text('Language (ભાષા / भाषा / மொழி)', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
                      children: [
                        {'code': 'en', 'label': 'English'},
                        {'code': 'hi', 'label': 'हिन्दी (Hindi)'},
                        {'code': 'gu', 'label': 'ગુજરાતી (Gujarati)'},
                        {'code': 'ta', 'label': 'தமிழ் (Tamil)'},
                      ].map((item) {
                        final isSel = language == item['code'];
                        return ChoiceChip(
                          label: Text(item['label']!),
                          selected: isSel,
                          selectedColor: ThalaivaaTheme.brandAmber.withValues(alpha: 0.2),
                          onSelected: (_) => ref.read(languageProvider.notifier).state = item['code']!,
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Branch Selector
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: cardBorder),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: const [
                        Icon(Icons.storefront_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                        SizedBox(width: 8),
                        Text('Select Operating Branch', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      ],
                    ),
                    const SizedBox(height: 10),
                    ...branches.map((b) {
                      final isSel = selectedBranch.id == b.id;
                      return ListTile(
                        leading: Icon(
                          isSel ? Icons.radio_button_checked : Icons.radio_button_unchecked,
                          color: isSel ? ThalaivaaTheme.brandAmber : Colors.grey,
                        ),
                        title: Text(b.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                        subtitle: Text('${b.address} • ${b.deliveryTime}', style: const TextStyle(fontSize: 11)),
                        onTap: () {
                          ref.read(selectedBranchProvider.notifier).state = b;
                        },
                      );
                    }).toList(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
'''

base_dir = r"C:\Users\Admin\thalaivaa_flutter\lib"
write_file(os.path.join(base_dir, "features", "profile", "profile_screen.dart"), profile_screen_dart)
print("Updated profile_screen.dart")
