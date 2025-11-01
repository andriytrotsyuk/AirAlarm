import UkraineAlarm

from .conf import API_KEY

WAIT_MS = 2000

configuration = UkraineAlarm.Configuration()
configuration.host = 'https://api.ukrainealarm.com'
configuration.api_key['Authorization'] = API_KEY
api_instance = UkraineAlarm.RegionsApi(UkraineAlarm.ApiClient(configuration))


def get_states():
    return api_instance.api_v3_regions_get().states


def get_active_alarm_start_at(region_id):
    api_instance = UkraineAlarm.AlertsApi(UkraineAlarm.ApiClient(configuration))
    api_response = api_instance.api_v3_alerts_region_id_get(region_id)
    if not api_response[0].active_alerts:
        return None
    return min(alert.last_update for alert in api_response[0].active_alerts)
