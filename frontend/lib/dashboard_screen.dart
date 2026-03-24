import 'package:flutter/material.dart';
import 'theme.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.lightBlue,
      appBar: AppBar(
        title: const Text('Dashboard'),
        backgroundColor: AppColors.buttonBlue,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ListView(
          children: [
            _tile(
              icon: Icons.notifications,
              title: 'Performance Alert',
              subtitle: 'You’re behind on Chemistry – check smart schedule.',
            ),
            const Divider(),
            _tile(
              icon: Icons.schedule,
              title: 'Smart Schedule',
              subtitle: '8:00–9:30 AM: Math Revision',
            ),
            const Divider(),
            _tile(
              icon: Icons.bar_chart,
              title: 'Weekly Progress',
              subtitle: '85% target achieved',
            ),
          ],
        ),
      ),
    );
  }

  Widget _tile({
    required IconData icon,
    required String title,
    required String subtitle,
  }) {
    return ListTile(
      leading: Icon(icon, color: AppColors.buttonBlue),
      title: Text(title, style: TextStyle(fontWeight: FontWeight.bold)),
      subtitle: Text(subtitle),
    );
  }
}
