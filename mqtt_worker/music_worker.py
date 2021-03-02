import os
import glob
import random
import pickle

from config import Config
from worker import Worker
from music_player import MusicPlayer

MUSIC_TOPIC_ROOT = 'home/music/'
MUSIC_TOPIC_SUBSCRIBE = MUSIC_TOPIC_ROOT + '+'
SAFE_MP3 = 'mp3/try.mp3'
MUSIC_SAVE_FILE = 'music.cfg'

class MusicConfig():
    def __init__(self):
        self._volume = 100

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume

class MusicWorker(Worker):
    def __init__(self, holder):
        super().__init__(holder)
        random.seed()
        self._config = Config()
        self._player = MusicPlayer()
        self._load_config()

    def on_connect(self, client, userdata, flags):
        super().on_connect(client, userdata, flags)
        client.subscribe(MUSIC_TOPIC_SUBSCRIBE)

    def on_message(self, client, userdata, msg):
        super().on_message(client, userdata, msg)

        payload = msg.payload.decode('UTF-8')

        if msg.topic.startswith(MUSIC_TOPIC_ROOT):
            command = msg.topic.rsplit("/", 1)[-1]
            if command == 'play':
                mp3_file = payload
                result = self._play_music(mp3_file)
                client.publish(msg.topic + '/reply', payload=result, qos=1)
            elif command == 'stop':
                self._stop_music()
            elif command == 'play_random_one':
                self._play_random_one()
            elif command == 'list_music':
                mp3_list = self._get_mp3_list()
                file_list = [mp3.rsplit('/', 1)[-1] for mp3 in mp3_list]
                client.publish(msg.topic + '/reply',
                               payload='{}:{}'.format(payload, ','.join(file_list)), qos=1, retain=True)
            elif command == 'get_volume':
                volume = self._get_volume()
                client.publish(msg.topic + '/reply',
                               payload='{}'.format(volume), qos=1, retain=True)
            elif command == 'set_volume':
                result = self._set_volume(payload)
                client.publish(msg.topic + '/reply',
                           payload=result, qos=1)
                if result == 'ok':
                    client.publish(MUSIC_TOPIC_ROOT + 'get_volume/reply',
                               payload='{}'.format(payload), qos=1, retain=True)

    def _play_music(self, mp3_file = None, remote_command = True):
        self._stop_music()

        result = 'ok'

        if mp3_file is None or len(mp3_file) == 0:
            self._player.play(SAFE_MP3)
            result = 'ok'
        elif remote_command:
            if mp3_file.find('..') != -1 or mp3_file.find('/') != -1 or mp3_file.find('\\') != -1:
                # bad guy
                self._player.play(SAFE_MP3)
                result = 'File not exist!'
            else:
                full_path = '{}/{}'.format(self._config.mp3_folder, mp3_file)
                if os.path.isfile(full_path):
                    self._player.play(full_path)
                    result = 'ok'
                else:
                    self._player.play(SAFE_MP3)
                    result = 'File not exist!'
        else:
            self._player.play(mp3_file)
            result = 'ok'

        return result

    def _stop_music(self):
        self._player.stop()

    def _get_mp3_list(self):
        mp3_list = glob.glob('{}/*.[mM][pP]3'.format(self._config.mp3_folder))
        return mp3_list

    def _play_random_one(self):
        mp3_list = self._get_mp3_list()
        mp3_file = random.choice(mp3_list)
        print('Playing: {}'.format(mp3_file))
        self._play_music(mp3_file, remote_command=False)

    def _get_volume(self):
        return self._player.get_volume()

    def _set_volume(self, volume):
        v = -1
        try:
            v = int(volume)
        except:
            pass

        if v >= 0 and v <= 100:
            self._player.set_volume(v)
            self._music_config.volume = v
            self._save_config()
            return 'ok'
        else:
            return 'volume is valid!'

    def _save_config(self):
        with open(MUSIC_SAVE_FILE, 'wb') as f:
            pickle.dump(self._music_config, f)

    def _load_config(self):
        self._music_config = None
        if os.path.isfile(MUSIC_SAVE_FILE):
            try:
                with open(MUSIC_SAVE_FILE, 'rb')as f:
                    self._music_config = pickle.load(f)
            except:
                pass

        if self._music_config is None:
            self._music_config = MusicConfig()

        print('Volume:', self._music_config.volume)

        self._player.set_volume(self._music_config.volume)

    def pause(self):
        self._player.pause()
        # 为了解决 alarm 设置不了音量的问题
        # 也不彻底，先这样了！
        self._player.set_volume(100)

    def resume(self):
        self._player.resume()
        # 为了解决 alarm 设置不了音量的问题
        # 也不彻底，先这样了！
        self._player.set_volume(self._music_config.volume)
