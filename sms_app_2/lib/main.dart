import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(ThemeToggleApp());
}

class ThemeToggleApp extends StatefulWidget {
  const ThemeToggleApp({super.key});

  @override
  State<ThemeToggleApp> createState() => _ThemeToggleAppState();
}

class _ThemeToggleAppState extends State<ThemeToggleApp> {
  ThemeMode _themeMode = ThemeMode.light;

  void _setTheme(ThemeMode mode) {
    setState(() {
      _themeMode = mode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
      themeMode: _themeMode,
      home: ThemeToggleWidget(
        themeMode: _themeMode,
        onThemeChange: _setTheme,
      ),
    );
  }
}

class ThemeToggleWidget extends StatelessWidget {
  final ThemeMode themeMode;
  final Function(ThemeMode) onThemeChange;

  const ThemeToggleWidget({
    super.key,
    required this.themeMode,
    required this.onThemeChange,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Theme Toggle Example')),
      body: Align(
        alignment: Alignment.bottomCenter,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                IconButton(
                  icon: const Icon(Icons.upload),
                  onPressed: () {
                    // Show Spam Detector Screen when SMS Threat is pressed
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => SpamDetectorScreen(),
                      ),
                    );
                  },
                ),
                const Text('SMS Threat'),
              ],
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                IconButton(
                  icon: const Icon(Icons.settings),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => SettingsPage(
                          currentTheme: themeMode,
                          onThemeChange: onThemeChange,
                        ),
                      ),
                    );
                  },
                ),
                const Text('Settings'),
              ],
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                IconButton(
                  icon: const Icon(Icons.person),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const LoginPage(),
                      ),
                    );
                  },
                ),
                const Text('Login'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class SpamDetectorScreen extends StatefulWidget {
  @override
  _SpamDetectorScreenState createState() => _SpamDetectorScreenState();
}

class _SpamDetectorScreenState extends State<SpamDetectorScreen> {
  final TextEditingController _controller = TextEditingController();
  String _result = "";

  Future<void> _detectSpam(String message) async {
    final url = Uri.parse('http://192.168.1.212:5001/predict'); // Replace <your_ip> with your backend's IP
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'message': message}),
    );

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      setState(() {
        _result = responseData['prediction'];
      });
    } else {
      setState(() {
        _result = "Error: Unable to classify the message.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Spam Detector'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                labelText: 'Enter a message',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                _detectSpam(_controller.text);
              },
              child: Text('Detect Spam'),
            ),
            SizedBox(height: 16),
            Text(
              'Result: $_result',
              style: TextStyle(fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}

class SettingsPage extends StatelessWidget {
  final ThemeMode currentTheme;
  final Function(ThemeMode) onThemeChange;

  const SettingsPage({
    super.key,
    required this.currentTheme,
    required this.onThemeChange,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Theme',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            ListTile(
              title: const Text('Light Mode'),
              leading: Radio<ThemeMode>(
                value: ThemeMode.light,
                groupValue: currentTheme,
                onChanged: (ThemeMode? value) {
                  if (value != null) {
                    onThemeChange(value);
                    Navigator.pop(context); // Close the settings page
                  }
                },
              ),
            ),
            ListTile(
              title: const Text('Dark Mode'),
              leading: Radio<ThemeMode>(
                value: ThemeMode.dark,
                groupValue: currentTheme,
                onChanged: (ThemeMode? value) {
                  if (value != null) {
                    onThemeChange(value);
                    Navigator.pop(context); // Close the settings page
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            const TextField(
              decoration: InputDecoration(labelText: 'Username'),
            ),
            const TextField(
              obscureText: true,
              decoration: InputDecoration(labelText: 'Password'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: null, // Add your login logic here
              child: const Text('Login'),
            ),
            const SizedBox(height: 20),
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const RegisterPage()),
                );
              },
              child: const Text("Don't have an account? Register here!"),
            ),
          ],
        ),
      ),
    );
  }
}

class RegisterPage extends StatelessWidget {
  const RegisterPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Register')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            const Text(
              'Register Page',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            const TextField(
              decoration: InputDecoration(labelText: 'Email'),
            ),
            const TextField(
              decoration: InputDecoration(labelText: 'Username'),
            ),
            const TextField(
              obscureText: true,
              decoration: InputDecoration(labelText: 'Password'),
            ),
            const SizedBox(height: 20),
            Center(
              child: ElevatedButton(
                onPressed: null, // Add your registration logic here
                child: const Text('Register Now'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}