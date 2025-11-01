__all__ = ('is_enabled', 'enable', 'disable')

import getpass
import os
import shutil
import sys
from faulthandler import is_enabled
from pathlib import Path

if sys.platform == 'win32':
    USER_NAME = getpass.getuser()
    path = rf'C:\Users\{USER_NAME}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\openAiralarm.bat'

    def is_enabled():
        return Path(path).exists()

    def enable():
        file_path = os.getcwd()
        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
        with open(bat_path + '\\' + "openAiralarm.bat", "w+") as bat_file:
            bat_file.write('chcp 1251\n')
            bat_file.write('cd /D %s\n' % file_path)
            bat_file.write(r'start %s' % "airalarm.exe")

    def disable():
        os.remove(path)
elif sys.platform == 'linux':
    from settings import AUTOSTART

    APPS_PATH = Path.home() / '/usr/share/applications'
    FILENAME = 'airalarm.desktop'
    path = AUTOSTART / FILENAME

    def is_enabled():
        return path.exists()

    def enable():
        os.makedirs(AUTOSTART, exist_ok=True)
        shutil.copy(APPS_PATH / FILENAME, AUTOSTART)

    def disable():
        path.unlink()
else:
    # raise NotImplementedError()
    def is_enabled():
        return False
