import json
import http.client


WAIT_MS = 2000

REGION_MAP = {
    25: 31,
    10: 15,
    15: 19,
    26: 9999,
    22: 24,
    6: 11,
    4: 28,
    13: 17,
    17: 20,
    2: 8,
    20: 23,
    8: 13,
    14: 18,
    21: 3,
    1: 4,
    24: 25,
    23: 26,
    16: 5,
    9: 14,
    18: 21,
    11: 16,
    12: 27,
    7: 12,
    3: 9,
    19: 22,
    5: 10,
    # {
    #   "regionId": "0",
    #   "regionName": "Тестовий регіон",
    #   "regionType": "State",
    #   "regionChildIds": []
    # }
}


def is_alarm(region_id: int) -> bool:
    external_region_id = REGION_MAP[region_id]
    conn = http.client.HTTPSConnection('api.ukrainealarm.com')
    endpoint = f'/api/v3/alerts/{external_region_id}'
    headers = {
        "Authorization": ""
    }
    conn.request("GET", endpoint, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    regions_alarm = json.loads(data)
    region_alarm = regions_alarm[0]
    active_alerts = region_alarm['activeAlerts']
    for active_alert in active_alerts:
        alert_region_id = active_alert['regionId']
        if str(external_region_id) == alert_region_id:
            return True
    return False
