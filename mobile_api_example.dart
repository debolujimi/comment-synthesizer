import 'dart:convert';
import 'package:http/http.dart' as http;

Future<String> getResponse(String message) async {
  final uri = Uri.parse('http://127.0.0.1:8000/respond');
  final response = await http.post(
    uri,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'message': message}),
  );

  if (response.statusCode != 200) {
    throw Exception('Request failed: ${response.statusCode}');
  }

  final data = jsonDecode(response.body);
  return data['response'] as String;
}

Future<void> main() async {
  try {
    final result = await getResponse('there is load shedding in my area');
    print(result);
  } catch (e) {
    print('Error: $e');
  }
}
