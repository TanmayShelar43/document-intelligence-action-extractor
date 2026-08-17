import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/widgets/document_card.dart';
import '../../upload/screens/upload_modal.dart';
import '../providers/document_provider.dart';

class DocumentsScreen extends ConsumerWidget {
  const DocumentsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final documents = ref.watch(documentProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Documents', style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: AppColors.background,
        elevation: 0,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Column(
            children: [
              TextField(
                style: const TextStyle(color: AppColors.textPrimary),
                decoration: InputDecoration(
                  hintText: 'Search documents...',
                  hintStyle: const TextStyle(color: AppColors.textMuted),
                  prefixIcon: const Icon(Icons.search, color: AppColors.textMuted),
                  filled: true,
                  fillColor: AppColors.surfaceCard,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: AppColors.borderStroke),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: documents.isEmpty
                    ? const Center(
                        child: Text('No documents uploaded yet', style: TextStyle(color: AppColors.textMuted)),
                      )
                    : ListView.builder(
                        itemCount: documents.length,
                        itemBuilder: (context, index) {
                          return DocumentCard(
                            document: documents[index],
                            onTap: () {
                              context.push('/analysis/${documents[index].id}');
                            },
                          );
                        },
                      ),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            backgroundColor: Colors.transparent,
            builder: (context) => const UploadModal(),
          );
        },
        icon: const Icon(Icons.add),
        label: const Text('Analyze Doc', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
    );
  }
}