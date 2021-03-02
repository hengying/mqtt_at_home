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

        self._server_addr = self.__config.get('server', 'addr')
        self._server_port = int(self.__config.get('server', 'port'))

        self._mp3_folder = self.__config.get('local', 'mp3_folder')
        self._alarm_mp3_folder = self.__config.get('local', 'alarm_mp3_folder')

        self._has_music_worker = int(self.__config.get('workers', 'music'))
        self._has_alarm_worker = int(self.__config.get('workers', 'alarm'))
        self._has_print_worker = int(self.__config.get('workers', 'print'))

    @property
    def server_addr(self):
        return self._server_addr

    @property
    def server_port(self):
        return self._server_port

    @property
    def mp3_folder(self):
        return self._mp3_folder

    @property
    def alarm_mp3_folder(self):
        return self._alarm_mp3_folder

    @property
    def has_music_worker(self):
        return self._has_music_worker

    @property
    def has_alarm_worker(self):
        return self._has_alarm_worker

    @property
    def has_print_worker(self):
        return self._has_print_worker

