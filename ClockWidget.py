# -*- coding: utf-8 -*-

import json
import configparser
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QBrush, QShowEvent, QCloseEvent
from PyQt5.QtCore import pyqtSignal, Qt, QDateTime, QTime

class ClockAddWidget(QWidget):

    clock_list = {
        
    }

    config = configparser.ConfigParser()

    alwaysResponse = False

    clock_add_signal = pyqtSignal()

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

class ShutdownWidget(QWidget):

    clock_list = {
        
    }

    config = configparser.ConfigParser()

    alwaysResponse = False

    change_signal = pyqtSignal()
    
    hour = 0
    minute = 0
    auto = True

    def __init__(self):
        super(ShutdownWidget, self).__init__()
        windows_rect = QApplication.desktop().screenGeometry()
        self.windows_width = windows_rect.width()
        self.windows_height = windows_rect.height()
        self.setFixedSize(500, 300)
        self.initUI()

    def initUI(self):
        self.setGeometry(int(self.windows_width / 2) - 250, int(self.windows_height / 2) - 150, 500, 300)
        self.setWindowTitle("设置关机时间")
        self.setAutoFillBackground = True
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)

        vLayout = QVBoxLayout()

        hLayout1 = QHBoxLayout()

        addClockButton = QPushButton("保存设置")
        addClockButton.clicked.connect(self.saveShutdown)

        self.dateEdit = QDateTimeEdit()
        self.dateEdit.setDisplayFormat("HH:mm")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.timeChanged.connect(self.timeChanged)

        self.onceButton = QRadioButton("自动关机")
        # self.onceButton

        hLayout1.addWidget(addClockButton)
        hLayout1.addWidget(self.dateEdit)
        hLayout1.addWidget(self.onceButton)
        vLayout.addLayout(hLayout1)
        self.setLayout(vLayout)

    def saveShutdown(self):
        config_path = r'setting/config.ini'
        self.config.read(config_path, encoding='utf-8')
        if self.onceButton.isChecked():
            auto = "True"
        else:
            auto = "False"
        self.config.set("Shutdown", "Auto", auto)
        self.config.set("Shutdown", "Hour", str(self.hour))
        self.config.set("Shutdown", "Minute", str(self.minute))
        self.config.write(open(config_path, "w"))
        QMessageBox.about(self,"保存", "保存成功")
        self.change_signal.emit()

    def timeChanged(self, time: QTime):
        self.hour = time.hour()
        self.minute = time.minute()

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.load_ini()
        self.setDateEditTime()
        self.setWindowModality(Qt.ApplicationModal)
        
    def setDateEditTime(self):
        time = QDateTime.currentDateTime()
        qTime = QTime(self.hour, self.minute,0,0)
        time.setTime(qTime)
        self.dateEdit.setDateTime(time)
        self.onceButton.setChecked(self.auto)

    def load_ini(self):
        config_path = r'setting/config.ini'
        self.config.read(config_path)
        if os.path.exists(config_path) and self.config.has_section("Shutdown"):
            self.auto = (self.config.get('Shutdown', 'Auto') == 'True')
            self.hour = int(self.config.get('Shutdown', 'Hour'))
            self.minute = int(self.config.get('Shutdown', 'Minute'))
        else:
            self.config.add_section("Shutdown")    
            self.config.set("Shutdown", "Auto", "True")
            self.config.set("Shutdown", "Hour", "0")
            self.config.set("Shutdown", "Minute", "0")
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