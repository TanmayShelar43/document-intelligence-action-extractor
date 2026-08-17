enum DocumentStatus { processing, completed, needsVerification }
enum RiskLevel { low, medium, high }

class DocumentModel {
  final String id;
  final String name;
  final DateTime uploadDate;
  final String fileType;
  final DocumentStatus status;
  final RiskLevel riskLevel;
  final int actionCount;

  const DocumentModel({
    required this.id,
    required this.name,
    required this.uploadDate,
    required this.fileType,
    required this.status,
    required this.riskLevel,
    required this.actionCount,
  });
}