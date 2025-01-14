import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  String loginMessage = ''; // To display feedback to the user

  Future<void> login() async {
    final String email = emailController.text.trim();
    final String password = passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      setState(() {
        loginMessage = 'Please fill in all fields.';
      });
      return;
    }

    try {
      final response = await http.post(
        Uri.parse('http://10.0.2.2:3000/login'), // Use 'http://127.0.0.1:3000' for iOS
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      if (response.statusCode == 200) {
        setState(() {
          loginMessage = 'Login successful!';
        });

        // Navigate to the next screen (e.g., HomeScreen)
        // Navigator.push(context, MaterialPageRoute(builder: (context) => HomeScreen()));
      } else if (response.statusCode == 401) {
        setState(() {
          loginMessage = 'Invalid email or password.';
        });
      } else if (response.statusCode == 404) {
        setState(() {
          loginMessage = 'User not found.';
        });
      } else {
        setState(() {
          loginMessage = 'Something went wrong. Please try again.';
        });
      }
    } catch (e) {
      setState(() {
        loginMessage = 'Error: Unable to connect to the server.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: emailController,
              decoration: InputDecoration(labelText: 'Email'),
            ),
            TextField(
              controller: passwordController,
              decoration: InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: login,
              child: Text('Login'),
            ),
            SizedBox(height: 10),
            Text(
              loginMessage,
              style: TextStyle(color: Colors.red),
            ),
            TextButton(
              onPressed: () => Navigator.pushNamed(context, '/register'),
              child: Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}