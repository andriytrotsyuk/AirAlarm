import 'package:flutter/material.dart';
import 'package:package_info_plus/package_info_plus.dart';

class AboutAppDialog extends StatelessWidget {
  const AboutAppDialog({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<PackageInfo>(
      future: PackageInfo.fromPlatform(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const AlertDialog(
            content: SizedBox(
              height: 100,
              child: Center(child: CircularProgressIndicator()),
            ),
          );
        }

        final packageInfo = snapshot.data!;

        return AlertDialog(
          title: const Text(''),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const SizedBox(height: 10),
                // App Icon
                Image.asset(
                  'icons/app.png',
                  width: 64,
                  height: 64,
                  errorBuilder: (context, error, stackTrace) =>
                      const Icon(Icons.security, size: 64),
                ),
                const SizedBox(height: 16),
                // App Name & Version
                Text(
                  'Повітряна тривога',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 4),
                Text(
                  'Версія ${packageInfo.version}',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Theme.of(context).colorScheme.outline,
                      ),
                ),
                const SizedBox(height: 24),
                // Description
                const Text(
                  'Програма для сповіщення про повітряні тривоги в Україні.',
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 24),
                // Copyright
                Text(
                  '© 2025 zd4school',
                  style: Theme.of(context).textTheme.bodySmall,
                ),
                const SizedBox(height: 8),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Закрити'),
            ),
          ],
        );
      },
    );
  }
}
