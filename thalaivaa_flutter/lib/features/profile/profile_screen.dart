import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/theme.dart';
import '../../models/models.dart';
import '../../providers/app_providers.dart';
import '../order/past_orders_screen.dart';

class ProfileScreen extends ConsumerStatefulWidget {
  const ProfileScreen({super.key});

  @override
  ConsumerState<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends ConsumerState<ProfileScreen> {
  final _emailPhoneController = TextEditingController(text: 'usera@test.com');
  final _passwordController = TextEditingController(text: 'Password123!');
  final _otpPhoneController = TextEditingController(text: '+919800000001');
  final _otpCodeController = TextEditingController(text: '123456');

  bool _isLoggingIn = false;
  String? _loginError;

  @override
  void dispose() {
    _emailPhoneController.dispose();
    _passwordController.dispose();
    _otpPhoneController.dispose();
    _otpCodeController.dispose();
    super.dispose();
  }

  Future<void> _performPasswordLogin(String emailOrPhone, String password) async {
    setState(() {
      _isLoggingIn = true;
      _loginError = null;
    });

    final res = await ref.read(authProvider.notifier).login(emailOrPhone, password);

    if (mounted) {
      setState(() {
        _isLoggingIn = false;
        if (res['success'] != true) {
          _loginError = res['message'] ?? 'Authentication failed.';
        }
      });

      if (res['success'] == true) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('✅ Welcome, ${(res['user'] as UserModel).name}! Logged in successfully.'),
            backgroundColor: Colors.green,
          ),
        );
      }
    }
  }

  Future<void> _performOtpVerify() async {
    setState(() {
      _isLoggingIn = true;
      _loginError = null;
    });

    final res = await ref.read(authProvider.notifier).verifyOtp(
      _otpPhoneController.text.trim(),
      _otpCodeController.text.trim(),
    );

    if (mounted) {
      setState(() {
        _isLoggingIn = false;
        if (res['success'] != true) {
          _loginError = res['message'] ?? 'OTP verification failed.';
        }
      });

      if (res['success'] == true) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('✅ Welcome, ${(res['user'] as UserModel).name}! OTP verified.'),
            backgroundColor: Colors.green,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(authProvider);
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
              // 1. Authenticated User Profile & Session Card (ONLY IF LOGGED IN)
              if (user != null) ...[
                Material(
                  color: cardBg,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                    side: BorderSide(color: cardBorder),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            CircleAvatar(
                              radius: 28,
                              backgroundColor: ThalaivaaTheme.brandAmber,
                              child: Text(
                                user.name.isNotEmpty ? user.name[0].toUpperCase() : 'U',
                                style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
                              ),
                            ),
                            const SizedBox(width: 14),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    user.name,
                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                                  ),
                                  const SizedBox(height: 3),
                                  Text(
                                    user.email.isNotEmpty ? user.email : user.phone,
                                    style: TextStyle(color: isDark ? Colors.white70 : Colors.black54, fontSize: 13),
                                  ),
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
                              child: const Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Icon(Icons.check_circle_rounded, color: Colors.green, size: 12),
                                  SizedBox(width: 4),
                                  Text('Signed In', style: TextStyle(color: Colors.green, fontSize: 11, fontWeight: FontWeight.bold)),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        const Divider(),
                        const SizedBox(height: 12),
                        Row(
                          children: [
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text('Phone Number', style: TextStyle(fontSize: 11, color: Colors.grey)),
                                  const SizedBox(height: 2),
                                  Text(user.phone.isNotEmpty ? user.phone : 'Not provided', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                                ],
                              ),
                            ),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text('Account ID', style: TextStyle(fontSize: 11, color: Colors.grey)),
                                  const SizedBox(height: 2),
                                  Text(
                                    user.id.length > 12 ? '${user.id.substring(0, 12)}...' : user.id,
                                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 12, fontFamily: 'monospace'),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        SizedBox(
                          width: double.infinity,
                          child: OutlinedButton.icon(
                            onPressed: () async {
                              await ref.read(authProvider.notifier).logout();
                              if (context.mounted) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('🚪 Signed out successfully.')),
                                );
                              }
                            },
                            icon: const Icon(Icons.logout_rounded, size: 16, color: Colors.redAccent),
                            label: const Text('Sign Out / Switch Account', style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Colors.redAccent)),
                            style: OutlinedButton.styleFrom(
                              side: const BorderSide(color: Colors.redAccent),
                              padding: const EdgeInsets.symmetric(vertical: 12),
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // 2. My Past Orders Tile
                Material(
                  color: cardBg,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                    side: BorderSide(color: cardBorder),
                  ),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(16),
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(builder: (_) => const PastOrdersScreen()),
                      );
                    },
                    child: Padding(
                      padding: const EdgeInsets.all(18),
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: ThalaivaaTheme.brandAmber.withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: const Icon(Icons.receipt_long_rounded, color: ThalaivaaTheme.brandAmber, size: 24),
                          ),
                          const SizedBox(width: 14),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'My Past Orders',
                                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  'View complete order history, past meals & invoices',
                                  style: TextStyle(fontSize: 12, color: isDark ? Colors.white60 : Colors.black54),
                                ),
                              ],
                            ),
                          ),
                          const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Colors.grey),
                        ],
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
              ],

              // 2. Database Multi-User Authentication Card (ONLY IF NOT LOGGED IN)
              if (user == null) ...[
                Material(
                  color: cardBg,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                    side: BorderSide(color: cardBorder),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: const [
                            Icon(Icons.lock_outline_rounded, color: ThalaivaaTheme.brandAmber, size: 20),
                            SizedBox(width: 8),
                            Text('Sign In to Your Account', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                          ],
                        ),
                        const SizedBox(height: 6),
                        const Text('Choose an account to sign in with live database credentials:', style: TextStyle(fontSize: 11, color: Colors.grey)),
                        const SizedBox(height: 12),

                        // Quick Test User Selector Chips
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: [
                            _buildUserChip('User A (3 Orders)', 'usera@test.com', '+919800000001', 'Password123!', isDark),
                            _buildUserChip('User B (1 Order)', 'userb@test.com', '+919800000002', 'Password123!', isDark),
                            _buildUserChip('User C (0 Orders)', 'userc@test.com', '+919800000003', 'Password123!', isDark),
                            _buildUserChip('Default Customer', 'customer@thalaivaa.com', '+919217002598', 'Password123!', isDark),
                          ],
                        ),

                        if (_loginError != null) ...[
                          const SizedBox(height: 12),
                          Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.red.withValues(alpha: 0.12),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: Colors.redAccent),
                            ),
                            child: Row(
                              children: [
                                const Icon(Icons.error_outline_rounded, color: Colors.redAccent, size: 16),
                                const SizedBox(width: 8),
                                Expanded(child: Text(_loginError!, style: const TextStyle(color: Colors.redAccent, fontSize: 12))),
                              ],
                            ),
                          ),
                        ],

                        const SizedBox(height: 14),
                        const Divider(),
                        const SizedBox(height: 10),
                        const Text('Password Authentication (Database Validated)', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                        const SizedBox(height: 10),
                        TextField(
                          controller: _emailPhoneController,
                          style: const TextStyle(fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'Email or Phone Number',
                            labelStyle: const TextStyle(fontSize: 12),
                            prefixIcon: const Icon(Icons.email_outlined, size: 18),
                            contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                          ),
                        ),
                        const SizedBox(height: 10),
                        TextField(
                          controller: _passwordController,
                          obscureText: true,
                          style: const TextStyle(fontSize: 13),
                          decoration: InputDecoration(
                            labelText: 'Password',
                            labelStyle: const TextStyle(fontSize: 12),
                            prefixIcon: const Icon(Icons.lock_outline_rounded, size: 18),
                            contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                          ),
                        ),
                        const SizedBox(height: 12),
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton.icon(
                            onPressed: _isLoggingIn
                                ? null
                                : () => _performPasswordLogin(
                                      _emailPhoneController.text.trim(),
                                      _passwordController.text,
                                    ),
                            icon: _isLoggingIn
                                ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                                : const Icon(Icons.login_rounded, size: 16),
                            label: Text(_isLoggingIn ? 'Authenticating...' : 'Sign In with Database Credentials', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: ThalaivaaTheme.brandAmber,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(vertical: 12),
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                            ),
                          ),
                        ),

                        const SizedBox(height: 14),
                        const Divider(),
                        const SizedBox(height: 10),
                        const Text('Alternative: Mobile OTP Authentication', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                        const SizedBox(height: 10),
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: _otpPhoneController,
                                style: const TextStyle(fontSize: 12),
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
                              onPressed: () {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('📱 OTP Code generated: 123456 (Auto-filled)')),
                                );
                                _otpCodeController.text = '123456';
                              },
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
                                controller: _otpCodeController,
                                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, letterSpacing: 2),
                                decoration: InputDecoration(
                                  labelText: '6-Digit OTP',
                                  labelStyle: const TextStyle(fontSize: 11),
                                  prefixIcon: const Icon(Icons.lock_clock_rounded, size: 16),
                                  contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                ),
                              ),
                            ),
                            const SizedBox(width: 8),
                            ElevatedButton.icon(
                              onPressed: _isLoggingIn ? null : _performOtpVerify,
                              icon: const Icon(Icons.verified_user_rounded, size: 14),
                              label: const Text('Verify OTP', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
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
                ),
                const SizedBox(height: 16),
              ],

              // 4. Theme Settings (Dark / Light)
              Material(
                color: cardBg,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(color: cardBorder),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16),
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
              ),

              const SizedBox(height: 16),

              // 5. Language Selector (i18n)
              Material(
                color: cardBg,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(color: cardBorder),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16),
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
                        runSpacing: 8,
                        children: [
                          {'code': 'en', 'label': 'English'},
                          {'code': 'hi', 'label': 'हिन्दी (Hindi)'},
                          {'code': 'gu', 'label': 'ગુજરાતી (Gujarati)'},
                          {'code': 'ta', 'label': 'தமிழ் (Tamil)'},
                        ].map((item) {
                          final isSel = language == item['code'];
                          return InkWell(
                            borderRadius: BorderRadius.circular(20),
                            onTap: () => ref.read(languageProvider.notifier).state = item['code']!,
                            child: Container(
                              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                              decoration: BoxDecoration(
                                color: isSel ? ThalaivaaTheme.brandAmber.withValues(alpha: 0.15) : (isDark ? Colors.white10 : const Color(0xFFF1F5F9)),
                                borderRadius: BorderRadius.circular(20),
                                border: Border.all(
                                  color: isSel ? ThalaivaaTheme.brandAmber : (isDark ? Colors.white24 : const Color(0xFFCBD5E1)),
                                ),
                              ),
                              child: Text(
                                item['label']!,
                                style: TextStyle(
                                  fontSize: 12,
                                  fontWeight: isSel ? FontWeight.bold : FontWeight.normal,
                                  color: isSel ? ThalaivaaTheme.brandAmber : (isDark ? Colors.white : Colors.black87),
                                ),
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 16),

              // 6. Branch Selector
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
                    const SizedBox(height: 12),
                    ...branches.map((b) {
                      final isSel = selectedBranch.id == b.id;
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 8),
                        child: InkWell(
                          borderRadius: BorderRadius.circular(10),
                          onTap: () => ref.read(selectedBranchProvider.notifier).state = b,
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                            decoration: BoxDecoration(
                              color: isSel
                                  ? ThalaivaaTheme.brandAmber.withValues(alpha: 0.1)
                                  : (isDark ? Colors.white.withValues(alpha: 0.03) : const Color(0xFFF8FAFC)),
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(
                                color: isSel ? ThalaivaaTheme.brandAmber : (isDark ? Colors.white10 : const Color(0xFFE2E8F0)),
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  isSel ? Icons.radio_button_checked_rounded : Icons.radio_button_off_rounded,
                                  color: isSel ? ThalaivaaTheme.brandAmber : Colors.grey,
                                  size: 18,
                                ),
                                const SizedBox(width: 10),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        b.name,
                                        style: TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 13,
                                          color: isSel ? ThalaivaaTheme.brandAmber : (isDark ? Colors.white : Colors.black87),
                                        ),
                                      ),
                                      const SizedBox(height: 2),
                                      Text(
                                        '${b.address} • ${b.deliveryTime}',
                                        style: TextStyle(fontSize: 11, color: isDark ? Colors.white60 : Colors.black54),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    }),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildUserChip(String label, String email, String phone, String password, bool isDark) {
    return InkWell(
      borderRadius: BorderRadius.circular(20),
      onTap: () {
        _emailPhoneController.text = email;
        _passwordController.text = password;
        _otpPhoneController.text = phone;
        _performPasswordLogin(email, password);
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: isDark ? Colors.white10 : const Color(0xFFF1F5F9),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: isDark ? Colors.white24 : const Color(0xFFCBD5E1)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.account_circle, size: 16, color: ThalaivaaTheme.brandAmber),
            const SizedBox(width: 6),
            Text(label, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}
