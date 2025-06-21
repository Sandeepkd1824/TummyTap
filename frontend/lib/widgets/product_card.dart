import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/product.dart';
import '../providers/cart_provider.dart';

class ProductCard extends StatelessWidget {
  final Product product;

  const ProductCard({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    final cart = Provider.of<CartProvider>(context, listen: false);

    return Card(
      elevation: 3,
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        contentPadding: const EdgeInsets.all(10),
        leading: Image.network(
          product.image,
          width: 60,
          height: 60,
          fit: BoxFit.cover,
        ),
        title: Text(product.name, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(product.description),
            Text('₹${product.price}', style: const TextStyle(color: Colors.green)),
            Text('Category: ${product.category.name}', style: const TextStyle(fontSize: 12)),
          ],
        ),
        trailing: ElevatedButton(
          onPressed: () {
            cart.addToCart(product);
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('${product.name} added to cart')),
            );
          },
          child: const Text('Add'),
        ),
      ),
    );
  }
}
