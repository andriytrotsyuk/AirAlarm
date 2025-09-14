import UkraineAlarm

from .conf import API_KEY

WAIT_MS = 2000

configuration = UkraineAlarm.Configuration()
configuration.host = 'https://api.ukrainealarm.com'
configuration.api_key['Authorization'] = API_KEY
api_instance = UkraineAlarm.RegionsApi(UkraineAlarm.ApiClient(configuration))


class Regions:
    def __init__(self):
        # FIXME: sort of Ukrainian alphabet
        self.states = sorted(api_instance.api_v3_regions_get().states, key=lambda x: x.region_name)
        self.max_len = 0
        for state in self.states:
            self.max_len = max(self.max_len, len(state.region_name))
            if state.region_child_ids is None:
                continue
            state.region_child_ids = sorted(state.region_child_ids, key=lambda x: x.region_name)
            for district in state.region_child_ids:
                self.max_len = max(self.max_len, len(district.region_name))
                if district.region_child_ids is None:
                    continue
                district.region_child_ids = sorted(district.region_child_ids, key=lambda x: x.region_name)
                for community in district.region_child_ids:
                    self.max_len = max(self.max_len, len(community.region_name))
                    # print(community.region_id, community.region_name)

    @property
    def state_names(self):
        return [state.region_name for state in self.states]

    def __getitem__(self, index):
        return self.states[index]

    def __len__(self):
        return len(self.states)

    def get_indexes(self, region_id: int) -> int:
        for state_i, state in enumerate(self.states):
            if state.region_id == region_id:
                return state_i, None, None
            if state.region_child_ids is None:
                continue
            for district_i, district in enumerate(state.region_child_ids):
                if district.region_id == region_id:
                    return state_i, district_i, None
                if district.region_child_ids is None:
                    continue
                for community_i, community in enumerate(district.region_child_ids):
                    if community.region_id == region_id:
                        return state_i, district_i, community_i
        return None, None, None


REGIONS = Regions()


def get_active_alarm_start_at(region_id):
    api_instance = UkraineAlarm.AlertsApi(UkraineAlarm.ApiClient(configuration))
    api_response = api_instance.api_v3_alerts_region_id_get(region_id)
    if not api_response[0].active_alerts:
        return None
    return min(alert.last_update for alert in api_response[0].active_alerts)
