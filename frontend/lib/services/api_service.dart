import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/product.dart';
import '../models/category.dart';
import '../models/order.dart';
import '../models/cart_item.dart';
import '../models/user.dart';

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000/api'; // adjust if backend is deployed

  static Future<List<Product>> fetchProducts({int? categoryId}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/products/${categoryId != null ? '?category=$categoryId' : ''}'),
    );

    if (response.statusCode == 200) {
      final List data = json.decode(response.body);
      return data.map((e) => Product.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load products');
    }
  }

  static Future<List<Category>> fetchCategories() async {
    final response = await http.get(Uri.parse('$baseUrl/categories/'));

    if (response.statusCode == 200) {
      final List data = json.decode(response.body);
      return data.map((e) => Category.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load categories');
    }
  }

  static Future<List<Order>> fetchOrders() async {
    final response = await http.get(Uri.parse('$baseUrl/orders/'));

    if (response.statusCode == 200) {
      final List data = json.decode(response.body);
      return data.map((e) => Order.fromJson(e)).toList();
    } else {
      throw Exception('Failed to load orders');
    }
  }

  static Future<bool> placeOrder(List<CartItem> cartItems, double totalPrice) async {
    final response = await http.post(
      Uri.parse('$baseUrl/place-order/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'items': cartItems
            .map((item) => {'product_id': item.product.id, 'quantity': item.quantity})
            .toList(),
        'total_price': totalPrice,
        'address_id': 1, // TODO: Replace with selected address ID
      }),
    );

    return response.statusCode == 201;
  }

  static Future<UserProfile?> fetchUserProfile() async {
    final response = await http.get(Uri.parse('$baseUrl/profile/'));

    if (response.statusCode == 200) {
      return UserProfile.fromJson(json.decode(response.body));
    }
    return null;
  }
}
