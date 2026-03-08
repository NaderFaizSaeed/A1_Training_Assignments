import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/project_model.dart';
import '../widgets/project_card.dart';
import 'project_details_screen.dart';

class ProjectsScreen extends StatefulWidget {
  @override
  _ProjectsScreenState createState() => _ProjectsScreenState();
}

class _ProjectsScreenState extends State<ProjectsScreen> {
  List<Project> projects = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchProjects();
  }

  fetchProjects() async {
    var data = await ApiService.getProjects();
    setState(() {
      projects = data;
      loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Projects")),
      body: loading
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
        itemCount: projects.length,
        itemBuilder: (context, index) {
          return ProjectCard(
            project: projects[index],
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => ProjectDetailsScreen(project: projects[index]),
                ),
              );
            },
          );
        },
      ),
    );
  }
}