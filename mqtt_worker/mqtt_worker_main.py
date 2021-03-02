import time

from config import Config

import paho.mqtt.client as mqtt

class App():
    def __init__(self):
        self._config = Config()
        self._workers = []
        self._music_players = []

        if self._config.has_music_worker:
            from music_worker import MusicWorker
            music_worker = MusicWorker(self)
            self._workers.append(music_worker)
            self._music_players.append(music_worker)

        if self._config.has_alarm_worker:
            from alarm_worker import AlarmWorker
            alarm_worker = AlarmWorker(self)
            self._workers.append(alarm_worker)
            self._music_players.append(alarm_worker)

        if self._config.has_print_worker:
            from print_worker import PrintWorker
            self._workers.append(PrintWorker(self))

        def call_back_on_connect(client, userdata, flags, rc):
            self.on_connect(client, userdata, flags, rc)

        def call_back_on_message(client, userdata, msg):
            self.on_message(client, userdata, msg)

        self._client = mqtt.Client()
        self._client.on_connect = call_back_on_connect
        self._client.on_message = call_back_on_message

    def run(self):
        try:
            self._client.connect(self._config.server_addr, self._config.server_port)
            self._client.loop_start()
            while(True):
                for worker in self._workers:
                    worker.update()
                time.sleep(1)
        except KeyboardInterrupt:
            self._client.loop_stop()
            self._client.disconnect()  # 关闭连接

    def on_connect(self, client, userdata, flags, rc):
        print("Connect result:{}".format(str(rc)))
        if rc == 0:
            for worker in self._workers:
                worker.on_connect(client, userdata, flags)

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))  # 打印主题和消息
        for worker in self._workers:
            worker.on_message(client, userdata, msg)

    def pause_music_players(self, except_me):
        for music_player in self._music_players:
            if music_player is not except_me:
                music_player.pause()

    def resume_music_players(self, except_me):
        for music_player in self._music_players:
            if music_player is not except_me:
                music_player.resume()

if "__main__" == __name__:
    app = App()
    app.run()



