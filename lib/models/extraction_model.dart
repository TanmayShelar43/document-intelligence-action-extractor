class ExtractedField {
  final String key;
  final String value;
  final double confidence; // Range 0.0 - 1.0

  const ExtractedField({
    required this.key,
    required this.value,
    required this.confidence,
  });
}

class ExtractionModel {
  final String documentId;
  final double overallConfidence;
  final List<ExtractedField> fields;
  final List<String> detectedRisks;

  const ExtractionModel({
    required this.documentId,
    required this.overallConfidence,
    required this.fields,
    required this.detectedRisks,
  });
}