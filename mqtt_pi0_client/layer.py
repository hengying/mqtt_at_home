
class Layer():
    def __init__(self, holder, name):
        self._holder = holder
        self._name = name

    def handle_event(self, event):
        pass

    def paint(self, image_draw):
        pass