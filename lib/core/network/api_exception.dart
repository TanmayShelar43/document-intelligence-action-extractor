import 'package:dio/dio.dart';

class ApiException implements Exception {
  final String message;
  final int? statusCode;

  ApiException(this.message, {this.statusCode});

  factory ApiException.fromDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return ApiException('Connection timeout. Please check your internet connection.');
      case DioExceptionType.badResponse:
        final status = error.response?.statusCode;
        final msg = error.response?.data?['detail'] ?? 'An error occurred ($status).';
        return ApiException(msg, statusCode: status);
      case DioExceptionType.connectionError:
        return ApiException('Unable to reach backend server. Verify server is running.');
      default:
        return ApiException('An unexpected network error occurred.');
    }
  }

  @override
  String toString() => message;
}