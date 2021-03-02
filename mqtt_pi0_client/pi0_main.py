import os
import time
from queue import Queue
from PIL import Image, ImageDraw, ImageFont
from button_enum import ButtonType
from event import *
from config import Config

ROW_HEIGHT = 16

class App():
    def __init__(self):
        self._input_devices = []
        self._subsystems = []
        self._layers = []
        self._event_queue = Queue()
        self._config = Config()

        self._background_color = 'BLACK'
        self._foreground_color = 'WHITE'

        self.__init_devices()
        self.__init_subsystems()

        self._width = self._display.width
        self._height = self._display.height
        self._row_count = self._height // self.row_height

        self.__init_paint_system()
        self.__active_subsystem(self._root_menu.title)

        self._client_id = str(time.time())
        self._need_refresh = True
        self._no_user_input_count = 0
        self._in_screen_saving_mode = False

    def __init_devices(self):
        if self._config.has_ups_lite:
            from UPS_Lite import UPSLite
            self._upslite = UPSLite()
            self._input_devices.append(self._upslite)

        if self._config.has_lcd_hat_1in3:
            from lcd_hat_1in3 import LCDHat
            self._display = LCDHat()
            self._input_devices.append(self._display)

        if self._config.has_oled_hat_1in3:
            from oled_hat_1in3 import OLEDHat
            self._display = OLEDHat()
            self._input_devices.append(self._display)
            self._background_color = 255    # 黑白颠倒
            self._foreground_color = 0

        if self._config.use_pygame:
            from desktop_win import DesktopWin
            self._display = DesktopWin()
            self._input_devices.append(self._display)

        if self._config.use_mqtt:
            from mqtt_client import MQTTClient
            self._mqtt_client = MQTTClient(self._event_queue)

    def __init_subsystems(self):
        from root_menu import RootMenu
        self._root_menu = RootMenu()
        self._subsystems.append(self._root_menu)

        if self._config.has_music_subsystem:
            from music_subsystem import MusicSubSystem
            self._subsystems.append(MusicSubSystem())

        if self._config.has_alarm_subsystem:
            from alarm_subsystem import AlarmSubSystem
            self._subsystems.append(AlarmSubSystem())

        from about_subsystem import AboutSubsystem
        self._subsystems.append(AboutSubsystem())

        subsystem_name_list = [s.title for s in self._subsystems[1:]]
        self._root_menu.set_subsystems(subsystem_name_list)

    def __init_paint_system(self):
        if self._config.use_rgb_color:
            self.__image = Image.new('RGB', (self._width, self._height))
        else:
            self.__image = Image.new('1', (self._width, self._height))
        self.__image_draw = ImageDraw.Draw(self.__image)
        self.__font16 = ImageFont.truetype("fonts/uni_dzh.ttf", 16)

    def __active_subsystem(self, subsystem_name):
        for subsystem in self._subsystems:
            if subsystem.title == subsystem_name:
                self._layers.append(subsystem.active(self))
                self._need_refresh = True
        self._active_subsystem = subsystem_name

    def is_actived(self, subsystem_name):
        return self._active_subsystem == subsystem_name

    def system_shutdown(self):
        os.system('sudo halt')
        time.sleep(100)

    @property
    def font16(self):
        return self.__font16

    @property
    def width(self):
        return self._width

    @property
    def row_height(self):
        return ROW_HEIGHT

    @property
    def row_count(self):
        return self._row_count

    @property
    def height(self):
        return self._height

    @property
    def client_id(self):
        return self._client_id

    @property
    def background_color(self):
        return self._background_color

    @property
    def foreground_color(self):
        return self._foreground_color

    def refresh_win(self):
        self._event_queue.put_nowait(RefreshWinEvent())

    def add_event(self, event):
        self._event_queue.put_nowait(event)

    def add_layer(self, layer):
        self._layers.append(layer)
        self._need_refresh = True

    def show_message(self, str):
        BIAS_Y = -2
        self.__image_draw.rectangle((0, 0, self._width, self._height), outline=self.background_color,
                                    fill=self.background_color)
        self.__image_draw.text((0, int(self.row_height * 1.5) + BIAS_Y), str,
                        font=self.font16, fill=self.foreground_color)
        self._display.display(self.__image)

    def run(self):
        while True:
            display_need_refresh = False

            for input_device in self._input_devices:
                input_device.update(self._event_queue)

            self._no_user_input_count += 1

            while not self._event_queue.empty():
                event = self._event_queue.get_nowait()

                if is_user_input(event):
                    if self._in_screen_saving_mode == True:
                        self._in_screen_saving_mode = False;
                        self._need_refresh = True
                        self._no_user_input_count = 0
                        # ignore this input event
                        continue;
                    self._need_refresh = True
                    self._no_user_input_count = 0

                if type(event) == PowerLowEvent:
                    print('System shut down!')
                    self.system_shutdown()
                    return
                elif type(event) == QuitEvent:
                    print('Quiting!')
                    return
                elif type(event) == PopLayer:
                    count = event.count
                    if count > len(self._layers):
                        count = len(self._layers) - 1
                    for i in range(count):
                        self._layers.pop()
                    if len(self._layers) == 1:
                        self._active_subsystem = self._root_menu.title
                    self._need_refresh = True
                elif type(event) == ActiveSubsystem:
                    self.__active_subsystem(event.subsystem_name)
                else:
                    for subsystem in self._subsystems:
                        subsystem.handle_event(event)

                    self._layers[-1].handle_event(event)

            if self._need_refresh:
                if self._in_screen_saving_mode == False:
                    print('refresh screen...')
                    self.__image_draw.rectangle((0, 0, self._width, self._height), outline=self.background_color, fill=self.background_color)
                    self._layers[-1].paint(self.__image_draw)
                    self._display.display(self.__image)
                self._need_refresh = False

            if self._no_user_input_count > self._config.screen_saver_wait_count:
                if self._in_screen_saving_mode == False:
                    print('screen saving mode...')
                    self._in_screen_saving_mode = True
                    self.__image_draw.rectangle((0, 0, self._width, self._height), outline=self.background_color, fill=self.background_color)
                    self._display.display(self.__image)

            if self._in_screen_saving_mode == True:
                time.sleep(1/10.0)
            else:
                time.sleep(1/60.0)

try:
    app = App()
    app.run()
except IOError as e:
    print(e)
except KeyboardInterrupt:
    print("ctrl + c:")
    exit()
