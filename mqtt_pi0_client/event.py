
class Event():
    def __init__(self):
        pass

class ButtonDownEvent(Event):
    def __init__(self, button_type):
        super().__init__()
        self._button_type = button_type

    @property
    def button_type(self):
        return self._button_type

class ButtonUpEvent(Event):
    def __init__(self, button_type):
        super().__init__()
        self._button_type = button_type

    @property
    def button_type(self):
        return self._button_type

class PowerEvent(Event):
    def __init__(self, voltage, capacity):
        super().__init__()
        self._voltage = voltage
        self._capacity = capacity

    @property
    def voltage(self):
        return self._voltage

    @property
    def capacity(self):
        return self._capacity

class PowerLowEvent(PowerEvent):
    def __init__(self, voltage, capacity):
        super().__init__(self, voltage, capacity)

class QuitEvent(Event):
    pass

class RefreshWinEvent(Event):
    pass

class ServerConnected(Event):
    def __init__(self, client):
        super().__init__()
        self._client = client

    @property
    def client(self):
        return self._client

class MessageReceived(Event):
    def __init__(self, client, msg):
        super().__init__()
        self._client = client
        self._msg = msg

    @property
    def client(self):
        return self._client

    @property
    def msg(self):
        return self._msg

class ListItemSelected(Event):
    def __init__(self, list_name, item_index):
        super().__init__()
        self._list_name = list_name
        self._item_index = item_index

    @property
    def list_name(self):
        return self._list_name

    @property
    def item_index(self):
        return self._item_index

class ListBack(Event):
    def __init__(self, list_name):
        super().__init__()
        self._list_name = list_name

    @property
    def list_name(self):
        return self._list_name

class PopLayer(Event):
    def __init__(self, count):
        super().__init__()
        self._count = count

    @property
    def count(self):
        return self._count

class ActiveSubsystem(Event):
    def __init__(self, subsystem_name):
        super().__init__()
        self._subsystem_name = subsystem_name

    @property
    def subsystem_name(self):
        return self._subsystem_name

def is_user_input(event):
    return type(event) == ButtonDownEvent or type(event) == ButtonUpEvent
