import 'package:dio/dio.dart';
import '../../../models/document_model.dart';
import '../services/document_api_service.dart';
import '../../../core/network/api_exception.dart';

class DocumentRepository {
  final bool useMockData;

  DocumentRepository({this.useMockData = false});

  Future<List<DocumentModel>> getDocuments() async {
    if (useMockData) {
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
      ];
    }

    try {
      final response = await DocumentApiService.fetchDocuments();
      final List rawList = response.data['documents'] ?? [];
      return rawList.map((json) => DocumentModel(
        id: json['id'],
        name: json['filename'],
        uploadDate: DateTime.parse(json['created_at']),
        fileType: json['file_type'].toString().toUpperCase(),
        status: DocumentStatus.values.byName(json['status']),
        riskLevel: RiskLevel.values.byName(json['risk_level']),
        actionCount: json['action_count'] ?? 0,
      )).toList();
    } on DioException catch (e) {
      throw ApiException.fromDioError(e);
    }
  }
}