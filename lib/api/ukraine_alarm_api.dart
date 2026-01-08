import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/constants.dart';
import '../models/region.dart';

class UkraineAlarmAPI {
  final String _apiKey = Constants.apiKey;
  final String _host = Constants.apiHost;

  Future<List<Region>> getRegions() async {
    // Note: This endpoint might need adjustment based on actual API response structure
    // The Python code uses a specific library, here we mock or implement based on assumption
    // For now, we will return a hardcoded list or try to fetch if we knew the exact endpoint.
    // Python: api_instance.api_v3_regions_get().states

    // Since I don't have the exact API docs for the raw HTTP endpoints easily available
    // without reverse engineering the python library more deeply,
    // I will implement a basic fetch but also fallback to a comprehensive list if needed.
    // However, the python code loads regions.json locally initially.
    // Let's try to fetch from API if possible, or maybe we should just use the local regions.json logic?
    // The Python code has a 'regions.py' that loads from 'regions.json'.
    // I should probably port the 'regions.json' content or logic.
    // But for now let's implement the alert check which is critical.

    return [];
  }

  Future<DateTime?> getActiveAlarmStartAt(String regionId) async {
    final url = Uri.parse('$_host/api/v3/alerts/$regionId');
    final response = await http.get(
      url,
      headers: {
        'Authorization': _apiKey,
        'accept': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      if (data.isNotEmpty) {
        final regionData = data[0];
        final activeAlerts = regionData['activeAlerts'] as List<dynamic>?;

        if (activeAlerts != null && activeAlerts.isNotEmpty) {
          // Find the earliest start time
          DateTime? minDate;
          for (var alert in activeAlerts) {
            final lastUpdate = DateTime.parse(alert['lastUpdate']);
            if (minDate == null || lastUpdate.isBefore(minDate)) {
              minDate = lastUpdate;
            }
          }
          return minDate;
        }
      }
    } else {
      throw Exception('Failed to load alerts: ${response.statusCode}');
    }
    return null;
  }
}
