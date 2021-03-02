
from subsystem import SubSystem
from list_control import ListControl
from event import *

class RootMenu(SubSystem):
    def __init__(self):
        super().__init__()

    @property
    def title(self):
        return '根菜单'

    def set_subsystems(self, subsystems_name_list):
        self._subsystems_name_list = subsystems_name_list

    def active(self, holder):
        super().active(holder)
        return ListControl(holder, self.title, self._subsystems_name_list)

    def handle_event(self, event):
        super().handle_event(event)
        if type(event) == ListItemSelected:
            if event.list_name == self.title:
                self._holder.add_event(ActiveSubsystem(self._subsystems_name_list[event.item_index]))
