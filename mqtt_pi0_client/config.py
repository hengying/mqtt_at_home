import time
import threading
import configparser


class SingletonType(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
        return cls._instance

class Config(metaclass=SingletonType):
    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config_file = "config.ini"
        self.__config.read(self.__config_file)

        self._has_ups_lite = int(self.__config.get('devices', 'ups_lite'))
        self._has_lcd_hat_1in3 = int(self.__config.get('devices', 'lcd_hat_1in3'))
        self._has_oled_hat_1in3 = int(self.__config.get('devices', 'oled_hat_1in3'))
        self._use_pygame = int(self.__config.get('devices', 'use_pygame'))
        self._use_mqtt = int(self.__config.get('devices', 'use_mqtt'))
        self._use_rgb_color = int(self.__config.get('devices', 'use_rgb_color'))

        self._pygame_win_width = int(self.__config.get('win', 'pygame_win_width'))
        self._pygame_win_height = int(self.__config.get('win', 'pygame_win_height'))
        self._screen_saver_wait_count = int(self.__config.get('win', 'screen_saver_wait_count'))

        self._server_addr = self.__config.get('server', 'addr')
        self._server_port = int(self.__config.get('server', 'port'))

        self._has_music_subsystem = int(self.__config.get('subsystem', 'music'))
        self._has_alarm_subsystem = int(self.__config.get('subsystem', 'alarm'))


    @property
    def has_ups_lite(self):
        return self._has_ups_lite

    @property
    def has_lcd_hat_1in3(self):
        return self._has_lcd_hat_1in3

    @property
    def has_oled_hat_1in3(self):
        return self._has_oled_hat_1in3

    @property
    def use_pygame(self):
        return self._use_pygame

    @property
    def use_mqtt(self):
        return self._use_mqtt

    @property
    def use_rgb_color(self):
        return self._use_rgb_color

    @property
    def pygame_win_width(self):
        return self._pygame_win_width

    @property
    def pygame_win_height(self):
        return self._pygame_win_height

    @property
    def server_addr(self):
        return self._server_addr

    @property
    def server_port(self):
        return self._server_port

    @property
    def has_music_subsystem(self):
        return self._has_music_subsystem

    @property
    def has_alarm_subsystem(self):
        return self._has_alarm_subsystem

    @property
    def screen_saver_wait_count(self):
        return self._screen_saver_wait_count
