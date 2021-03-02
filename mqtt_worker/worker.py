
class Worker():
    def __init__(self, holder):
        self._holder = holder

    def on_connect(self, client, userdata, flags):
        pass

    def on_message(self, client, userdata, msg):
        pass

    def update(self):
        pass