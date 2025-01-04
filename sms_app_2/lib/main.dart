import 'package:flutter/material.dart';


void main() => runApp(const BadgeExampleApp());

class BadgeExampleApp extends StatelessWidget {
  const BadgeExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar:AppBar(title: Text('Badge Sample')),
        body: const BadgeExample(),
      ),
    );
  }
}

class BadgeExample extends StatelessWidget {
  const BadgeExample({super.key});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.bottomCenter,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: <Widget>[
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(
                icon: const Badge(
                  child: Icon(Icons.upload),
                ),
                onPressed: () {},
              ),
              const Text('SMS Threat'),
            ],
          ),
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(
                icon: const Badge(
                  child: Icon(Icons.settings),
                ),
                onPressed: () {},
              ),
              const Text('Settings'),
            ],
          ),
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(
                icon: const Badge(
                  child: Icon(Icons.person),
                ),
                onPressed: () {},
              ),
              const Text('Login'),
            ],
          ),
        ],
      ),
    );
  }
}
