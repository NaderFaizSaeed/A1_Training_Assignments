import 'package:flutter/material.dart';
import '../models/project_model.dart';

class ProjectDetailsScreen extends StatelessWidget {
  final Project project;

  ProjectDetailsScreen({required this.project});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(project.title)),
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Project ID: ${project.id}", style: TextStyle(fontSize: 18)),
            SizedBox(height: 10),
            Text("Description:", style: TextStyle(fontSize: 18)),
            Text(project.description),
          ],
        ),
      ),
    );
  }
}