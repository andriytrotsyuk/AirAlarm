import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:window_manager/window_manager.dart';
import 'package:tray_manager/tray_manager.dart';

import '../providers/app_state.dart';
import 'views/status_view.dart';
import 'views/search_view.dart';

import 'package:package_info_plus/package_info_plus.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen>
    with WindowListener, TrayListener {
  String _version = '';

  @override
  void initState() {
    super.initState();
    windowManager.addListener(this);
    trayManager.addListener(this);
    _init();
    _loadVersion();

    // Listen to AppState changes
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final appState = Provider.of<AppState>(context, listen: false);
      appState.addListener(_updateTrayIcon);
    });
  }

  @override
  void dispose() {
    windowManager.removeListener(this);
    trayManager.removeListener(this);
    super.dispose();
  }

  String _currentIcon = 'assets/safe.ico';

  void _updateTrayIcon() {
    final appState = Provider.of<AppState>(context, listen: false);
    String newIcon;

    if (appState.connectionError != null) {
      newIcon = 'assets/unknown.ico';
    } else if (appState.alarmNotification) {
      newIcon = 'assets/alarm.ico';
    } else {
      newIcon = 'assets/safe.ico';
    }

    if (_currentIcon != newIcon) {
      _currentIcon = newIcon;
      trayManager.setIcon(newIcon);
    }
  }

  void _init() async {
    await windowManager.setPreventClose(true);
    // Initial icon set
    final appState = Provider.of<AppState>(context, listen: false);
    if (appState.connectionError != null || appState.audioError != null) {
      _currentIcon = 'assets/unknown.ico';
    } else if (appState.alarmNotification) {
      _currentIcon = 'assets/alarm.ico';
    } else {
      _currentIcon = 'assets/safe.ico';
    }
    await trayManager.setIcon(_currentIcon);
    await trayManager.setToolTip('Повітряна тривога');
    Menu menu = Menu(
      items: [
        MenuItem(
          key: 'show_window',
          label: 'Відкрити',
        ),
        MenuItem.separator(),
        MenuItem(
          key: 'exit_app',
          label: 'Вийти',
        ),
      ],
    );
    await trayManager.setContextMenu(menu);
  }

  Future<void> _loadVersion() async {
    final packageInfo = await PackageInfo.fromPlatform();
    setState(() {
      _version = packageInfo.version;
    });
  }

  @override
  void onWindowClose() async {
    bool isPreventClose = await windowManager.isPreventClose();
    if (isPreventClose) {
      windowManager.hide();
    }
  }

  @override
  void onTrayIconMouseDown() {
    windowManager.show();
    windowManager.focus();
  }

  @override
  void onTrayIconRightMouseDown() {
    trayManager.popUpContextMenu();
  }

  @override
  void onTrayMenuItemClick(MenuItem menuItem) {
    if (menuItem.key == 'show_window') {
      windowManager.show();
      windowManager.focus();
    } else if (menuItem.key == 'exit_app') {
      windowManager.destroy();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Consumer<AppState>(
          builder: (context, appState, child) {
            if (appState.regionId == null) {
              return const SearchView();
            } else {
              return const StatusView();
            }
          },
        ),
      ),
      bottomNavigationBar: Container(
        padding: const EdgeInsets.only(left: 20.0, right: 20.0, bottom: 20.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '© 2025 zd4school – Ліцензія MIT',
              style: Theme.of(context)
                  .textTheme
                  .bodySmall
                  ?.copyWith(color: Theme.of(context).colorScheme.outline),
            ),
            Text(
              'Версія $_version',
              style: Theme.of(context)
                  .textTheme
                  .bodySmall
                  ?.copyWith(color: Theme.of(context).colorScheme.outline),
            ),
          ],
        ),
      ),
    );
  }
}
