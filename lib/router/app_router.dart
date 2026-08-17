import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../features/auth/screens/login_screen.dart';
import '../features/home/screens/home_screen.dart';
import '../features/documents/screens/documents_screen.dart';
import '../features/tasks/screens/tasks_screen.dart';
import '../features/profile/screens/profile_screen.dart';
import '../features/analysis/screens/analysis_screen.dart';

final GlobalKey<NavigatorState> _rootNavigatorKey = GlobalKey<NavigatorState>();

final appRouter = GoRouter(
  navigatorKey: _rootNavigatorKey,
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/analysis/:id',
      builder: (context, state) {
        final id = state.pathParameters['id'] ?? 'doc_1';
        return AnalysisScreen(documentId: id);
      },
    ),
    ShellRoute(
      builder: (context, state, child) {
        return Scaffold(
          body: child,
          bottomNavigationBar: BottomNavigationBar(
            currentIndex: _calculateSelectedIndex(state.uri.toString()),
            onTap: (index) {
              switch (index) {
                case 0: context.go('/home'); break;
                case 1: context.go('/documents'); break;
                case 2: context.go('/tasks'); break;
                case 3: context.go('/profile'); break;
              }
            },
            items: const [
              BottomNavigationBarItem(icon: Icon(Icons.dashboard_rounded), label: 'Home'),
              BottomNavigationBarItem(icon: Icon(Icons.folder_copy_rounded), label: 'Docs'),
              BottomNavigationBarItem(icon: Icon(Icons.task_alt_rounded), label: 'Tasks'),
              BottomNavigationBarItem(icon: Icon(Icons.person_rounded), label: 'Profile'),
            ],
          ),
        );
      },
      routes: [
        GoRoute(path: '/home', builder: (context, state) => const HomeScreen()),
        GoRoute(path: '/documents', builder: (context, state) => const DocumentsScreen()),
        GoRoute(path: '/tasks', builder: (context, state) => const TasksScreen()),
        GoRoute(path: '/profile', builder: (context, state) => const ProfileScreen()),
      ],
    ),
  ],
);

int _calculateSelectedIndex(String location) {
  if (location.startsWith('/documents')) return 1;
  if (location.startsWith('/tasks')) return 2;
  if (location.startsWith('/profile')) return 3;
  return 0;
}