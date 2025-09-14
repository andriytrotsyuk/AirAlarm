import datetime
import logging.handlers
import re
import tkinter as tk
from tkinter import ttk

import pygame

import autostart
from conf import ICONS_PATH, START_PATH, END_PATH, SILENCE_PATH, ANTHEM_PATH, ANTHEM_TIME
from providers import get_active_alarm_start_at, WAIT_MS, REGIONS
from storage import State
from settings import SETTINGS

LOG_FILENAME = "airalarm.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

APP_NAME = "Повітряна тривога"
APP_STATE = State()

class App:
    def __init__(self):
        # Use `className` parameter here to set name of the window that is visible only in linux Gnome desktop environment
        self._root = tk.Tk(className=APP_NAME)
        self._root.title(APP_NAME)
        self._root.resizable(width=False, height=False)
        self._root.wm_iconphoto(True, *(tk.PhotoImage(file=path) for path in ICONS_PATH.iterdir()))
        self._root.bind("<Button-1>", self._on_click)

        self.frame = ttk.Frame(self._root)
        self.frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        pygame.mixer.init()

        self._settings_frame = SettingsFrame(self)
        self._region_frame = RegionFrame(self)

        copyright_label = ttk.Label(self.frame, text="© 2023, Кір'янчук Юрій")
        copyright_label.grid(row=2, column=0, padx=10, pady=(50, 10), sticky="W")

    def mainloop(self):
        self._root.mainloop()

    def _on_click(self, event):
        event.widget.focus()
    
    def after(self, ms, func=None, *args):
        return self._root.after(ms, func=func, *args)
    
    def after_cancel(self, timer):
        self._root.after_cancel(timer)
    
    def on_region_changed(self, region_id):
        self._settings_frame.on_region_changed(region_id)


class RegionFrame:
    def __init__(self, parent: App):
        self._parent = parent
        frame = ttk.Frame(parent.frame)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        
        label = ttk.Label(frame, text="Оберіть свій регіон", font="Impact 14")
        label.grid(row=0, column=0, sticky="W", padx=5)

        self._state_index, self._district_index, self._community_index = REGIONS.get_indexes(SETTINGS.region_id)
        
        self._state_combobox = ttk.Combobox(
            frame,
            state="readonly",
            width=REGIONS.max_len,
            font="Arial 14",
            values=REGIONS.state_names,
        )
        if self._state_index is not None:
            self._state_combobox.current(self._state_index)
        self._state_combobox.bind("<<ComboboxSelected>>", self._on_state_selected)
        self._state_combobox.grid(row=0, column=1, sticky="W", padx=5)

        self._district_combobox = ttk.Combobox(
            frame,
            state="readonly",
            width=REGIONS.max_len,
            font="Arial 14",
        )
        if self._district_index is None:
            self._districts = []
        else:
            self._districts = REGIONS[self._state_index].region_child_ids
            self._district_combobox.config(values=[district.region_name for district in self._districts])
            self._district_combobox.current(self._district_index)
            self._district_combobox.grid(row=1, column=1, sticky="W", padx=5)
        self._district_combobox.bind("<<ComboboxSelected>>", self._on_district_selected)

        self._community_combobox = ttk.Combobox(
            frame,
            state="readonly",
            width=REGIONS.max_len,
            font="Arial 14",
        )
        if self._community_index is None:
            self._communities = []
        else:
            self._communities = REGIONS[self._state_index].region_child_ids[self._district_index].region_child_ids
            self._community_combobox.config(values=[community.region_name for community in self._communities])
            self._community_combobox.current(self._community_index)
            self._community_combobox.grid(row=2, column=1, sticky="W", padx=5)
        self._community_combobox.bind("<<ComboboxSelected>>", self._on_community_selected)
        self._on_region_changed(SETTINGS.region_id)

    def _on_state_selected(self, event):
        index = event.widget.current()
        if index == self._state_index:
            return
        self._state_index = index
        self._districts = REGIONS[index].region_child_ids
        if self._districts:
            self._district_combobox.set('')
            self._community_combobox.set('')
            district_names = [district.region_name for district in self._districts]
            self._district_combobox.config(values=district_names)
            self._district_combobox.grid(row=1, column=1, sticky="W", padx=5)
            self._on_region_changed(None)
        else:
            self._on_region_changed(REGIONS.states[index].region_id)
            self._district_combobox.grid_remove()
        self._community_combobox.grid_remove()

    def _on_district_selected(self, event):
        index = event.widget.current()
        if index == self._district_index:
            return
        self._district_index = index
        self._communities = self._districts[index].region_child_ids
        if self._communities:
            self._community_combobox.set('')
            community_names = [community.region_name for community in self._communities]
            self._community_combobox.config(values=community_names)
            self._community_combobox.grid(row=2, column=1, sticky="W", padx=5)
        else:
            self._community_combobox.grid_remove()
        self._on_region_changed(None)

    def _on_community_selected(self, event):
        index = event.widget.current()
        if index == self._community_index:
            return
        self._community_index = index
        self._on_region_changed(self._communities[index].region_id)
    
    def _on_region_changed(self, region_id):
        SETTINGS.region_id = region_id
        self._parent.on_region_changed(region_id)


class SettingsFrame:
    def __init__(self, parent: App):
        self._parent = parent
        self.frame = ttk.Frame(parent.frame)
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky="W")
        
        TimePicker(self.frame)
        self._switch = Switch(self)
        additional_functions_label = ttk.Label(self.frame, text="Додаткові функції", font="Impact 16")
        additional_functions_label.grid(row=6, column=0, sticky="W", padx=5, pady=(30, 0))
        Anthem(self)
        Autostart(self)

    def after(self, ms, func=None, *args):
        return self._parent.after(ms, func=func, *args)
    
    def after_cancel(self, timer):
        self._parent.after_cancel(timer)

    def on_region_changed(self, region_id):
        self._switch.on_region_changed(region_id)

class TimePicker:
    def __init__(self, parent: ttk.Frame):
        notification_label = ttk.Label(parent, text="Тривалість оголошення -", font="Arial 14")
        notification_label.grid(row=0, column=0, sticky="W", padx=(5, 0))
        
        validate_command = parent.register(self._validate)
        
        self._entry = ttk.Entry(parent, width=8, validate='key', validatecommand=(validate_command, '%P'))
        self._entry.insert(0, SETTINGS.time)
        self._entry.grid(row=0, column=1, sticky="W")
        self._entry.bind("<FocusOut>", self._on_focus_out)
        
        minutes_label = ttk.Label(parent, text=" хв", font="Arial 14")
        minutes_label.grid(row=0, column=2, sticky="W", padx=(0, 5))

    def _validate(self, newval):
        if re.match('^[0-9]*$', newval) is None or len(newval) > 2:
            return False
        if newval == '0':
            return False
        try:    
            SETTINGS.time = int(newval)
        except ValueError:
            pass
        return True

    def _on_focus_out(self, event):
        event.widget.delete(0, tk.END)
        event.widget.insert(0, SETTINGS.time)


class Switch:
    def __init__(self, parent: SettingsFrame):
        self._parent = parent
        
        self._label = ttk.Label(parent.frame, text="")
        self._label.grid(row=1, column=0, sticky="W", padx=5)
        
        self._start_notification_sound = pygame.mixer.Sound(START_PATH)
        self._end_notification_sound = pygame.mixer.Sound(END_PATH)
    
    def on_region_changed(self, region_id):
        self._start_notification_sound.stop()
        self._end_notification_sound.stop()
        APP_STATE.SirenaPlayed = False
        APP_STATE.SirenaNowPlaying = False
        self._label.config(text='Немає тривоги')
        if region_id is None:
            self._disable()
        else:
            self._enable()

    def _disable(self):
        APP_STATE.alarmNotification = False
        self._label.config(text='')

    def _enable(self):
        APP_STATE.alarmNotification = True
        self.Refresh()

    def Refresh(self):
        try:
            if APP_STATE.alarmNotification:
                start_at = get_active_alarm_start_at(SETTINGS.region_id)
                logger.debug("Are authorities signalling about air alarm now: %s", start_at)
                logger.debug("Has siren played already: %s", APP_STATE.SirenaPlayed)
                logger.debug("Is siren playing now: %s", APP_STATE.SirenaNowPlaying)
                if start_at is None:
                    if APP_STATE.SirenaPlayed:  # Відбій
                        # FIXME: play after anthem
                        length = self._end_notification_sound.get_length()
                        self._start_notification_sound.stop()
                        self._end_notification_sound.play(loops=1)
                        APP_STATE.SirenaPlayed = False
                        self._label.config(text="Немає тривоги")
                        APP_STATE.SirenaNowPlaying = True
                        APP_STATE.end = datetime.datetime.now() + datetime.timedelta(seconds=length)
                else:
                    end_play_at = start_at + datetime.timedelta(minutes=SETTINGS.time)
                    if end_play_at < datetime.datetime.now(datetime.UTC):
                        APP_STATE.SirenaPlayed = True
                        self._label.config(text="Тривога")
                    if not APP_STATE.SirenaPlayed:  # Тривога
                        seconds = SETTINGS.time * 60
                        pygame.mixer.music.stop()
                        self._end_notification_sound.stop()
                        self._start_notification_sound.play(loops=-1, maxtime=seconds * 1000, fade_ms=5 * 1000)
                        APP_STATE.SirenaPlayed = True
                        self._label.config(text="Тривога")
                        APP_STATE.SirenaNowPlaying = True
                        APP_STATE.end = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        except Exception as err:
            logger.exception(err)
        if APP_STATE.SirenaNowPlaying and datetime.datetime.now() > APP_STATE.end:
            APP_STATE.SirenaNowPlaying = False
        self._parent.after(WAIT_MS, self.Refresh)


class Anthem:
    def __init__(self, parent: SettingsFrame):
        self._parent = parent

        self._is_anthem_enabled = tk.BooleanVar(value=SETTINGS.is_anthem_enabled)
        self._is_anthem_enabled.set(SETTINGS.is_anthem_enabled)
        checkbutton = ttk.Checkbutton(
            self._parent.frame,
            variable=self._is_anthem_enabled,
            text="Хвилина мовчання і гімн України",
            command=self._command,
        )
        checkbutton.grid(row=7, column=0, sticky="W", padx=5)
        self._timer = None
        self._command()

    def _command(self):
        SETTINGS.is_anthem_enabled = self._is_anthem_enabled.get()
        if SETTINGS.is_anthem_enabled:
            run_at = datetime.datetime.now().replace(**ANTHEM_TIME)
            if run_at < datetime.datetime.now():
                run_at += datetime.timedelta(days=1)
            delta = run_at - datetime.datetime.now()
            self._timer = self._parent.after(int(delta.total_seconds() * 1000), self._play)
        else:
            if self._timer is not None:
                self._parent.after_cancel(self._timer)
                self._timer = None

    def _play(self):
        if APP_STATE.SirenaNowPlaying:
            return
        print(datetime.datetime.now())
        pygame.mixer.music.stop()
        pygame.mixer.music.load(SILENCE_PATH)
        pygame.mixer.music.play()
        pygame.mixer.music.queue(ANTHEM_PATH)
        self._parent.after(61000, self._command)


class Autostart:
    def __init__(self, parent: SettingsFrame):
        self._parent = parent

        self._is_autostart_enabled = tk.BooleanVar(value=SETTINGS.autostart)
        auto_checkbutton = ttk.Checkbutton(parent.frame, variable=self._is_autostart_enabled, text="Автозапуск", command=self._command)
        auto_checkbutton.grid(row=9, column=0, sticky="W", padx=5)

    def _command(self):
        SETTINGS.autostart = self._is_autostart_enabled.get()
        if SETTINGS.autostart:
            autostart.enable()
        else:
            autostart.disable()


if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as err:
        logger.exception(err)
