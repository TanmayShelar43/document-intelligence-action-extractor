import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_theme.dart';
import '../../auth/providers/auth_provider.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('User Profile', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: AppColors.background,
        elevation: 0,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              const CircleAvatar(
                radius: 40,
                backgroundColor: AppColors.primaryAccent,
                child: Icon(Icons.person, size: 48, color: Colors.white),
              ),
              const SizedBox(height: 16),
              const Text(
                'Developer Account',
                style: TextStyle(color: AppColors.textPrimary, fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              const Text(
                'admin@docintelligence.ai',
                style: TextStyle(color: AppColors.textMuted, fontSize: 14),
              ),
              const SizedBox(height: 32),
              Card(
                child: Column(
                  children: [
                    const ListTile(
                      leading: Icon(Icons.security, color: AppColors.secondaryAccent),
                      title: Text('API Configuration', style: TextStyle(color: AppColors.textPrimary)),
                      subtitle: Text('FastAPI Endpoint: http://127.0.0.1:8000', style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                      trailing: Icon(Icons.chevron_right, color: AppColors.textMuted),
                    ),
                    const Divider(height: 1, color: AppColors.borderStroke),
                    const ListTile(
                      leading: Icon(Icons.palette_outlined, color: AppColors.secondaryAccent),
                      title: Text('App Theme', style: TextStyle(color: AppColors.textPrimary)),
                      subtitle: Text('Dark Futuristic (Active)', style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                      trailing: Icon(Icons.chevron_right, color: AppColors.textMuted),
                    ),
                  ],
                ),
              ),
              const Spacer(),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.error.withValues(alpha: 0.15),
                    side: const BorderSide(color: AppColors.error),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: () async {
                    await ref.read(authProvider.notifier).logout();
                    if (context.mounted) {
                      context.go('/login');
                    }
                  },
                  icon: const Icon(Icons.logout, color: AppColors.error),
                  label: const Text(
                    'Sign Out',
                    style: TextStyle(color: AppColors.error, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}