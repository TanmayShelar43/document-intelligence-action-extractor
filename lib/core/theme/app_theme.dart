import 'package:flutter/material.dart';

class AppColors {
  // Base Palette
  static const Color background = Color(0xFF0B0718);
  static const Color surfacePrimary = Color(0xFF17122B);
  static const Color surfaceCard = Color(0xFF211A3B);
  static const Color borderStroke = Color(0xFF371FA5);

  // Accents
  static const Color primaryAccent = Color(0xFF6C3BFF);
  static const Color secondaryAccent = Color(0xFF9B7BFF);

  // Text
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textMuted = Color(0xFFB7B0C9);

  // Semantic Status
  static const Color success = Color(0xFF57D39A); // High Confidence
  static const Color warning = Color(0xFFF4C95D); // Needs Verification
  static const Color error = Color(0xFFFF6B81);   // Risk / Priority
}

class AppTheme {
  static ThemeData get darkTheme {
    return ThemeData.dark().copyWith(
      scaffoldBackgroundColor: AppColors.background,
      primaryColor: AppColors.primaryAccent,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.primaryAccent,
        secondary: AppColors.secondaryAccent,
        surface: AppColors.surfaceCard,
        error: AppColors.error,
      ),
      cardTheme: CardThemeData(
        color: AppColors.surfaceCard,
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: const BorderSide(color: AppColors.borderStroke, width: 1),
        ),
      ),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: AppColors.primaryAccent,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
      bottomNavigationBarTheme: const BottomNavigationBarThemeData(
        backgroundColor: AppColors.surfacePrimary,
        selectedItemColor: AppColors.secondaryAccent,
        unselectedItemColor: AppColors.textMuted,
        type: BottomNavigationBarType.fixed,
      ),
    );
  }
}