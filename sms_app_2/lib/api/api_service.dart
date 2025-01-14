import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://localhost:3000";

  static Future<String> register(String username, String email, String password) async {
    final response = await http.post(
      Uri.parse("$baseUrl/register"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "username": username,
        "email": email,
        "password": password,
      }),
    );

    if (response.statusCode == 201) {
      return "User registered successfully.";
    } else {
      return "Error: ${response.body}";
    }
  }

  static Future<String> login(String email, String password) async {
    final response = await http.post(
      Uri.parse("$baseUrl/login"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "email": email,
        "password": password,
      }),
    );

    if (response.statusCode == 200) {
      return "Login successful.";
    } else {
      return "Error: ${response.body}";
    }
  }
}