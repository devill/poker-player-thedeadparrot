import json
import threading
import time
import urllib

import player

CONFIG_JSON_URL = 'https://dl.dropboxusercontent.com/u/819938/leanpoker/config.json'

config_instance = None


class Config(object):
    version = 'config not loaded'
    refresh_interval = 5
    bet_on_high_card = 0
    bet_on_pair = 0
    bet_on_high_pair = 1000

    def __init__(self, test=False):
        self.log = player.log

        if not test:
            self._start_thread()

    @staticmethod
    def get_instance(*args, **kwargs):
        global config_instance

        if config_instance is None:
            config_instance = Config(*args, **kwargs)

        return config_instance

    def load(self):
        try:
            r = urllib.urlopen(CONFIG_JSON_URL)
            config_json = json.load(r)

            for k, v in config_json.iteritems():
                self.__setattr__(k, v)
                self.log.info('config set %s = %s', k, v)

            self.log.info('finished loading config file')
        except Exception as e:
            self.log.error('exception caught: %s', e)


    def _start_thread(self):
        thread = threading.Thread(target=self._load)
        thread.start()

    def _load(self):
        while True:
            self.load()
            time.sleep(self.refresh_interval)
