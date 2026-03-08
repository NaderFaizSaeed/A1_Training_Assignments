import 'package:flutter/material.dart';
import '../models/user_model.dart';
import 'projects_screen.dart';

class DashboardScreen extends StatelessWidget {
  final User user;

  DashboardScreen({required this.user});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Dashboard")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("Welcome, ${user.name}", style: TextStyle(fontSize: 22)),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => ProjectsScreen()),
                );
              },
              child: Text("View Projects"),
            ),
          ],
        ),
      ),
    );
  }
}