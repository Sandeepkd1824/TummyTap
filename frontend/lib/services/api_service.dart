import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/product.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.1.7:8000/api/products/';

  static Future<List<Product>> fetchProducts() async {
    final response = await http.get(Uri.parse(baseUrl));
    print('Status Code: ${response.statusCode}');
    print('Body: ${response.body}');

    if (response.statusCode == 200) {
      List data = json.decode(response.body);
      return data.map((item) => Product.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load products');
    }
  }
}
