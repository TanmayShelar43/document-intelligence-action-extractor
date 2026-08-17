import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/storage/secure_storage_service.dart';

class AuthState {
  final bool isAuthenticated;
  final bool isLoading;
  final String? token;

  const AuthState({
    required this.isAuthenticated,
    this.isLoading = false,
    this.token,
  });
}

class AuthNotifier extends Notifier<AuthState> {
  @override
  AuthState build() {
    _checkInitialAuth();
    return const AuthState(isAuthenticated: false, isLoading: true);
  }

  Future<void> _checkInitialAuth() async {
    final token = await SecureStorageService.getToken();
    if (token != null && token.isNotEmpty) {
      state = AuthState(isAuthenticated: true, isLoading: false, token: token);
    } else {
      state = const AuthState(isAuthenticated: false, isLoading: false);
    }
  }

  Future<void> loginMock(String email, String password) async {
    state = const AuthState(isAuthenticated: false, isLoading: true);
    await Future.delayed(const Duration(seconds: 1)); // Simulated network latency
    const mockToken = 'mock_jwt_token_12345';
    await SecureStorageService.saveToken(mockToken);
    state = const AuthState(isAuthenticated: true, isLoading: false, token: mockToken);
  }

  Future<void> logout() async {
    await SecureStorageService.deleteToken();
    state = const AuthState(isAuthenticated: false, isLoading: false);
  }
}

final authProvider = NotifierProvider<AuthNotifier, AuthState>(AuthNotifier.new);