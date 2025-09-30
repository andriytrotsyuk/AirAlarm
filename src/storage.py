from datetime import datetime


class State:
    def __init__(self):
        self.SirenaNowPlaying = False
        self.SirenaPlayed = False
        self.end = datetime(1, 1, 1)
        self.MusicPlaying = False
        self.alarmNotification = False
