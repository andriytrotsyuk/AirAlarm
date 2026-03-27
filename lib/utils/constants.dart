import 'package:flutter_dotenv/flutter_dotenv.dart';

class Constants {
  static String get apiKey => dotenv.env['API_KEY'] ?? '';
  static const String apiHost = 'https://api.ukrainealarm.com';
  static const String appName = 'Тривога';
  static const Duration alarmCheckInterval = Duration(seconds: 10);

  // Asset paths
  static const String startSoundPath = 'sounds/sirena.mp3';
  static const String endSoundPath = 'sounds/vdbj.mp3';
  static const String minuteSoundPath = 'sounds/hvilina.mp3';
  static const String anthemSoundPath = 'sounds/gimn.mp3';
  static const String silenceSoundPath = 'sounds/silence.mp3';
}
