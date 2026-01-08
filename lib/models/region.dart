class Region {
  final String id;
  final String name;
  final String display;

  Region({
    required this.id,
    required this.name,
    required this.display,
  });

  factory Region.fromJson(Map<String, dynamic> json) {
    return Region(
      id: json['id'] as String,
      name: json['name'] as String,
      display: json['display'] as String,
    );
  }
}
