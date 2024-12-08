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
{
  "states": [
    {
      "regionId": "31",
      "regionName": "м. Київ",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "15",
      "regionName": "Кіровоградська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "19",
      "regionName": "Полтавська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "9999",
      "regionName": "Автономна Республіка Крим",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "24",
      "regionName": "Черкаська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "11",
      "regionName": "Закарпатська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "28",
      "regionName": "Донецька область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "17",
      "regionName": "Миколаївська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "20",
      "regionName": "Сумська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "8",
      "regionName": "Волинська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "23",
      "regionName": "Херсонська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "13",
      "regionName": "Івано-Франківська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "18",
      "regionName": "Одеська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "3",
      "regionName": "Хмельницька область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "4",
      "regionName": "Вінницька область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "25",
      "regionName": "Чернігівська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "26",
      "regionName": "Чернівецька область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "5",
      "regionName": "Рівненська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "14",
      "regionName": "Київська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "21",
      "regionName": "Тернопільська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "16",
      "regionName": "Луганська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "27",
      "regionName": "Львівська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "12",
      "regionName": "Запорізька область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "9",
      "regionName": "Дніпропетровська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "22",
      "regionName": "Харківська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "10",
      "regionName": "Житомирська область",
      "regionType": "State",
      "regionChildIds": []
    },
    {
      "regionId": "0",
      "regionName": "Тестовий регіон",
      "regionType": "State",
      "regionChildIds": []
    }
  ]
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
