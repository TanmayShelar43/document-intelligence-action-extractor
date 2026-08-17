import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';

import '../../../core/theme/app_theme.dart';
import '../../documents/providers/document_provider.dart';

class UploadModal extends ConsumerWidget {
  const UploadModal({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      padding: const EdgeInsets.all(24.0),
      decoration: const BoxDecoration(
        color: AppColors.surfacePrimary,
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(24),
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Upload Document',
                style: TextStyle(
                  color: AppColors.textPrimary,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              IconButton(
                icon: const Icon(
                  Icons.close,
                  color: AppColors.textMuted,
                ),
                onPressed: () {
                  Navigator.pop(context);
                },
              ),
            ],
          ),

          const SizedBox(height: 20),

          GestureDetector(
            onTap: () async {
              final result = await FilePicker.pickFiles(
                type: FileType.custom,
                allowedExtensions: [
                  'pdf',
                  'docx',
                  'png',
                  'jpg',
                ],
              );

              if (result.isNotEmpty) {
                final file = result.first;

                // Extract extension from file name
                final fileName = file.name;
                final dotIndex = fileName.lastIndexOf('.');

                final extension = dotIndex != -1
                    ? fileName.substring(dotIndex + 1).toUpperCase()
                    : 'PDF';

                // Add document
                ref.read(documentProvider.notifier).addDocument(
                      fileName,
                      extension,
                    );

                // Close modal
                if (context.mounted) {
                  Navigator.pop(context);
                }
              }
            },
            child: Container(
              height: 160,
              decoration: BoxDecoration(
                color: AppColors.surfaceCard,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: AppColors.borderStroke,
                  width: 1.5,
                ),
              ),
              child: const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.cloud_upload_outlined,
                    size: 48,
                    color: AppColors.primaryAccent,
                  ),

                  SizedBox(height: 12),

                  Text(
                    'Tap to select file',
                    style: TextStyle(
                      color: AppColors.textPrimary,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  SizedBox(height: 4),

                  Text(
                    'Supports PDF, DOCX, PNG, JPG',
                    style: TextStyle(
                      color: AppColors.textMuted,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: 24),
        ],
      ),
    );
  }
}