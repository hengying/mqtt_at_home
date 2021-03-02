
import paho.mqtt.client as mqtt

from config import Config
from event import *

class MQTTClient():
    def __init__(self, event_queue):
        self._config = Config()
        self._event_queue = event_queue

        def call_back_on_connect(client, userdata, flags, rc):
            self.on_connect(client, userdata, flags, rc)

        def call_back_on_message(client, userdata, msg):
            self.on_message(client, userdata, msg)

        self._client = mqtt.Client()
        self._client.on_connect = call_back_on_connect
        self._client.on_message = call_back_on_message

        try:
            self._client.connect(self._config.server_addr, self._config.server_port)
            self._client.loop_start()
        except KeyboardInterrupt:
            self._client.loop_stop()
            self._client.disconnect()

    def run(self):
        try:
            self._client.connect(self._config.server_addr, self._config.server_port)
            self._client.loop_start()
        except KeyboardInterrupt:
            self._client.loop_stop()
            self._client.disconnect()  # 关闭连接

    def on_connect(self, client, userdata, flags, rc):
        print("Connect result:{}".format(str(rc)))
        if rc == 0:
            self._event_queue.put_nowait(ServerConnected(client))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))  # 打印主题和消息
        self._event_queue.put_nowait(MessageReceived(client, msg))
