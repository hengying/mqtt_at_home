
from subsystem import SubSystem
from event import *
from list_control import ListControl

MUSIC_TOPIC_ROOT = 'home/music/'
MUSIC_REPLY_TOPIC_SUBSCRIBE = MUSIC_TOPIC_ROOT + '+/reply'
MUSIC_LIST = '音乐列表'

class MusicSubSystem(SubSystem):
    def __init__(self):
        super().__init__()

    @property
    def title(self):
        return '音乐'

    def active(self, holder):
        super().active(holder)
        return ListControl(holder, self.title,
                           ['随机播放一首', '音乐列表', '停止'])

    def handle_event(self, event):
        super().handle_event(event)
        if type(event) == ServerConnected:
            print('server connect!')
            self._client = event.client
            self._client.subscribe(MUSIC_REPLY_TOPIC_SUBSCRIBE)
        elif type(event) == MessageReceived:
            if event.msg.topic == MUSIC_TOPIC_ROOT + 'list_music/reply':
                if self._holder is not None:
                    payload = event.msg.payload.decode('UTF-8')
                    print('music list: ', payload)
                    client_id, music_list_str = payload.split(':', 1)
                    if client_id == self._holder.client_id:
                        self._music_list = music_list_str.split(',')
                        self._music_list_ctrl = ListControl(self._holder, self.title + '/'+ MUSIC_LIST,
                                   self._music_list)
                        # 子系统不在激活状态，不要弹出 layer!
                        if self._holder.is_actived(self.title):
                            self._holder.add_layer(self._music_list_ctrl)
        elif type(event) == ListItemSelected:
            if event.list_name == self.title:
                if event.item_index == 0:
                    self._client.publish(MUSIC_TOPIC_ROOT + 'play_random_one', payload='', qos=1)
                elif event.item_index == 1:
                    self._client.publish(MUSIC_TOPIC_ROOT + 'list_music', payload=self._holder.client_id, qos=1)
                elif event.item_index == 2:
                    self._client.publish(MUSIC_TOPIC_ROOT + 'stop', payload='', qos=1)
            elif event.list_name == self.title + '/'+ MUSIC_LIST:
                music_name = self._music_list[event.item_index]
                self._client.publish(MUSIC_TOPIC_ROOT + 'play', payload=music_name, qos=1)
        if type(event) == ListBack:
            if event.list_name == self.title:
                self._holder.add_event(PopLayer(1))
            elif event.list_name == self.title + '/'+ MUSIC_LIST:
                self._holder.add_event(PopLayer(1))
