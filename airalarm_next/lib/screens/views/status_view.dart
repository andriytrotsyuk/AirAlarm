import 'package:flutter/material.dart';
import 'package:flutter_spinbox/flutter_spinbox.dart';
import 'package:provider/provider.dart';
import '../../providers/app_state.dart';
import '../../models/region.dart';

class StatusView extends StatelessWidget {
  const StatusView({super.key});

  @override
  Widget build(BuildContext context) {
    final appState = Provider.of<AppState>(context);

    Region? region;
    try {
      region = appState.regions.firstWhere((r) => r.id == appState.regionId);
    } catch (_) {
      region = null;
    }

    final displayRegion =
        region != null ? region.name : (appState.regionId ?? '');

    return Column(
      children: [
        // Region Name
        Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                displayRegion,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 8),
              TextButton(
                onPressed: () {
                  appState.clearRegion();
                },
                child: const Text('Змінити'),
              ),
            ],
          ),
        ),

        // Alarm Status
        Expanded(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  appState.connectionError != null
                      ? Icons.signal_wifi_connected_no_internet_4_rounded
                      : (appState.alarmNotification
                          ? Icons.warning_rounded
                          : Icons.check_circle_rounded),
                  size: 130,
                  color: appState.connectionError != null
                      ? Colors.orange
                      : (appState.alarmNotification
                          ? Colors.red
                          : Colors.green),
                ),
                Text(
                  appState.connectionError ??
                      (appState.alarmNotification
                          ? 'Тривога'
                          : 'Немає тривоги'),
                  style: Theme.of(context).textTheme.displaySmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ],
            ),
          ),
        ),

        // Settings
        Card(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
            child: Column(
              children: [
                Text('Налаштування',
                    style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: Theme.of(context).colorScheme.outline)),
                const SizedBox(height: 8),
                ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(
                    'Тривалість оголошення (хв):',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                  trailing: SizedBox(
                    width: 120,
                    child: SpinBox(
                      min: 1,
                      max: 60,
                      iconSize:
                          Theme.of(context).textTheme.bodyMedium?.fontSize,
                      textStyle: Theme.of(context).textTheme.bodyMedium,
                      decoration: InputDecoration(
                        isDense: true,
                        contentPadding: const EdgeInsets.only(
                            left: 0, right: 0, bottom: 12, top: 12),
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(50),
                          borderSide: BorderSide(
                            color: Theme.of(context).colorScheme.outline,
                            width: 2,
                          ),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(50),
                          borderSide: BorderSide(
                            color: Theme.of(context).colorScheme.primary,
                            width: 2,
                          ),
                        ),
                      ),
                      value: appState.durationMinutes.toDouble(),
                      onChanged: (val) {
                        appState.setDuration(val.toInt());
                      },
                    ),
                  ),
                ),
                ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text('Хвилина мовчання і гімн України',
                      style: Theme.of(context).textTheme.bodyMedium),
                  trailing: Switch(
                    value: appState.isAnthemEnabled,
                    onChanged: (val) => appState.setAnthemEnabled(val),
                  ),
                ),
                ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text('Автозапуск',
                      style: Theme.of(context).textTheme.bodyMedium),
                  trailing: Switch(
                    value: false,
                    onChanged: (val) => {},
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
