import 'dart:io';
import 'package:logger/logger.dart';
import 'package:path_provider/path_provider.dart';

class LoggerService {
  static late Logger _logger;
  static late String logFilePath;

  static Future<void> init() async {
    final Directory directory = await getApplicationSupportDirectory();
    logFilePath = '${directory.path}/app_log.txt';
    
    _logger = Logger(
      level: Level.all,
      printer: PrettyPrinter(
        methodCount: 0,
        errorMethodCount: 5,
        lineLength: 80,
        colors: false,
        printEmojis: true,
        dateTimeFormat: DateTimeFormat.dateAndTime,
      ),
      output: MultiOutput([
        ConsoleOutput(),
        FileOutput(
          file: File(logFilePath),
          overrideExisting: false,
        ),
      ]),
    );

    _logger.i("Logger initialized at $logFilePath");
  }

  static void i(dynamic message) {
    _logger.i(message);
  }

  static void d(dynamic message) {
    _logger.d(message);
  }

  static void e(dynamic message, [dynamic error, StackTrace? stackTrace]) {
    _logger.e(message, error: error, stackTrace: stackTrace);
  }

  static void w(dynamic message) {
    _logger.w(message);
  }
}
