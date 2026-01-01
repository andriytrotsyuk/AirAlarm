import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../api/ukraine_alarm_api.dart';
import '../utils/constants.dart';
import '../models/region.dart';

class AppState with ChangeNotifier {
  final UkraineAlarmAPI _api = UkraineAlarmAPI();
  final AudioPlayer _audioPlayer = AudioPlayer();

  String? _regionId;
  String? get regionId => _regionId;

  String? _connectionError;
  String? get connectionError => _connectionError;

  String? _audioError;
  String? get audioError => _audioError;

  bool _isAlarm = false;
  bool get alarmNotification => _isAlarm;

  bool _sirenPlaying = false;
  bool get sirenPlaying => _sirenPlaying;

  int _durationMinutes = 3;
  int get durationMinutes => _durationMinutes;

  bool _isAnthemEnabled = false;
  bool get isAnthemEnabled => _isAnthemEnabled;

  Timer? _checkAlarmTimer;

  Timer? _stopSirenTimer;

  List<Region> _regions = [];
  List<Region> get regions => _regions;

  Timer? _anthemTimer;
  final AudioPlayer _anthemPlayer = AudioPlayer();
  bool _isAnthemPlaying = false;

  AppState() {
    _loadSettings();
    _loadRegions();
    _checkAudioAvailability();
  }

  void _init() {
    if (_regionId != null && _regionId!.isNotEmpty) {
      _startMonitoring();
    }
    _scheduleAnthem();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    _regionId = prefs.getString('region_id');
    _durationMinutes = prefs.getInt('duration') ?? 3;
    _isAnthemEnabled = prefs.getBool('is_anthem_enabled') ?? false;
    notifyListeners();
  }

  Future<void> _checkAudioAvailability() async {
    _audioError = null;
    try {
      await _audioPlayer.play(AssetSource(Constants.silenceSoundPath));
    } catch (e) {
      _audioError = 'Аудіо відключене';
      print('Audio availability check failed: $e');
      return;
    } finally {
      notifyListeners();
    }
    // We don't want to actually play silence indefinitely if it loops, but
    // silence is short.
    // Ideally stop it immediately if it works.
    // But wait slightly to ensure it actually starts?
    // play() is async, if it throws it throws.
    // Let's stop it just in case.
    await _audioPlayer.stop();
    _init();
  }

  Future<void> _loadRegions() async {
    final String response = await rootBundle.loadString('assets/regions.json');
    final List<dynamic> data = json.decode(response);
    _regions = data.map((json) => Region.fromJson(json)).toList();
    notifyListeners();
  }

  Future<void> setRegion(String id) async {
    _regionId = id;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('region_id', id);
    _startMonitoring();
    notifyListeners();
  }

  Future<void> clearRegion() async {
    _regionId = null;
    _stopSirenTimer?.cancel();
    _stopSiren();
    _checkAlarmTimer?.cancel();
    _isAlarm = false;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('region_id');
    notifyListeners();
  }

  Future<void> setDuration(int minutes) async {
    _durationMinutes = minutes;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('duration', minutes);
    notifyListeners();
  }

  Future<void> setAnthemEnabled(bool enabled) async {
    _isAnthemEnabled = enabled;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('is_anthem_enabled', enabled);
    notifyListeners();
  }

  void _startMonitoring() {
    _checkAlarmTimer?.cancel();
    _checkAlarmTimer =
        Timer.periodic(const Duration(seconds: 2), (timer) => _checkAlarm());
    _checkAlarm(); // Initial check
  }

  Future<void> _checkAlarm() async {
    if (_regionId == null || _regionId!.isEmpty) return;

    try {
      final startAt = await _api.getActiveAlarmStartAt(_regionId!);
      _connectionError = null; // Clear error on success

      if (startAt == null) {
        // No alarm
        if (_isAlarm) {
          _stopSirenTimer?.cancel();
          _stopSiren();
          _playEnd();
        }
        _isAlarm = false;
      } else {
        // Alarm active
        _isAlarm = true;
        final endPlayAt = startAt.add(Duration(minutes: _durationMinutes));
        _playSiren(endPlayAt);
      }
    } catch (e) {
      _connectionError = 'Помилка з\'єднання';
      print('Error checking alarm: $e');
    }
    notifyListeners();
  }

  Future<void> _playSiren(DateTime stopTime) async {
    if (_sirenPlaying) return;
    final now = DateTime.now();
    final durationToWait = stopTime.difference(now);

    if (durationToWait.isNegative) {
      return;
    }

    // Stop anthem if playing
    if (_isAnthemPlaying) {
      await _stopAnthem();
    }

    _sirenPlaying = true;
    await _audioPlayer.play(AssetSource(Constants.startSoundPath));
    await _audioPlayer.setReleaseMode(ReleaseMode.loop);

    _stopSirenTimer = Timer(durationToWait, () {
      _stopSiren();
    });
  }

  Future<void> _stopSiren() async {
    if (!_sirenPlaying) return;
    await _audioPlayer.stop();
    _sirenPlaying = false;
    notifyListeners();
  }

  Future<void> _playEnd() async {
    await _audioPlayer.setReleaseMode(ReleaseMode.release);
    await _audioPlayer.play(AssetSource(Constants.endSoundPath));
  }

  void _scheduleAnthem() {
    _anthemTimer?.cancel();
    final now = DateTime.now();
    var scheduledTime = DateTime(now.year, now.month, now.day, 9, 0, 0);
    if (scheduledTime.isBefore(now)) {
      scheduledTime = scheduledTime.add(const Duration(days: 1));
    }
    final duration = scheduledTime.difference(now);
    _anthemTimer = Timer(duration, _playAnthemSequence);
  }

  Future<void> _playAnthemSequence() async {
    // Schedule next day
    _scheduleAnthem();
    if (!_isAnthemEnabled || _sirenPlaying) {
      return;
    }
    _isAnthemPlaying = true;
    notifyListeners();
    // Play silence
    await _anthemPlayer.play(AssetSource(Constants.silenceSoundPath));
    // Listen for completion to play anthem
    // Note: We need a one-time listener or manage state carefully
    // to avoid playing anthem after anthem finishes if we use a persistent listener.
    // Simpler approach: await completion if possible, but play() is async fire-and-forget for completion usually.
    // audioplayers play() returns void/Future.
    // We can use onPlayerComplete for sequencing.
    _anthemPlayer.onPlayerComplete.first.then((_) async {
      if (_isAnthemPlaying) {
        // Check if not interrupted
        await _anthemPlayer.play(AssetSource(Constants.anthemSoundPath));
        // Reset flag after anthem finishes
        _anthemPlayer.onPlayerComplete.first.then((_) {
          _isAnthemPlaying = false;
          notifyListeners();
        });
      }
    });
  }

  Future<void> _stopAnthem() async {
    await _anthemPlayer.stop();
    _isAnthemPlaying = false;
    notifyListeners();
  }
}
