import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../models/extraction_model.dart';

final analysisProvider = Provider.family<ExtractionModel?, String>((ref, documentId) {
  return ExtractionModel(
    documentId: documentId,
    overallConfidence: 0.94,
    fields: const [
      ExtractedField(key: 'Vendor Name', value: 'Acme Enterprise Ltd.', confidence: 0.98),
      ExtractedField(key: 'Effective Date', value: 'October 15, 2026', confidence: 0.96),
      ExtractedField(key: 'Contract Value', value: '\$185,000.00 USD', confidence: 0.92),
      ExtractedField(key: 'Renewal Term', value: 'Auto-renews 30 days prior', confidence: 0.88),
    ],
    detectedRisks: const [
      'Automatic renewal without price cap lock.',
      'Indemnification clause weighted heavily toward vendor.',
    ],
  );
});