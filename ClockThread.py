# -*- coding: utf-8 -*-

import os
import json
from pygame import mixer
from PyQt5.QtCore import QThread, QTime, pyqtSignal


class ClockThread(QThread):
    
    music_path = ''

    playing_time = 0

    clock_playing = False

    clock_list = {

    }

    # activity_signal = pyqtSignal()

    clock_signal = pyqtSignal()

    def __init__(self):
        super(ClockThread, self).__init__()
        self.load_clock()
        mixer.init()

    def run(self):
        while True:
            # self.activity_signal.emit()
            self.clock_start()
            self.sleep(1)

    def load_clock(self):
        dir_path = r'setting'
        json_path = r'setting/clock.json'
        if os.path.exists(dir_path) == False:
            os.makedirs(dir_path)
        if os.path.exists(json_path):
            with open(json_path) as f:
                self.clock_list = json.load(f)
        else:
            self.clock_list = {
                "list": []
            }
            with open(json_path, "w") as outfile:
                json.dump(self.clock_list, outfile)

    def clock_start(self):
        time = QTime.currentTime()
        hour = time.hour()
        minute = time.minute()
        # print("现在时间是{}:{}:{}".format(hour, minute, time.second()))
        if self.clock_playing:
            self.playing_time += 1
            if self.playing_time >= 300:
                # 停止音乐
                if mixer.music.get_busy():
                    mixer.music.stop()
                self.clock_playing = False
                self.playing_time = 0

        # if hour == 0 and minute == 0:
        #     for item in self.clock_list['list']:
        #         if not item['once']:
        #             item['play'] = False
        #     print('闹钟重置')
        #     self.clock_save()
        for item in self.clock_list['list']:
            if item['play'] and (not item['once']) and (item['hour'] < hour or (item['hour'] == hour and item['minute'] < minute)):
                # 重置闹钟
                item['play'] = False
                self.clock_save()
            if item['hour'] == hour and item['minute'] == minute and (not item['play']):
                item['play'] = True
                self.clock_save()
                if not self.clock_playing:
                    self.clock_play(item=item)
                break

    def clock_save(self):
        json_path = r'setting/clock.json'
        with open(json_path, "w") as outfile:
            json.dump(self.clock_list, outfile)

    def clock_play(self, item):
        # TODO: 闹钟响起
        hour = item['hour']
        minute = item['minute']
        remark = item['remake']
        print("闹钟 {}:{} \n{}".format(hour, minute, remark))
        # self.music_path = item['music']
        self.music_path = 'music/oblivious.mp3'
        self.clock_signal.emit()
        self.clock_playing = True
        try:
            mixer.music.load(self.music_path)
            if not mixer.music.get_busy():
                mixer.music.play()
        except:
            print('load music error')
            self.clock_playing = False