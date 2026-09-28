import 'package:flutter/material.dart';

class ThalaivaaTheme {
  // Brand Color Tokens
  static const primaryOrange = Color(0xFFFF6B00);
  static const brandAmber = Color(0xFFFF6B00);
  static const primaryDeep = Color(0xFFE05D00);
  static const primaryLight = Color(0xFFFFF3EB);
  static const darkSlate = Color(0xFF181824);
  static const obsidianBg = Color(0xFF10141D);
  static const darkCard = Color(0xFF1A2230);
  static const surfaceCard = Color(0xFF1E2838);
  static const accentGold = Color(0xFFFFB800);
  static const goldAccent = Color(0xFFFFB800);
  static const goldLight = Color(0xFFFFF8E7);
  static const vegGreen = Color(0xFF00A86B);
  static const vegLight = Color(0xFFE8F8F2);
  static const nonVegRed = Color(0xFFE63946);
  static const spiceRed = Color(0xFFE63946);
  static const nonVegLight = Color(0xFFFFECEE);
  static const bgLight = Color(0xFFF7F8FA);
  static const surfaceWhite = Colors.white;
  static const textMain = Color(0xFF1A1A1A);
  static const textMuted = Color(0xFF757575);
  static const textMutedLight = Color(0xFF757575);
  static const borderLight = Color(0xFFE5E7EB);
  static const borderDark = Color(0xFF2D3748);

  static String formatInr(num amount) {
    final rounded = amount.round();
    final str = rounded.abs().toString();
    if (str.length <= 3) {
      return (amount < 0 ? '-\u20B9' : '\u20B9') + str;
    }
    final last3 = str.substring(str.length - 3);
    final rest = str.substring(0, str.length - 3);
    final buffer = StringBuffer();
    for (int i = 0; i < rest.length; i++) {
      if (i > 0 && (rest.length - i) % 2 == 0) {
        buffer.write(',');
      }
      buffer.write(rest[i]);
    }
    buffer.write(',');
    buffer.write(last3);
    return (amount < 0 ? '-\u20B9' : '\u20B9') + buffer.toString();
  }

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.fromSeed(
        seedColor: brandAmber,
        primary: brandAmber,
        secondary: const Color(0xFF0F172A),
        surface: surfaceWhite,
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: const Color(0xFFF8FAFC),
      appBarTheme: const AppBarTheme(
        backgroundColor: surfaceWhite,
        foregroundColor: Color(0xFF0F172A),
        elevation: 0,
        centerTitle: false,
      ),
      cardTheme: CardThemeData(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: borderLight, width: 1),
        ),
        color: surfaceWhite,
      ),
      chipTheme: ChipThemeData(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        side: const BorderSide(color: borderLight),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: surfaceWhite,
        indicatorColor: brandAmber.withValues(alpha: 0.15),
        labelTextStyle: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return const TextStyle(color: brandAmber, fontWeight: FontWeight.bold, fontSize: 12);
          }
          return const TextStyle(color: Color(0xFF64748B), fontSize: 12);
        }),
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: ColorScheme.fromSeed(
        seedColor: brandAmber,
        primary: brandAmber,
        secondary: goldAccent,
        surface: surfaceCard,
        brightness: Brightness.dark,
      ),
      scaffoldBackgroundColor: obsidianBg,
      appBarTheme: const AppBarTheme(
        backgroundColor: obsidianBg,
        foregroundColor: Colors.white,
        elevation: 0,
        centerTitle: false,
      ),
      cardTheme: CardThemeData(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: borderDark, width: 1),
        ),
        color: surfaceCard,
      ),
      chipTheme: ChipThemeData(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        side: const BorderSide(color: borderDark),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: darkCard,
        indicatorColor: brandAmber.withValues(alpha: 0.25),
        labelTextStyle: WidgetStateProperty.resolveWith((states) {
          if (states.contains(WidgetState.selected)) {
            return const TextStyle(color: brandAmber, fontWeight: FontWeight.bold, fontSize: 12);
          }
          return const TextStyle(color: Colors.white60, fontSize: 12);
        }),
      ),
    );
  }
}
