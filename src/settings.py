__all__ = (
    'INTERNAL',
    'FONT_FAMILY',
    'CONFIG_APP',
    'CONFIG_TEMPLATE_PATH',
    'LOGS',
    'ICONS_PATH',
    'START_PATH',
    'END_PATH',
    'SILENCE_PATH',
    'ANTHEM_PATH',
    'ANTHEM_TIME',
    'NETWORK_ERROR',
    'REGIONS_PATH',
    'AUTOSTART',
)

import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    RUNNING_FILE = sys.executable
else:
    # Running in a normal Python process
    RUNNING_FILE = __file__
PARENT = Path(RUNNING_FILE).parent
INTERNAL = PARENT / "_internal"
CONFIG_TEMPLATE_PATH = INTERNAL / "config.json"
REGIONS_PATH = INTERNAL / "regions.json"
ICONS_PATH = INTERNAL / "icons"
SOUND_PATH = INTERNAL / "Sound"

START_PATH = SOUND_PATH / "sirena.mp3"
END_PATH = SOUND_PATH / "vdbj.mp3"
SILENCE_PATH = SOUND_PATH / "hvilina.mp3"
ANTHEM_PATH = SOUND_PATH / "gimn.mp3"

ANTHEM_TIME = {'hour': 9, 'minute': 0, 'second': 0, 'microsecond': 0}
NETWORK_ERROR = 'Інтернет зʼєднання відсутнє'
FONT_FAMILY = 'Helvetica'

CONFIG_HOME = Path(os.getenv('XDG_CONFIG_HOME', default=Path.home() / '.config'))
CONFIG_APP = CONFIG_HOME / 'airalarm'
AUTOSTART = CONFIG_HOME / 'autostart'
DATA_HOME = Path(os.getenv('XDG_DATA_HOME',	default=Path.home() / '.local/share'))
DATA_APP = DATA_HOME / 'AirAlarm'
LOGS = DATA_APP / 'logs'
