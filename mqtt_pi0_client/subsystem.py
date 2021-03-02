
class SubSystem():
    def __init__(self):
        self._holder = None

    @property
    def title(self):
        return '子系统'

    def active(self, holder):
        self._holder = holder

    def handle_event(self, event):
        pass

