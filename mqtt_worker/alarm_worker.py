import os
import glob
import random
import pickle
import re
from datetime import datetime

from config import Config
from worker import Worker
from music_player import MusicPlayer

ALARM_TOPIC_ROOT = 'home/alarm/'
ALARM_TOPIC_SUBSCRIBE = ALARM_TOPIC_ROOT + '+'
ALARM_MP3 = 'mp3/try.mp3'
ALARM_SAVE_FILE = 'alarm.cfg'

class Alarm():
    def __init__(self, alarm_time, enabled = True):
        self._alarm_time = alarm_time
        self._enabled = enabled

    @property
    def alarm_time(self):
        return self._alarm_time

    @property
    def enabled(self):
        return self._enabled

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

class AlarmWorker(Worker):
    def __init__(self, holder):
        super().__init__(holder)
        self._config = Config()
        self._player = MusicPlayer()
        self._load_alarms()
        self._time_pattern = re.compile('^([012]\d):(\d\d)$')
        self._old_time_str = ''
        self._alarm_is_playing = False

    def on_connect(self, client, userdata, flags):
        super().on_connect(client, userdata, flags)
        client.subscribe(ALARM_TOPIC_SUBSCRIBE)

    def on_message(self, client, userdata, msg):
        super().on_message(client, userdata, msg)

        payload = msg.payload.decode('UTF-8')

        if msg.topic.startswith(ALARM_TOPIC_ROOT):
            command = msg.topic.rsplit("/", 1)[-1]
            if command == 'add':
                alarm_time = payload
                if alarm_time != '':
                    rst = self._time_pattern.match(alarm_time)
                    if rst is not None:
                        hour = int(rst.group(1))
                        minute = int(rst.group(2))
                        if hour < 24 and minute < 60:
                            alarm = self._find_alarm(alarm_time)
                            if alarm is None:
                                self._alarms.append(Alarm(alarm_time))
                            else:
                                alarm.enable()
                            self._save_alarms()
            elif command == 'stop':
                self._stop_alarm()
            elif command == 'delete':
                alarm_time = payload
                alarm = self._find_alarm(alarm_time)
                if alarm is not None:
                    self._alarms.remove(alarm)
                    print('delete:', self._alarms)
                    client.publish(msg.topic + '/reply', payload='ok', qos=1)
                    self._save_alarms()
                else:
                    client.publish(msg.topic + '/reply', payload='Alarm not exist!', qos=1)
            elif command == 'enable':
                alarm_time = payload
                alarm = self._find_alarm(alarm_time)
                if alarm is not None:
                    alarm.enable()
                    client.publish(msg.topic + '/reply', payload='ok', qos=1)
                    self._save_alarms()
                else:
                    client.publish(msg.topic + '/reply', payload='Alarm not exist!', qos=1)
            elif command == 'disable':
                alarm_time = payload
                alarm = self._find_alarm(alarm_time)
                if alarm is not None:
                    alarm.disable()
                    client.publish(msg.topic + '/reply', payload='ok', qos=1)
                    self._save_alarms()
                else:
                    client.publish(msg.topic + '/reply', payload='Alarm not exist!', qos=1)
            elif command == 'list_alarm':
                alarm_list = self._get_alarm_list()
                print('list:', '{}:{}'.format(payload, ','.join(alarm_list)))

                client.publish(msg.topic + '/reply',
                               payload='{}:{}'.format(payload, ','.join(alarm_list)), qos=1, retain=True)
            elif command == 'alarm_at_once':
                self._play_alarm()

    def _play_alarm(self):
        #self._stop_alarm()
        self._holder.pause_music_players(self)
        mp3_list = self._get_alarm_mp3_list()
        mp3_file = random.choice(mp3_list)
        print('Playing: {}'.format(mp3_file))
        self._player.play(mp3_file)
        # 好像这个音量被 music_worker 干扰了
        # 设置不起作用，get_volume 返回 -1！
        #self._player.set_volume(100)
        #print('Alarm volume:', self._player.get_volume())
        self._alarm_is_playing = True

    def _stop_alarm(self):
        self._player.stop()

    def _get_alarm_list(self):
        return sorted(['{}{}'.format(alarm.alarm_time, '' if alarm.enabled else ' 已停用') for alarm in self._alarms])

    def _find_alarm(self, alarm_time):
        for alarm in self._alarms:
            if alarm.alarm_time == alarm_time:
                return alarm
        return None

    def _save_alarms(self):
        with open(ALARM_SAVE_FILE, 'wb') as f:
            pickle.dump(self._alarms, f)

    def _load_alarms(self):
        self._alarms = []
        if os.path.isfile(ALARM_SAVE_FILE):
            try:
                with open(ALARM_SAVE_FILE, 'rb')as f:
                    self._alarms = pickle.load(f)
            except:
                self._alarms = []

    def update(self):
        super().update()
        current_time_str = datetime.now().strftime('%H:%M')

        for alarm in self._alarms:
            if alarm.enabled:
                if alarm.alarm_time != self._old_time_str and alarm.alarm_time == current_time_str:
                    self._play_alarm()
                    break

        self._old_time_str = current_time_str

        if self._alarm_is_playing:
            if not self._player.is_playing():
                self._alarm_is_playing = False
                self._holder.resume_music_players(self)

    def _get_alarm_mp3_list(self):
        mp3_list = glob.glob('{}/*.mp3'.format(self._config.alarm_mp3_folder))
        return mp3_list

    def pause(self):
        self._player.pause()

    def resume(self):
        self._player.resume()
