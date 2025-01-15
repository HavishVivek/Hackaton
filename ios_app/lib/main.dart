import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;

/// Flutter code sample for [CupertinoTabBar].

void main() => runApp(const CupertinoTabBarApp());

class CupertinoTabBarApp extends StatelessWidget {
  const CupertinoTabBarApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const CupertinoApp(
      theme: CupertinoThemeData(brightness: Brightness.light),
      home: CupertinoTabBarExample(),
    );
  }
}

class CupertinoTabBarExample extends StatelessWidget {
  const CupertinoTabBarExample({super.key});

  @override
  Widget build(BuildContext context) {
    return CupertinoTabScaffold(
      tabBar: CupertinoTabBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.cloud_upload),
            label: 'SMS Threat',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.settings),
            label: 'Settings',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.person_alt_circle_fill),
            label: 'Login/Register',
          ),
        ],
      ),
      tabBuilder: (BuildContext context, int index) {
        switch (index) {
          case 0:
            return CupertinoTabView(
              builder: (BuildContext context) {
                return const SMSThreatTab();
              },
            );
          case 1:
            return CupertinoTabView(
              builder: (BuildContext context) {
                return const Center(
                  child: Text('Settings Tab'),
                );
              },
            );
          case 2:
            return CupertinoTabView(
              builder: (BuildContext context) {
                return const Center(
                  child: Text('Login/Register Tab'),
                );
              },
            );
          default:
            return const Center(
              child: Text('Content not found'),
            );
        }
      },
    );
  }
}

class SMSThreatTab extends StatefulWidget {
  const SMSThreatTab({super.key});

  @override
  _SMSThreatTabState createState() => _SMSThreatTabState();
}

class _SMSThreatTabState extends State<SMSThreatTab> {
  final TextEditingController _controller = TextEditingController();
  String _result = "";

  Future<void> _detectSpam(String message) async {
    const url = 'http://192.168.1.212:5001/predict'; // Replace <your_ip> with your backend's IP
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'message': message}),
      );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        setState(() {
          _result = responseData['prediction'] == 'spam' ? "This is Spam!" : "This is Safe!";
        });
      } else {
        setState(() {
          _result = "Error: Unable to classify the message.";
        });
      }
    } catch (e) {
      setState(() {
        _result = "Error: Could not connect to the server.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: const CupertinoNavigationBar(
        middle: Text('SMS Threat Detection'),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CupertinoTextField(
              controller: _controller,
              placeholder: "Enter SMS message",
              padding: const EdgeInsets.all(12),
            ),
            const SizedBox(height: 16),
            CupertinoButton.filled(
              onPressed: () {
                _detectSpam(_controller.text);
              },
              child: const Text('Detect'),
            ),
            const SizedBox(height: 16),
            Text(
              _result,
              style: const TextStyle(fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}