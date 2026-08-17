import 'package:flutter/material.dart';
import '../../models/document_model.dart';
import '../theme/app_theme.dart';

class DocumentCard extends StatelessWidget {
  final DocumentModel document;
  final VoidCallback onTap;

  const DocumentCard({
    super.key,
    required this.document,
    required this.onTap,
  });

  Color _getRiskColor(RiskLevel risk) {
    switch (risk) {
      case RiskLevel.high: return AppColors.error;
      case RiskLevel.medium: return AppColors.warning;
      case RiskLevel.low: return AppColors.success;
    }
  }

  Widget _buildStatusChip(DocumentStatus status) {
    String text;
    Color color;

    switch (status) {
      case DocumentStatus.completed:
        text = 'Verified';
        color = AppColors.success;
        break;
      case DocumentStatus.needsVerification:
        text = 'Needs Review';
        color = AppColors.warning;
        break;
      case DocumentStatus.processing:
        text = 'Analyzing...';
        color = AppColors.secondaryAccent;
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withValues(alpha: 0.5)),
      ),
      child: Text(
        text,
        style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.bold),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: AppColors.primaryAccent.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.description_rounded, color: AppColors.secondaryAccent),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          document.name,
                          style: const TextStyle(
                            color: AppColors.textPrimary,
                            fontWeight: FontWeight.bold,
                            fontSize: 15,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          '${document.fileType} • ${document.uploadDate.day}/${document.uploadDate.month}/${document.uploadDate.year}',
                          style: const TextStyle(color: AppColors.textMuted, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                  _buildStatusChip(document.status),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Icon(Icons.shield_outlined, size: 16, color: _getRiskColor(document.riskLevel)),
                      const SizedBox(width: 4),
                      Text(
                        '${document.riskLevel.name.toUpperCase()} RISK',
                        style: TextStyle(
                          color: _getRiskColor(document.riskLevel),
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                  Row(
                    children: [
                      const Icon(Icons.task_alt_rounded, size: 16, color: AppColors.textMuted),
                      const SizedBox(width: 4),
                      Text(
                        '${document.actionCount} Actions',
                        style: const TextStyle(color: AppColors.textMuted, fontSize: 12),
                      ),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}