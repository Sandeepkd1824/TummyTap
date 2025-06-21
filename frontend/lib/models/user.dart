class UserProfile {
  final int id;
  final String name;
  final String email;

  UserProfile({
    required this.id,
    required this.name,
    required this.email,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'],
      name: json['first_name'] ?? '',
      email: json['email'] ?? '',
    );
  }
}
