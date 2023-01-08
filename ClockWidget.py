# -*- coding: utf-8 -*-

import json
import configparser
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QBrush, QShowEvent
from PyQt5.QtCore import pyqtSignal, Qt, QDateTime, QTime

class ClockAddWidget(QWidget):

    clock_list = {
        
    }

    alwaysResponse = False

    clock_add_signal = pyqtSignal()

    selectTime: QTime = QTime.currentTime()

    def __init__(self):
        super(ClockAddWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)

        self.setAutoFillBackground = True
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bg.png").scaled(300, 300, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation)))
        self.setPalette(palette)

        vLayout = QVBoxLayout()

        hLayout1 = QHBoxLayout()

        addClockButton = QPushButton("添加闹钟")
        addClockButton.clicked.connect(self.addClock)

        self.dateEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateEdit.setDisplayFormat("HH:mm")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.timeChanged.connect(self.timeChanged)

        self.onceButton = QRadioButton("仅一次")
        # self.onceButton

        hLayout1.addWidget(addClockButton)
        hLayout1.addWidget(self.dateEdit)
        hLayout1.addWidget(self.onceButton)
        vLayout.addLayout(hLayout1)

        self.setLayout(vLayout)

    def addClock(self):
        clock = {
            'hour': self.selectTime.hour(),
            'minute': self.selectTime.minute(),
            'remake': '',
            'once': self.onceButton.isChecked(),
            'music': '',
            'play': False
        }
        self.clock_list['list'].append(clock)
        with open(r'setting/clock.json', "w") as outfile:
            json.dump(self.clock_list, outfile)

        if self.onceButton.isChecked():
            value = "添加闹钟, 时间为{}:{}(仅一次)".format(self.selectTime.hour(), self.selectTime.minute())
        else:
            value = "添加闹钟, 时间为{}:{}".format(self.selectTime.hour(), self.selectTime.minute())
        QMessageBox.about(self,"添加闹钟", value)
        self.clock_add_signal.emit()

    def timeChanged(self, time: QTime):
        self.selectTime = time
        # print(time)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.load_ini()
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        if self.alwaysResponse:
            self.setWindowModality(Qt.NonModal)
        else:
            self.setWindowModality(Qt.ApplicationModal)

    def load_ini(self):
        config = configparser.ConfigParser()
        config_path = r'setting/config.ini'
        config.read(config_path)
        if os.path.exists(config_path) and config.has_section("Response"):
            self.alwaysResponse = (config.get('Response', 'Always') == 'True')
        else:
            config.add_section("Response")    
            config.set("Response", "Always", "True")
            config.write(open(config_path, "w"))
            self.alwaysResponse = True


class ClockMessageWidget(QWidget):

    end_signal = pyqtSignal()

    def __init__(self):
        super(ClockMessageWidget, self).__init__()
        self.initUI()

    def initUI(self):
        pass

    def close(self) -> bool:
        print('关闭')
        return super().close()

    def hide(self) -> None:
        print('隐藏')
        # self.end_signal.emit()
        return super().hide()