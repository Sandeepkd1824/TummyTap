import 'package:flutter/material.dart';
import '../models/product.dart';

class CartItem {
  final Product product;
  int quantity;

  CartItem({required this.product, required this.quantity});
}

class CartProvider with ChangeNotifier {
  // Map of product ID to CartItem
  final Map<int, CartItem> _items = {};

  Map<int, CartItem> get items => _items;

  // Total number of different products in the cart
  int get itemCount => _items.length;

  // Total price of all items
  double get totalPrice {
    return _items.values.fold(
      0,
      (sum, item) => sum + double.parse(item.product.price) * item.quantity,
    );
  }

  // Add item to cart or increase quantity if already added
  void addToCart(Product product) {
    if (product.id == null) return;

    if (_items.containsKey(product.id)) {
      _items[product.id]!.quantity++;
    } else {
      _items[product.id!] = CartItem(product: product, quantity: 1);
    }
    notifyListeners();
  }

  // Remove item completely from cart
  void removeItem(int productId) {
    _items.remove(productId);
    notifyListeners();
  }

  // Increase quantity of an item
  void incrementQuantity(int productId) {
    if (_items.containsKey(productId)) {
      _items[productId]!.quantity++;
      notifyListeners();
    }
  }

  // Decrease quantity or remove item if quantity goes to 0
  void decrementQuantity(int productId) {
    if (_items.containsKey(productId)) {
      if (_items[productId]!.quantity > 1) {
        _items[productId]!.quantity--;
      } else {
        _items.remove(productId);
      }
      notifyListeners();
    }
  }

  // Clear all items in the cart
  void clearCart() {
    _items.clear();
    notifyListeners();
  }
}
