import 'package:flutter/material.dart';

class AppColors {
  static const primaryColor = Color(0xFF00A86B);
  static const accentColor = Color(0xFFF9A825);
  static const backgroundColor = Color(0xFFF5F5F5);
  static const textColor = Color(0xFF333333);
  static const gray = Color(0xFF9E9E9E);
  static const white = Colors.white;
  static const errorColor = Color(0xFFB00020);
}

class AppTextStyles {
  static const heading = TextStyle(
    fontSize: 22,
    fontWeight: FontWeight.bold,
    color: AppColors.textColor,
  );

  static const subheading = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w500,
    color: AppColors.gray,
  );

  static const body = TextStyle(
    fontSize: 14,
    color: AppColors.textColor,
  );
}

class AppConstants {
  static const baseUrl = 'http://127.0.0.1:8000/api';
}
