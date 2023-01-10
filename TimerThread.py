# -*- coding: utf-8 -*-

import os
import json
import base64
import configparser
from pygame import mixer
from PyQt5.QtCore import QThread, QTime, pyqtSignal, QDateTime

# 计时器，时间相关判断
class TimerThread(QThread):

    start_time = 0
    last_time = 0
    all_time = 0

    local_ahead_times = 0

    config = configparser.ConfigParser()

    music_path = ''

    playing_time = 0

    auto_shutdown = False

    shutdown_hour = 0
    shutdown_minute = 0
    shutdown_doing = False

    clock_playing = False

    clock_list = {

    }
    
    clock_item = {

    }

    clock_signal = pyqtSignal()

    def __init__(self):
        super(TimerThread, self).__init__()
        self.start_time = QDateTime.currentDateTime().toTime_t()
        self.load_shutdownInfo()
        self.load_clock()
        mixer.init()

    def run(self):
        while True:
            self.timer_start()
            self.sleep(1)
            self.all_time += 1

    # 装载关机信息
    def load_shutdownInfo(self):
        dir_path = r'setting'
        config_path = r'setting/config.ini'
        if os.path.exists(dir_path) == False:
            os.makedirs(dir_path)
        self.config.read(config_path, encoding='utf-8')
        if os.path.exists(config_path) and self.config.has_section("Shutdown"):
            self.auto_shutdown = self.config.get("Shutdown", "auto") == "True"
            self.shutdown_hour = int(self.config.get("Shutdown", "hour"))
            self.shutdown_minute = int(self.config.get("Shutdown", "minute"))
        else:
            self.config.add_section("Shutdown")    
            self.config.set("Shutdown", "auto", "False")
            self.config.set("Shutdown", "hour", "0")
            self.config.set("Shutdown", "minute", "0")
            self.config.write(open(config_path, "w"))

    # 装载闹钟信息
    def load_clock(self):
        json_path = r'setting/clock.json'
        if os.path.exists(json_path):
            with open(json_path) as f:
                self.clock_list = json.load(f)
        else:
            self.clock_list = {
                "list": []
            }
            with open(json_path, "w") as outfile:
                json.dump(self.clock_list, outfile)

    def timer_start(self):
        time = QTime.currentTime()
        hour = time.hour()
        minute = time.minute()
        self.judge_shutdown(hour=hour, minute=minute)
        self.judge_clock(hour=hour, minute=minute)

    # 关机判断
    def judge_shutdown(self, hour: int, minute: int):
        if self.auto_shutdown:
            if hour == self.shutdown_hour and minute == self.shutdown_minute and (not self.shutdown_doing):
                self.shutdown_doing = True
                self.shutdown_save()
                os.system('shutdown -s -t 30')
    
    # 自动关机信息记录
    def shutdown_save(self):
        end_time = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')
        start_time = QDateTime.fromTime_t(self.start_time).toString('yyyy-MM-dd HH:mm:ss')
        m, s = divmod(self.all_time, 60)
        h, m = divmod(m, 60) 
        log = '本次开始时间为{}，共运行{}小时{}分钟{}秒，结束时间为{}, 本地时间前调{}次'.format(start_time, h, m, s, end_time, self.local_ahead_times)
        blog = base64.b64encode(log.encode(encoding='utf-8')).decode(encoding='utf-8')
        logs_path = r"logs.txt"
        with open(logs_path, 'a', encoding='utf-8') as file:
            file.write('{}: {}\n'.format(end_time, blog))

    # 闹钟判断
    def judge_clock(self, hour: int, minute: int):
        if self.clock_playing:
            self.playing_time += 1
            if self.playing_time >= 300:
                # 停止音乐
                self.clock_stop()
            else:
                self.clock_play(type=1)
        if self.all_time % 15 == 0:
            # self.clock_signal.emit()
            now_time = QDateTime.currentDateTime().toTime_t()
            if self.last_time > now_time:
                self.local_ahead_times += 1
            self.last_time = now_time
            for item in self.clock_list['list']:
                if item['play'] and (not item['once']) and (item['hour'] < hour or (item['hour'] == hour and item['minute'] < minute)):
                    # 重置闹钟
                    item['play'] = False
                    self.clock_save()
                if item['hour'] == hour and item['minute'] == minute and (not item['play']):
                    item['play'] = True
                    self.clock_save()
                    if not self.clock_playing:
                        self.clock_item = item
                        self.clock_play()

    # 闹钟变更存储
    def clock_save(self):
        json_path = r'setting/clock.json'
        with open(json_path, "w") as outfile:
            json.dump(self.clock_list, outfile)

    # 闹钟 type： 0 首次播放 1 循环
    def clock_play(self, type: int=0):
        if type == 0:
            hour = self.clock_item['hour']
            minute = self.clock_item['minute']
            remark = self.clock_item['remake']
            print("闹钟 {}:{} \n{}".format(hour, minute, remark))
            # self.music_path = self.clock_item['music']
            self.clock_signal.emit()
            self.clock_playing = True
        self.music_path = 'music/oblivious.mp3'
        try:
            if not mixer.music.get_busy():
                mixer.music.load(self.music_path)
                mixer.music.play()
        except:
            print('load music error')
            self.clock_playing = False

    def clock_stop(self):
        self.clock_playing = False
        self.playing_time = 0
        if mixer.music.get_busy():
            mixer.music.stop()
        

    def shutdown_change(self):
        os.system('shutdown -a')
        self.shutdown_doing = False
        self.shutdown_minute += 10
        if self.shutdown_minute >= 60:
            self.shutdown_hour += 1
            self.shutdown_minute -= 60
            if self.shutdown_hour >= 24:
                self.shutdown_hour -= 24