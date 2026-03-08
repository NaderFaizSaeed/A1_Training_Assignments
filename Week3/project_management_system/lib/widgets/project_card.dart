import 'package:flutter/material.dart';
import '../models/project_model.dart';

class ProjectCard extends StatelessWidget {
  final Project project;
  final VoidCallback onTap;

  ProjectCard({required this.project, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
      child: ListTile(
        title: Text(project.title),
        subtitle: Text(project.description),
        onTap: onTap,
      ),
    );
  }
}