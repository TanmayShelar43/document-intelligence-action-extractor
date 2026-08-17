import 'package:dio/dio.dart';
import '../../../core/network/api_client.dart';

class DocumentApiService {
  static Future<Response> uploadDocument(String filePath, String fileName) async {
    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(
        filePath,
        filename: fileName,
      ),
    });

    return await ApiClient.dio.post(
      '/documents/upload',
      data: formData,
    );
  }

  static Future<Response> fetchDocuments() async {
    return await ApiClient.dio.get('/documents');
  }

  static Future<Response> fetchDocumentDetails(String documentId) async {
    return await ApiClient.dio.get('/documents/$documentId');
  }
}