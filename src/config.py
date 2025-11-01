__all__ = ["CONFIG"]

import json
import shutil

from settings import CONFIG_TEMPLATE_PATH, CONFIG_APP


class Config:
    def __init__(self):
        CONFIG_APP.mkdir(parents=True, exist_ok=True)
        self._path = CONFIG_APP / 'config.json'
        if not self._path.exists():
            shutil.copy(CONFIG_TEMPLATE_PATH, CONFIG_APP)
        with self._path.open("r", encoding="utf-8") as f:
            self._settings = json.load(f)
        self.region_id = self._settings["region_id"]
        self.time = self._settings["time"]

    @property
    def region_id(self):
        return self._settings["region_id"]

    @region_id.setter
    def region_id(self, value):
        self._settings["region_id"] = value
        self._save()

    @property
    def time(self):
        return self._settings["time"]

    @time.setter
    def time(self, value):
        self._settings["time"] = value
        self._save()

    @property
    def is_anthem_enabled(self):
        return self._settings["is_anthem_enabled"]

    @is_anthem_enabled.setter
    def is_anthem_enabled(self, value):
        self._settings["is_anthem_enabled"] = value
        self._save()

    def _save(self):
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(self._settings, f)


CONFIG = Config()
