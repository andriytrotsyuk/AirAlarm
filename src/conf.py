__all__ = (
    'BASE_PATH',
    'FONT_FAMILY',
    'SETTINGS_PATH',
    'ICONS_PATH',
    'START_PATH',
    'END_PATH',
    'SILENCE_PATH',
    'ANTHEM_PATH',
    'ANTHEM_TIME',
    'NETWORK_ERROR',
    'REGIONS_PATH',
)

import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    RUNNING_FILE = sys.executable
else:
    # Running in a normal Python process
    RUNNING_FILE = __file__
SRC_PATH = Path(RUNNING_FILE).parent
BASE_PATH = SRC_PATH / "_internal"
SETTINGS_PATH = BASE_PATH / "settings.json"
REGIONS_PATH = BASE_PATH / "regions.json"
ICONS_PATH = BASE_PATH / "icons"
SOUND_PATH = BASE_PATH / "Sound"

START_PATH = SOUND_PATH / "sirena.mp3"
END_PATH = SOUND_PATH / "vdbj.mp3"
SILENCE_PATH = SOUND_PATH / "hvilina.mp3"
ANTHEM_PATH = SOUND_PATH / "gimn.mp3"

ANTHEM_TIME = {'hour': 9, 'minute': 0, 'second': 0, 'microsecond': 0}
NETWORK_ERROR = 'Інтернет зʼєднання відсутнє'
FONT_FAMILY = 'Helvetica'
