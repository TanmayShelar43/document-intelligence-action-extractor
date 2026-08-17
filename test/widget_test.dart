import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:document_intelligenece_action/main.dart';

void main() {
  testWidgets('App initializes and displays Login Screen', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: DocumentIntelligenceApp(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Document Intelligence'), findsOneWidget);
    expect(find.text('Sign In'), findsOneWidget);
  });
}