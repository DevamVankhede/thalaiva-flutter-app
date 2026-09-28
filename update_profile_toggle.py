# Professional Theme Switcher & Language Selector upgrade
import os

PROFILE_SCREEN_CODE = r'''import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../providers/app_providers.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);
    final language = ref.watch(languageProvider);
    final branches = ref.watch(branchesProvider);
    final selectedBranch = ref.watch(selectedBranchProvider);
    final addresses = ref.watch(savedAddressesProvider);
    final tr = ref.watch(trProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final bg = isDark ? ThalaivaaTheme.obsidianBg : const Color(0xFFF8FAFC);
    final cardBg = isDark ? ThalaivaaTheme.surfaceCard : Colors.white;
    final cardBorder = isDark ? ThalaivaaTheme.borderDark : const Color(0xFFE2E8F0);
    final toggleTrackBg = isDark ? const Color(0xFF0F172A) : const Color(0xFFF1F5F9);

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        title: Text(tr('profile'), style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 18)),
        elevation: 0,
        backgroundColor: cardBg,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(16, 14, 16, 40),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // 1. Professional Segmented Theme Switcher
                Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: cardBorder),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: isDark ? 0.2 : 0.03),
                        blurRadius: 12,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                                  shape: BoxShape.circle,
                                ),
                                child: const Icon(Icons.palette_rounded, color: ThalaivaaTheme.brandAmber, size: 18),
                              ),
                              const SizedBox(width: 10),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    tr('themeMode'),
                                    style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14),
                                  ),
                                  const SizedBox(height: 2),
                                  Text(
                                    isDark ? 'Obsidian Dark Mode Active' : 'Clean Light Mode Active',
                                    style: TextStyle(
                                      fontSize: 11,
                                      color: isDark ? Colors.white54 : const Color(0xFF64748B),
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                          // Live active indicator badge
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(
                              color: isDark ? const Color(0xFF334155) : const Color(0xFFFEF3C7),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(
                                  isDark ? Icons.nightlight_round : Icons.wb_sunny_rounded,
                                  size: 12,
                                  color: isDark ? const Color(0xFF94A3B8) : const Color(0xFFD97706),
                                ),
                                const SizedBox(width: 4),
                                Text(
                                  isDark ? 'DARK' : 'LIGHT',
                                  style: TextStyle(
                                    fontSize: 10,
                                    fontWeight: FontWeight.w800,
                                    color: isDark ? const Color(0xFFF8FAFC) : const Color(0xFFB45309),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),

                      const SizedBox(height: 16),

                      // Professional Segmented Sliding Toggle
                      Container(
                        height: 50,
                        padding: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: toggleTrackBg,
                          borderRadius: BorderRadius.circular(14),
                          border: Border.all(color: cardBorder),
                        ),
                        child: Row(
                          children: [
                            // Light Mode Segment
                            Expanded(
                              child: InkWell(
                                onTap: () => ref.read(themeModeProvider.notifier).state = ThemeMode.light,
                                borderRadius: BorderRadius.circular(10),
                                child: AnimatedContainer(
                                  duration: const Duration(milliseconds: 220),
                                  curve: Curves.easeInOut,
                                  decoration: BoxDecoration(
                                    color: themeMode == ThemeMode.light
                                        ? (isDark ? const Color(0xFF1E293B) : Colors.white)
                                        : Colors.transparent,
                                    borderRadius: BorderRadius.circular(10),
                                    boxShadow: themeMode == ThemeMode.light
                                        ? [
                                            BoxShadow(
                                              color: Colors.black.withValues(alpha: isDark ? 0.3 : 0.08),
                                              blurRadius: 6,
                                              offset: const Offset(0, 2),
                                            ),
                                          ]
                                        : null,
                                  ),
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(
                                        Icons.wb_sunny_rounded,
                                        size: 16,
                                        color: themeMode == ThemeMode.light
                                            ? const Color(0xFFEA580C)
                                            : (isDark ? Colors.white38 : const Color(0xFF94A3B8)),
                                      ),
                                      const SizedBox(width: 8),
                                      Text(
                                        'Clean Light',
                                        style: TextStyle(
                                          fontSize: 13,
                                          fontWeight: themeMode == ThemeMode.light ? FontWeight.w800 : FontWeight.w600,
                                          color: themeMode == ThemeMode.light
                                              ? (isDark ? Colors.white : const Color(0xFF0F172A))
                                              : (isDark ? Colors.white54 : const Color(0xFF64748B)),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),

                            const SizedBox(width: 4),

                            // Dark Mode Segment
                            Expanded(
                              child: InkWell(
                                onTap: () => ref.read(themeModeProvider.notifier).state = ThemeMode.dark,
                                borderRadius: BorderRadius.circular(10),
                                child: AnimatedContainer(
                                  duration: const Duration(milliseconds: 220),
                                  curve: Curves.easeInOut,
                                  decoration: BoxDecoration(
                                    color: themeMode == ThemeMode.dark
                                        ? (isDark ? const Color(0xFF1E293B) : const Color(0xFF0F172A))
                                        : Colors.transparent,
                                    borderRadius: BorderRadius.circular(10),
                                    boxShadow: themeMode == ThemeMode.dark
                                        ? [
                                            BoxShadow(
                                              color: Colors.black.withValues(alpha: 0.25),
                                              blurRadius: 8,
                                              offset: const Offset(0, 2),
                                            ),
                                          ]
                                        : null,
                                  ),
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(
                                        Icons.dark_mode_rounded,
                                        size: 16,
                                        color: themeMode == ThemeMode.dark
                                            ? const Color(0xFFF59E0B)
                                            : (isDark ? Colors.white38 : const Color(0xFF94A3B8)),
                                      ),
                                      const SizedBox(width: 8),
                                      Text(
                                        'Obsidian Dark',
                                        style: TextStyle(
                                          fontSize: 13,
                                          fontWeight: themeMode == ThemeMode.dark ? FontWeight.w800 : FontWeight.w600,
                                          color: themeMode == ThemeMode.dark
                                              ? Colors.white
                                              : (isDark ? Colors.white54 : const Color(0xFF64748B)),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 2. Multi-Language Switcher (Professional 2x2 Grid with Script Badges)
                Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: cardBorder),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: isDark ? 0.2 : 0.03),
                        blurRadius: 12,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.translate_rounded, color: ThalaivaaTheme.brandAmber, size: 18),
                          ),
                          const SizedBox(width: 10),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(tr('language'), style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14)),
                              const SizedBox(height: 2),
                              Text(
                                'Instant real-time app translation',
                                style: TextStyle(fontSize: 11, color: isDark ? Colors.white54 : const Color(0xFF64748B)),
                              ),
                            ],
                          ),
                        ],
                      ),
                      const SizedBox(height: 14),
                      GridView.count(
                        crossAxisCount: 2,
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        crossAxisSpacing: 10,
                        mainAxisSpacing: 10,
                        childAspectRatio: 2.4,
                        children: [
                          {'code': 'en', 'title': 'English', 'native': 'English', 'flag': '🇬🇧'},
                          {'code': 'hi', 'title': 'Hindi', 'native': 'हिन्दी', 'flag': '🇮🇳'},
                          {'code': 'gu', 'title': 'Gujarati', 'native': 'ગુજરાતી', 'flag': '🇮🇳'},
                          {'code': 'ta', 'title': 'Tamil', 'native': 'தமிழ்', 'flag': '🇮🇳'},
                        ].map((item) {
                          final isSel = language == item['code'];
                          return InkWell(
                            onTap: () => ref.read(languageProvider.notifier).state = item['code']!,
                            borderRadius: BorderRadius.circular(14),
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 200),
                              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                              decoration: BoxDecoration(
                                color: isSel
                                    ? ThalaivaaTheme.brandAmber.withValues(alpha: isDark ? 0.2 : 0.1)
                                    : toggleTrackBg,
                                borderRadius: BorderRadius.circular(14),
                                border: Border.all(
                                  color: isSel
                                      ? ThalaivaaTheme.brandAmber
                                      : cardBorder,
                                  width: isSel ? 2 : 1,
                                ),
                              ),
                              child: Row(
                                children: [
                                  Text(item['flag']!, style: const TextStyle(fontSize: 18)),
                                  const SizedBox(width: 8),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Text(
                                          item['native']!,
                                          style: TextStyle(
                                            fontWeight: FontWeight.w800,
                                            fontSize: 13,
                                            color: isSel
                                                ? ThalaivaaTheme.brandAmber
                                                : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                          ),
                                        ),
                                        Text(
                                          item['title']!,
                                          style: TextStyle(
                                            fontSize: 10,
                                            color: isDark ? Colors.white54 : const Color(0xFF64748B),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  if (isSel)
                                    const Icon(Icons.check_circle_rounded, color: ThalaivaaTheme.brandAmber, size: 18),
                                ],
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 3. Saved Addresses
                Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: cardBorder),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: isDark ? 0.2 : 0.03),
                        blurRadius: 12,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.location_on_rounded, color: ThalaivaaTheme.brandAmber, size: 18),
                          ),
                          const SizedBox(width: 10),
                          Text(tr('savedAddresses'), style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14)),
                        ],
                      ),
                      const SizedBox(height: 12),
                      ...addresses.map((addr) {
                        return Container(
                          margin: const EdgeInsets.only(bottom: 8),
                          decoration: BoxDecoration(
                            color: toggleTrackBg,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: cardBorder),
                          ),
                          child: Material(
                            color: Colors.transparent,
                            child: ListTile(
                              leading: Icon(
                                addr.label == 'Home'
                                    ? Icons.home_rounded
                                    : (addr.label == 'Work' ? Icons.business_rounded : Icons.place_rounded),
                                color: ThalaivaaTheme.brandAmber,
                              ),
                              title: Text(addr.label, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                              subtitle: Text('${addr.addressLine} • ${addr.landmark}', style: const TextStyle(fontSize: 11)),
                            ),
                          ),
                        );
                      }).toList(),
                    ],
                  ),
                ),

                const SizedBox(height: 16),

                // 4. Branch Selector
                Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: cardBorder),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: isDark ? 0.2 : 0.03),
                        blurRadius: 12,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.storefront_rounded, color: ThalaivaaTheme.brandAmber, size: 18),
                          ),
                          const SizedBox(width: 10),
                          Text(tr('operatingBranch'), style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14)),
                        ],
                      ),
                      const SizedBox(height: 12),
                      ...branches.map((b) {
                        final isSel = selectedBranch.id == b.id;
                        return Container(
                          margin: const EdgeInsets.only(bottom: 8),
                          decoration: BoxDecoration(
                            color: isSel ? ThalaivaaTheme.brandAmber.withValues(alpha: isDark ? 0.15 : 0.08) : toggleTrackBg,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: isSel ? ThalaivaaTheme.brandAmber : cardBorder,
                            ),
                          ),
                          child: Material(
                            color: Colors.transparent,
                            child: ListTile(
                              leading: Icon(
                                isSel ? Icons.radio_button_checked : Icons.radio_button_unchecked,
                                color: isSel ? ThalaivaaTheme.brandAmber : Colors.grey,
                              ),
                              title: Text(b.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                              subtitle: Text('${b.address} • ${b.deliveryTime}', style: const TextStyle(fontSize: 11)),
                              trailing: isSel ? const Icon(Icons.check_circle_rounded, color: ThalaivaaTheme.brandAmber, size: 18) : null,
                              onTap: () {
                                ref.read(selectedBranchProvider.notifier).state = b;
                              },
                            ),
                          ),
                        );
                      }).toList(),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
'''

with open(r'C:\Users\Admin\thalaivaa_flutter\lib\features\profile\profile_screen.dart', 'w', encoding='utf-8') as f:
    f.write(PROFILE_SCREEN_CODE)

print('Updated profile_screen.dart with professional segmented toggle and language grid.')
