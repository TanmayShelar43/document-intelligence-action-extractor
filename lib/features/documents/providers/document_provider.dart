import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../models/document_model.dart';

class DocumentNotifier extends Notifier<List<DocumentModel>> {
  @override
  List<DocumentModel> build() {
    return [
      DocumentModel(
        id: 'doc_1',
        name: 'Vendor_Agreement_2026.pdf',
        uploadDate: DateTime.now().subtract(const Duration(hours: 3)),
        fileType: 'PDF',
        status: DocumentStatus.completed,
        riskLevel: RiskLevel.low,
        actionCount: 4,
      ),
      DocumentModel(
        id: 'doc_2',
        name: 'Q3_Tax_Notice_Urgent.pdf',
        uploadDate: DateTime.now().subtract(const Duration(days: 1)),
        fileType: 'PDF',
        status: DocumentStatus.needsVerification,
        riskLevel: RiskLevel.high,
        actionCount: 2,
      ),
      DocumentModel(
        id: 'doc_3',
        name: 'Equipment_Lease_Contract.docx',
        uploadDate: DateTime.now().subtract(const Duration(days: 2)),
        fileType: 'DOCX',
        status: DocumentStatus.processing,
        riskLevel: RiskLevel.medium,
        actionCount: 0,
      ),
    ];
  }

  void addDocument(String name, String fileType) {
    final newDoc = DocumentModel(
      id: 'doc_${DateTime.now().millisecondsSinceEpoch}',
      name: name,
      uploadDate: DateTime.now(),
      fileType: fileType.toUpperCase(),
      status: DocumentStatus.processing,
      riskLevel: RiskLevel.medium,
      actionCount: 0,
    );
    state = [newDoc, ...state];
  }
}

final documentProvider = NotifierProvider<DocumentNotifier, List<DocumentModel>>(DocumentNotifier.new);