import 'package:flutter/material.dart';

class UserProvider with ChangeNotifier {
  String? _token;
  String? _email;

  String? get token => _token;
  String? get email => _email;

  bool get isLoggedIn => _token != null;

  void login(String token, String email) {
    _token = token;
    _email = email;
    notifyListeners();
  }

  void logout() {
    _token = null;
    _email = null;
    notifyListeners();
  }
}
