class Product {
  final int id;
  final String name;
  final String description;
  final String image;
  final double price;
  final int categoryId;

  Product({
    required this.id,
    required this.name,
    required this.description,
    required this.image,
    required this.price,
    required this.categoryId,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      name: json['name'] ?? '',
      description: json['description'] ?? '',
      image: json['image'] ?? '',  // Make sure this matches backend key
      price: double.tryParse(json['price'].toString()) ?? 0.0,
      categoryId: json['category_id'] ?? 0,
    );
  }
}
