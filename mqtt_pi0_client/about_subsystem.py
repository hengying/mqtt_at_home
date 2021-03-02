import time
from subsystem import SubSystem
from config import Config
from list_control import ListControl
from event import *

class AboutSubsystem(SubSystem):
    def __init__(self):
        super().__init__()
        self._config = Config()
        self._voltage = 0
        self._capacity = 100

    @property
    def title(self):
        return '系统'

    def active(self, holder):
        super().active(holder)


        if self._config.has_ups_lite:
            self._list = ['电池电压:{:.2f}V'.format(self._voltage),
                          '电池容量:{:.0f}%'.format(self._capacity),
                          'hengying', '2021/1', '关机']
            return ListControl(holder, self.title, self._list)
        else:
            self._list = ['hengying', '2021/1', '关机']
            return ListControl(holder, self.title, self._list)

    def handle_event(self, event):
        super().handle_event(event)
        if type(event) == PowerEvent:
            self._voltage = event.voltage
            self._capacity = event.capacity
        elif type(event) == ListItemSelected:
            if event.list_name == self.title:
                if event.item_index == len(self._list) - 1:
                    print('Shutting down...')
                    self._holder.show_message('正在关机...')
                    time.sleep(3)
                    self._holder.system_shutdown()
        if type(event) == ListBack:
            if event.list_name == self.title:
                self._holder.add_event(PopLayer(1))

