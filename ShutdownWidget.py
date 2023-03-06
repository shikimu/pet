# -*- coding: utf-8 -*-

import configparser
import os
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QDateTimeEdit, QRadioButton, QMessageBox
from PyQt5.QtGui import QShowEvent
from PyQt5.QtCore import pyqtSignal, Qt, QDateTime, QTime


class ShutdownWidget(QWidget):

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