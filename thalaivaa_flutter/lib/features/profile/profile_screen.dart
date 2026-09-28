import 'package:flutter/material.dart';
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
              // User Account & Interactive OTP Login Card
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
                      children: [
                        CircleAvatar(
                          radius: 26,
                          backgroundColor: ThalaivaaTheme.brandAmber,
                          child: const Text('T', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('Ramesh Patel', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                              Text('+91 92170 02598 • Surat Outlet', style: TextStyle(color: isDark ? Colors.white60 : Colors.black54, fontSize: 12)),
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.green.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: Colors.green),
                          ),
                          child: const Text('🔐 Logged In', style: TextStyle(color: Colors.green, fontSize: 11, fontWeight: FontWeight.bold)),
                        ),
                      ],
                    ),
                    const SizedBox(height: 14),
                    const Divider(),
                    const SizedBox(height: 10),
                    const Text('Mobile OTP Authentication', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: TextEditingController(text: '+91 92170 02598'),
                            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                            decoration: InputDecoration(
                              labelText: 'Mobile Phone',
                              labelStyle: const TextStyle(fontSize: 11),
                              prefixIcon: const Icon(Icons.phone_android_rounded, size: 16),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton.icon(
                          onPressed: () {},
                          icon: const Icon(Icons.send_rounded, size: 14),
                          label: const Text('Send OTP', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: ThalaivaaTheme.brandAmber,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: TextEditingController(text: '123456'),
                            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, letterSpacing: 3),
                            decoration: InputDecoration(
                              labelText: '6-Digit OTP (Dev: 123456)',
                              labelStyle: const TextStyle(fontSize: 11),
                              prefixIcon: const Icon(Icons.lock_clock_rounded, size: 16),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton.icon(
                          onPressed: () {},
                          icon: const Icon(Icons.verified_user_rounded, size: 14),
                          label: const Text('Verify', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Logout & Session Management Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardBg,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.red.withValues(alpha: 0.3)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text('Session & Account', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        SizedBox(height: 2),
                        Text('Revoke Sanctum token & sign out', style: TextStyle(fontSize: 11, color: Colors.grey)),
                      ],
                    ),
                    ElevatedButton.icon(
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('🚪 Logged Out Successfully. Please log in to place orders.'))
                        );
                      },
                      icon: const Icon(Icons.logout_rounded, size: 16),
                      label: const Text('Logout', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.redAccent,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
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
                          activeColor: ThalaivaaTheme.brandAmber,
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
                      return RadioListTile<Branch>(
                        value: b,
                        groupValue: selectedBranch,
                        title: Text(b.name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                        subtitle: Text('${b.address} • ${b.deliveryTime}', style: const TextStyle(fontSize: 11)),
                        activeColor: ThalaivaaTheme.brandAmber,
                        onChanged: (val) {
                          if (val != null) ref.read(selectedBranchProvider.notifier).state = val;
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
