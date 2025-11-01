import json

from providers.ukrainealarm import get_states

from settings import REGIONS_PATH


class Regions:
    def __init__(self):
        with REGIONS_PATH.open() as f:
            self._data = json.load(f)

    def filter(self, text):
        if not text:
            return self._data.copy()
        return [region for region in self._data if text in region['name'].lower()]

    def get(self, identifier):
        for region in self._data:
            if region['id'] == identifier:
                return region
        return self._data[0]


def init():
    states = get_states()
    flat = []
    for state in states:
        display_name = state.region_name
        flat.append({
            'id': state.region_id,
            'name': state.region_name,
            'display': display_name,
        })
        if state.region_child_ids:
            for district in state.region_child_ids:
                display_name = f"{district.region_name}\n{state.region_name}"
                flat.append({
                    'id': district.region_id,
                    'name': district.region_name,
                    'display': display_name,
                })
                if district.region_child_ids:
                    for community in district.region_child_ids:
                        display_name = f"{community.region_name}\n{district.region_name}\n{state.region_name}"
                        flat.append({
                            'id': community.region_id,
                            'name': community.region_name,
                            'display': display_name,
                        })
    flat = sorted(flat, key=_key)
    with REGIONS_PATH.open(mode='w') as f:
        json.dump(flat, f)


# Ukrainian alphabet order for sorting
ALPHABET = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя"


def _key(region):
    main_name = region['name']
    # Convert to sorting key based on Ukrainian alphabet
    return [ALPHABET.index(char) if char in ALPHABET else ord(char) for char in main_name]


if __name__ == '__main__':
    init()
else:
    REGIONS = Regions()
