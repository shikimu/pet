# -*- coding: utf-8 -*-

import json
import configparser
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QBrush, QShowEvent, QCloseEvent
from PyQt5.QtCore import pyqtSignal, Qt, QDateTime, QTime

class ClockAddWidget(QWidget):

    config = configparser.ConfigParser()

    alwaysResponse = False

    clock_add_signal = pyqtSignal(dict)

    selectTime: QTime = QTime.currentTime()

    def __init__(self):
        super(ClockAddWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("添加闹钟")
        self.setAutoFillBackground = True
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(r"Resources/Background/clock.png").scaled(300, 300, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation)))
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
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
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
        if self.onceButton.isChecked():
            value = "添加闹钟, 时间为{}:{}(仅一次)".format(self.selectTime.hour(), self.selectTime.minute())
        else:
            value = "添加闹钟, 时间为{}:{}".format(self.selectTime.hour(), self.selectTime.minute())
        QMessageBox.about(self,"添加闹钟", value)
        self.clock_add_signal.emit(clock)
        self.hide()

    def timeChanged(self, time: QTime):
        self.selectTime = time

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.load_ini()
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        if self.alwaysResponse:
            self.setWindowModality(Qt.NonModal)
        else:
            self.setWindowModality(Qt.ApplicationModal)

    def load_ini(self):
        config_path = r'setting/config.ini'
        self.config.read(config_path)
        if os.path.exists(config_path) and self.config.has_section("Response"):
            self.alwaysResponse = (self.config.get('Response', 'Always') == 'True')
        else:
            self.config.add_section("Response")    
            self.config.set("Response", "Always", "True")
            self.config.write(open(config_path, "w"))
            self.alwaysResponse = False

class ClockMessageWidget(QWidget):

    end_signal = pyqtSignal()

    def __init__(self):
        super(ClockMessageWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        print('关闭事件')
        self.end_signal.emit()
        return super().closeEvent(a0)