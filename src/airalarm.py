import datetime
import logging.handlers
import tkinter as tk
import tkinter.font as tkfont

import pygame
import ttkbootstrap as ttk
from urllib3.exceptions import MaxRetryError

import autostart
from settings import (
    ICONS_PATH,
    START_PATH,
    END_PATH,
    SILENCE_PATH,
    ANTHEM_PATH,
    ANTHEM_TIME,
    NETWORK_ERROR,
    FONT_FAMILY,
    LOGS,
)
from providers import get_active_alarm_start_at, WAIT_MS
from regions import REGIONS
from storage import State
from config import CONFIG

LOGS.mkdir(parents=True, exist_ok=True)
LOG_FILENAME = LOGS / 'airalarm.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

APP_NAME = 'Повітряна тривога'
APP_STATE = State()


class App:
    def __init__(self):
        pygame.mixer.init()

        self.window = tk.Tk()
        self.window.title(APP_NAME)
        self.window.resizable(width=False, height=False)
        self.window.geometry('443x400')
        self.window.wm_iconphoto(True, *(tk.PhotoImage(file=path) for path in ICONS_PATH.iterdir()))
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        default_font = tkfont.nametofont('TkDefaultFont')
        default_font.configure(family=FONT_FAMILY)

        self.style = ttk.Style()
        self.style.theme_use('superhero')
        self.style.configure('TButton', font=(FONT_FAMILY, 10))

        AnthemPlayer(self)

        Body(self)

    def mainloop(self):
        self.window.mainloop()
    
    def after(self, ms, func=None, *args):
        return self.window.after(ms, func=func, *args)


class Body:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.window)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW, padx=8, pady=8)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        Main(self)
        Footer(self)

    def after(self, ms, func=None, *args):
        return self.app.after(ms, func=func, *args)


class Main:
    def __init__(self, body):
        self.body = body
        self.frame = ttk.Frame(body.frame)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.status_page = StatusPage(self)
        self.search_page = SearchPage(self)

        self.init()

    def init(self):
        if CONFIG.region_id:
            region = REGIONS.get(CONFIG.region_id)
            self.status_page.on_region_selected(region)
        else:
            self.search_page.show()

    def after(self, ms, func=None, *args):
        return self.body.after(ms, func=func, *args)


class EmptyPage:
    def __init__(self, main):
        self.main = main

        self.frame = ttk.Frame(main.frame)
        self.frame.grid_columnconfigure(0, weight=1)

        self._error = Error(self)

    def on_error(self, error):
        self._error.on_error(error)
        self._error.label.grid(row=0, column=0, sticky=tk.EW)
        self.frame.grid(row=0, column=0, sticky=ttk.NSEW)

    def hide(self):
        self.frame.grid_remove()


class Error:
    def __init__(self, page):
        self.page = page
        self.label = ttk.Label(page.frame, text='some', bootstyle='inverse-danger', padding=10)

    def on_error(self, error):
        self.label.config(text=error)

    def hide(self):
        self.label.grid_remove()


class StatusPage:
    def __init__(self, main: Main):
        self.main = main

        self.frame = ttk.Frame(main.frame, padding=(0, 4))
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        self._error = Error(self)
        self._region_selected = RegionSelected(self)
        self._alert_status = AlertStatus(self)
        self._preferences = Preferences(self)

    def on_region_selected(self, region):
        self._alert_status.enable()
        self._region_selected.set(region['name'])
        self.frame.grid(row=0, column=0, sticky=ttk.NSEW)

    def on_restore(self):
        self._error.hide()
        self._alert_status.show()

    def on_change_button_clicked(self):
        self._alert_status.disable()
        self.frame.grid_remove()
        self.main.search_page.show()

    def on_error(self, error):
        self._alert_status.hide()
        self._error.on_error(error)
        self._error.label.grid(row=1, column=0, sticky=ttk.EW)


class RegionSelected:
    def __init__(self, page):
        self.page = page

        self.frame = ttk.Frame(page.frame, padding=(16, 0))
        self.frame.grid(row=0, column=0, sticky=ttk.NSEW)
        self.frame.grid_columnconfigure(0, weight=1)

        self._change_button = ttk.Button(
            self.frame,
            text='Змінити',
            command=self._on_click,
            bootstyle='secondary',
        )
        self._change_button.grid(row=1, column=0)

        self._region_label = ttk.Label(
            self.frame,
            anchor=ttk.CENTER,
            wraplength=395,
            text='',
            font=(FONT_FAMILY, 13),
            justify=ttk.CENTER,
        )
        self._region_label.grid(row=0, column=0, sticky=ttk.EW, pady=(0, 4))

    def _on_click(self):
        self.page.on_change_button_clicked()

    def set(self, text):
        self._region_label.configure(text=text)


class Preferences:
    def __init__(self, page: StatusPage):
        self.page = page

        self.frame = ttk.Frame(self.page.frame)
        self.frame.grid(row=2, column=0, sticky=ttk.EW)
        self.frame.grid_columnconfigure(0, weight=1)
        self.label_frame = ttk.LabelFrame(self.frame, text='Налаштування', padding=16)
        self.label_frame.grid(row=0, column=0, sticky=ttk.NSEW)
        self.label_frame.rowconfigure(0, weight=1, pad=16)
        self.label_frame.rowconfigure(1, weight=1, pad=16)
        self.label_frame.rowconfigure(2, weight=1, pad=16)

        TimePicker(self.label_frame)
        AnthemSetting(self)
        Autostart(self)

    def after(self, ms, func=None, *args):
        return self.page.main.after(ms, func=func, *args)


class TimePicker:
    def __init__(self, parent: ttk.LabelFrame):
        notification_label = ttk.Label(
            parent,
            text='Тривалість оголошення:',
        )
        notification_label.grid(row=0, column=0, sticky=ttk.E)

        validate_command = parent.register(self._validate)

        self._spinbox = ttk.Spinbox(
            parent,
            width=2,
            from_=1,
            to=99,
            state='readonly',
            validate='all',
            validatecommand=(validate_command, '%P'),
        )
        self._spinbox.set(str(CONFIG.time))
        self._spinbox.grid(row=0, column=1, sticky=ttk.W, padx=(8, 0))

        minutes_label = ttk.Label(
            parent,
            text=' хв',
        )
        minutes_label.grid(row=0, column=2, sticky=ttk.W)

    def _validate(self, newval):
        CONFIG.time = int(newval)


class AlertStatus:
    def __init__(self, page):
        self.page = page

        self.frame = ttk.Frame(self.page.frame)
        self.frame.grid_columnconfigure(0, weight=1)

        self._label = ttk.Label(
            self.frame,
            text='',
            font=(FONT_FAMILY, 25, 'bold'),
            justify=ttk.CENTER,
        )
        self._label.grid(row=3, column=0)

        self._icon = ttk.Label(
            self.frame,
            text='',
            font=(FONT_FAMILY, 55, 'bold'),
            justify=ttk.CENTER,
        )
        self._icon.grid(row=2, column=0)
        
        self._start_notification_sound = pygame.mixer.Sound(START_PATH)
        self._end_notification_sound = pygame.mixer.Sound(END_PATH)

        self.show()
    
    def enable(self):
        APP_STATE.__init__()
        APP_STATE.alarmNotification = True
        self.Refresh()

    def disable(self):
        pygame.mixer.stop()
        APP_STATE.alarmNotification = False

    def Refresh(self):
        try:
            if APP_STATE.alarmNotification:
                start_at = get_active_alarm_start_at(CONFIG.region_id)
                self.page.on_restore()
                logger.debug('Are authorities signalling about air alarm now: %s', start_at)
                logger.debug('Has siren played already: %s', APP_STATE.SirenaPlayed)
                logger.debug('Is siren playing now: %s', APP_STATE.SirenaNowPlaying)
                if start_at is None:
                    self._on_notification_end()
                    self._start_notification_sound.stop()
                    if APP_STATE.SirenaPlayed and not pygame.mixer.music.get_busy():  # Відбій
                        length = self._end_notification_sound.get_length()
                        self._end_notification_sound.play(loops=1)
                        APP_STATE.SirenaPlayed = False
                        APP_STATE.SirenaNowPlaying = True
                        APP_STATE.end = datetime.datetime.now() + datetime.timedelta(seconds=length)
                else:
                    end_play_at = start_at + datetime.timedelta(minutes=CONFIG.time)
                    if end_play_at < datetime.datetime.now(datetime.UTC):
                        APP_STATE.SirenaPlayed = True
                        self._on_notification_start()
                    if not APP_STATE.SirenaPlayed:  # Тривога
                        seconds = CONFIG.time * 60
                        pygame.mixer.music.stop()
                        self._end_notification_sound.stop()
                        self._start_notification_sound.play(loops=-1, maxtime=seconds * 1000, fade_ms=5 * 1000)
                        APP_STATE.SirenaPlayed = True
                        self._on_notification_start()
                        APP_STATE.SirenaNowPlaying = True
                        APP_STATE.end = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            else:
                return
        except MaxRetryError:
            self._on_error(NETWORK_ERROR)
        except Exception as err:
            logger.exception(err)
        if APP_STATE.SirenaNowPlaying and datetime.datetime.now() > APP_STATE.end:
            APP_STATE.SirenaNowPlaying = False
        self.page.main.after(WAIT_MS, self.Refresh)

    def _on_notification_start(self):
        self._label.config(text='Тривога')
        self._icon.config(text='⚠', bootstyle='danger')

    def _on_notification_end(self):
        self._label.config(text='Немає тривоги')
        self._icon.config(text='✓', bootstyle='info')

    def _on_error(self, error):
        self.page.on_error(error)

    def show(self):
        self.frame.grid(row=1, column=0, sticky=ttk.NSEW)

    def hide(self):
        self.frame.grid_remove()


class AnthemSetting:
    def __init__(self, parent: Preferences):
        self._parent = parent

        self._is_anthem_enabled = ttk.BooleanVar(value=CONFIG.is_anthem_enabled)
        self._is_anthem_enabled.set(CONFIG.is_anthem_enabled)
        label = ttk.Label(
            self._parent.label_frame,
            text='Хвилина мовчання і гімн України',
        )
        label.grid(row=1, column=0, sticky=ttk.E)
        checkbutton = ttk.Checkbutton(
            self._parent.label_frame,
            variable=self._is_anthem_enabled,
            command=self._command,
            bootstyle='rounded-toggle',
        )
        checkbutton.grid(row=1, column=1, sticky=ttk.W, padx=8)

    def _command(self):
        CONFIG.is_anthem_enabled = self._is_anthem_enabled.get()


class AnthemPlayer:
    def __init__(self, app: App):
        self.app = app
        self._init()

    def _init(self):
        run_at = datetime.datetime.now().replace(**ANTHEM_TIME)
        if run_at < datetime.datetime.now():
            run_at += datetime.timedelta(days=1)
        delta = run_at - datetime.datetime.now()
        self.app.after(int(delta.total_seconds() * 1000), self._play)

    def _play(self):
        if APP_STATE.SirenaNowPlaying:
            return
        if not CONFIG.is_anthem_enabled:
            return
        pygame.mixer.music.load(SILENCE_PATH)
        pygame.mixer.music.play()
        pygame.mixer.music.queue(ANTHEM_PATH)
        self._init()


class Autostart:
    def __init__(self, parent: Preferences):
        self._parent = parent

        self._is_autostart_enabled = ttk.BooleanVar(value=autostart.is_enabled())
        label = ttk.Label(
            parent.label_frame,
            text='Автозапуск',
        )
        label.grid(row=2, column=0, sticky=ttk.E)
        auto_checkbutton = ttk.Checkbutton(
            parent.label_frame,
            variable=self._is_autostart_enabled,
            command=self._command,
            bootstyle='rounded-toggle',
        )
        auto_checkbutton.grid(row=2, column=1, sticky=ttk.W, padx=8)

    def _command(self):
        if self._is_autostart_enabled.get():
            autostart.enable()
        else:
            autostart.disable()


class SearchPage:
    def __init__(self, main):
        self.main = main

        self.frame = ttk.Frame(main.frame, padding=3)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self._search_field = SearchField(self)
        self._found_field = FoundField(self)

    def show(self):
        self._search_field.init()
        self._found_field.init()

        self.frame.grid(row=0, column=0, sticky=ttk.NSEW)

    def on_search_changed(self, text):
        self._found_field.update(REGIONS.filter(text))

    def on_region_selected(self, region):
        CONFIG.region_id = region['id']
        self.frame.grid_remove()
        self.main.status_page.on_region_selected(region)

    def after(self, ms, func=None, *args):
        return self.main.after(ms, func=func, *args)

    def after_cancel(self, timer):
        self.main.after_cancel(timer)


class SearchField:
    def __init__(self, page):
        self.page = page
        self.foreground = page.main.body.app.style.configure('TEntry')['foreground']

        self._search_entry = ttk.Entry(page.frame, font=(FONT_FAMILY, 16))
        self._search_entry.grid(row=0, column=0, sticky=ttk.EW)
        self._search_entry.bind('<KeyRelease>', self._on_key_release)
        self._search_entry.bind('<FocusIn>', self._on_focus_in)

        self._placeholder_text = 'Пошук'

    def init(self):
        self._show_placeholder()

    def _show_placeholder(self):
        self._search_entry.delete(0, ttk.END)
        self._search_entry.insert(0, self._placeholder_text)
        self._search_entry.configure(foreground='grey')

    def _on_focus_in(self, event):
        self._hide_placeholder()

    def _hide_placeholder(self):
        self._search_entry.delete(0, ttk.END)
        self._search_entry.configure(foreground=self.foreground)

    def _on_key_release(self, event):
        self._on_search_changed()

    def _on_search_changed(self):
        text = self._get_search_text().lower()
        self.page.on_search_changed(text)

    def _get_search_text(self):
        return self._search_entry.get().strip()


class FoundField:
    def __init__(self, page):
        self.page = page

        self._listbox_frame = ttk.Frame(page.frame)
        self._listbox_frame.grid(row=1, column=0)
        self._listbox = ttk.Text(
            self._listbox_frame,
            height=19,
            width=50,
            cursor='hand2',
            state=ttk.DISABLED,
        )
        scrollbar = ttk.Scrollbar(self._listbox_frame, orient=ttk.VERTICAL, command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=scrollbar.set)

        self._listbox.grid(row=0, column=0, sticky=ttk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=ttk.NSEW)

        self._listbox.tag_configure('grey', foreground='#888888', font=(FONT_FAMILY, 10))

        self._listbox.bind('<Button-1>', self._on_text_click)

        self._selected_line = -1

        self._filtered_regions = []

    def init(self):
        self._filtered_regions = REGIONS.filter('')
        self._update_listbox()

    def _on_text_click(self, event):
        line_num = int(self._listbox.index(ttk.CURRENT).split('.')[0])
        region_index = self._get_region_index_from_line(line_num)
        if region_index >= 0:
            self._select_region(region_index)

    def _get_region_index_from_line(self, line_num):
        current_line = 1
        for i, region in enumerate(self._filtered_regions[:20]):
            lines_count = len(region['display'].split('\n'))
            if current_line <= line_num <= current_line + lines_count - 1:
                return i
            current_line += lines_count + 1  # +1 for the separator
        return -1

    def _select_first_result(self):
        if self._filtered_regions:
            self._select_region(0)

    def _select_region(self, index):
        if 0 <= index < len(self._filtered_regions):
            region = self._filtered_regions[index]
            self.page.on_region_selected(region)

    def update(self, regions):
        self._filtered_regions = regions
        self._update_listbox()

    def _update_listbox(self):
        self._listbox.config(state=ttk.NORMAL)
        self._listbox.delete("1.0", ttk.END)

        for i, region in enumerate(self._filtered_regions[:20]):  # Limit to 20 results
            lines = region['display'].split('\n')

            # Insert main region name (first line) in normal color
            self._listbox.insert(ttk.END, lines[0])

            # Insert parent regions (remaining lines) in grey
            for line in lines[1:]:
                self._listbox.insert(ttk.END, f'\n{line}', 'grey')

            # Add separator between regions
            if i < len(self._filtered_regions[:20]) - 1:
                self._listbox.insert(ttk.END, '\n\n')

        self._listbox.config(state=ttk.DISABLED)


class Footer:
    def __init__(self, body):
        self.frame = ttk.Frame(body.frame)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid(row=1, column=0, sticky=ttk.NSEW, pady=(4, 0))
        copyright_label = ttk.Label(self.frame, text='© 2025 zd4school – Ліцензія MIT')
        copyright_label.grid(row=1, column=0, sticky=ttk.W)
        version = ttk.Label(self.frame, text='Версія 1.0.0')
        version.grid(row=1, column=1, sticky=ttk.E)


if __name__ == '__main__':
    try:
        App().mainloop()
    except Exception as err:
        logger.exception(err)
