import json
from urllib.request import Request, urlopen


LOCATION_MAP = {
    21: 3,
    1: 4,
    16: 5,
    2: 8,
    3: 9,
    5: 10,
    6: 11,
    7: 12,
    8: 13,
    9: 14,
    10: 15,
    11: 16,
    13: 17,
    14: 18,
    15: 19,
    17: 20,
    18: 21,
    19: 22,
    20: 23,
    22: 24,
    24: 25,
    23: 26,
    12: 27,
    4: 28,
    26: 29,
    27: 30,
    25: 31,
}


def is_alarm(region_id: str) -> bool:
    location_id = LOCATION_MAP[region_id]
    request = Request(
        f'https://api.alerts.in.ua/v1/iot/active_air_raid_alerts/{location_id}.json',
        headers={'Authorization': 'Bearer '},
    )
    with urlopen(request) as response:
        state = json.load(response)
    return state in 'AP'
