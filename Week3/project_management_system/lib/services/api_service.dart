import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user_model.dart';
import '../models/project_model.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.8.161:8000';
  static Future<User?> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/users/login'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"email": email, "password": password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        // البيانات حسب ما يرجعها الباك اند
        return User(
          id: data['id'],
          name: data['name'],
          email: data['email'],
          role: data['role'],
        );
      } else {
        print("Login failed: ${response.body}");
        return null;
      }
    } catch (e) {
      print("Login error: $e");
      return null;
    }
  }

  /// جلب المشاريع
  static Future<List<Project>> getProjects() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/projects'));
      if (response.statusCode == 200) {
        List data = jsonDecode(response.body);
        return data.map((json) => Project.fromJson(json)).toList();
      } else {
        print("Fetch projects failed: ${response.body}");
        return [];
      }
    } catch (e) {
      print("Fetch projects error: $e");
      return [];
    }
  }

  /// جلب تفاصيل مشروع واحد
  static Future<Project?> getProject(int id) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/projects/$id'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return Project.fromJson(data);
      } else {
        print("Fetch project failed: ${response.body}");
        return null;
      }
    } catch (e) {
      print("Fetch project error: $e");
      return null;
    }
  }
}