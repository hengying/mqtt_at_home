
from subsystem import SubSystem
from event import *
from list_control import ListControl

ALARM_TOPIC_ROOT = 'home/alarm/'
ALARM_REPLY_TOPIC_SUBSCRIBE = ALARM_TOPIC_ROOT + '+/reply'
ALARM_LIST = '闹铃列表'
ALARM_ADD_HOUR_LIST = '小时列表'
ALARM_ADD_MINUTE_LIST = '分钟列表'
ALARM_OPT_LIST = '闹铃操作'

class AlarmSubSystem(SubSystem):
    def __init__(self):
        super().__init__()

    @property
    def title(self):
        return '闹铃'

    def active(self, holder):
        super().active(holder)
        return ListControl(holder, self.title,
                           ['闹铃列表', '添加闹铃', '停止闹铃'])

    def handle_event(self, event):
        super().handle_event(event)
        if type(event) == ServerConnected:
            print('server connect!')
            self._client = event.client
            self._client.subscribe(ALARM_REPLY_TOPIC_SUBSCRIBE)
        elif type(event) == MessageReceived:
            if event.msg.topic == ALARM_TOPIC_ROOT + 'list_alarm/reply':
                if self._holder is not None:
                    payload = event.msg.payload.decode('UTF-8')
                    print('alarm list: ', payload)
                    client_id, alarm_list_str = payload.split(':', 1)
                    if client_id == self._holder.client_id:
                        self._alarm_list = alarm_list_str.split(',')
                        self._alarm_list_ctrl = ListControl(self._holder, self.title + '/'+ ALARM_LIST,
                                   self._alarm_list)
                        # 子系统不在激活状态，不要弹出 layer!
                        if self._holder.is_actived(self.title):
                            self._holder.add_layer(self._alarm_list_ctrl)
        elif type(event) == ListItemSelected:
            if event.list_name == self.title:
                if event.item_index == 0:
                    self._client.publish(ALARM_TOPIC_ROOT + 'list_alarm', payload=self._holder.client_id, qos=1)
                elif event.item_index == 1:
                    hour_list = ['{:02d}:'.format(i) for i in range(24)]
                    hour_ctrl = ListControl(self._holder, self.title + '/' + ALARM_ADD_HOUR_LIST, hour_list)
                    self._holder.add_layer(hour_ctrl)
                elif event.item_index == 2:
                    self._client.publish(ALARM_TOPIC_ROOT + 'stop', payload='', qos=1)
            elif event.list_name == self.title + '/'+ ALARM_LIST:
                alarm = self._alarm_list[event.item_index]
                if alarm == '':
                    return
                alarm_opt_list = []
                if len(alarm) > 5:
                    self._current_alarm_enabled = False
                    alarm_opt_list = ['启用', '删除']
                else:
                    self._current_alarm_enabled = True
                    alarm_opt_list = ['停用', '删除']
                self._current_alarm = alarm[:5]
                alarm_opt_ctrl = ListControl(self._holder, self.title + '/' + ALARM_OPT_LIST, alarm_opt_list)
                self._holder.add_layer(alarm_opt_ctrl)
            elif event.list_name == self.title + '/' + ALARM_ADD_HOUR_LIST:
                self._alarm_hour = event.item_index
                minute_list = ['{:02d}:{:02d}'.format(self._alarm_hour, i) for i in range(0, 60, 5)]
                minute_ctrl = ListControl(self._holder, self.title + '/' + ALARM_ADD_MINUTE_LIST, minute_list)
                self._holder.add_layer(minute_ctrl)
            elif event.list_name == self.title + '/' + ALARM_ADD_MINUTE_LIST:
                self._alarm_minute = event.item_index * 5
                self._client.publish(ALARM_TOPIC_ROOT + 'add',
                                     payload='{:02d}:{:02d}'.format(self._alarm_hour, self._alarm_minute), qos=1)
                self._client.publish(ALARM_TOPIC_ROOT + 'list_alarm', payload=self._holder.client_id, qos=1)
                self._holder.add_event(PopLayer(2))
            elif event.list_name == self.title + '/' + ALARM_OPT_LIST:
                if event.item_index == 0:
                    if self._current_alarm_enabled:
                        self._client.publish(ALARM_TOPIC_ROOT + 'disable', payload=self._current_alarm, qos=1)
                    else:
                        self._client.publish(ALARM_TOPIC_ROOT + 'enable', payload=self._current_alarm, qos=1)
                elif event.item_index == 1:
                    self._client.publish(ALARM_TOPIC_ROOT + 'delete', payload=self._current_alarm, qos=1)
                self._holder.add_event(PopLayer(2))
                # 如果 delete qos 为2，list_alarm qos为1，则list_alarm会在删除前返回，
                # 导致显示不正确。暂时都设置为 qos=1。
                self._client.publish(ALARM_TOPIC_ROOT + 'list_alarm', payload=self._holder.client_id, qos=1)
        if type(event) == ListBack:
            if event.list_name == self.title:
                self._holder.add_event(PopLayer(1))
            elif event.list_name == self.title + '/'+ ALARM_LIST:
                self._holder.add_event(PopLayer(1))
            elif event.list_name == self.title + '/'+ ALARM_ADD_HOUR_LIST:
                self._holder.add_event(PopLayer(1))
            elif event.list_name == self.title + '/'+ ALARM_ADD_MINUTE_LIST:
                self._holder.add_event(PopLayer(1))
            elif event.list_name == self.title + '/'+ ALARM_OPT_LIST:
                self._holder.add_event(PopLayer(1))
