# -*- coding: utf-8 -*-

import configparser
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class SetTab(QTabWidget):

    alwaysResponse = False

    config = configparser.ConfigParser()

    def __init__(self, parent=None):
        super(SetTab, self).__init__(parent)

        # self.setGeometry(300,300,200,200)
        self.setWindowTitle("设置")

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAutoFillBackground(True)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "设置")
        self.addTab(self.tab2, "关于")

        self.initTab1UI()
        self.initTab2UI()

    
    def initTab1UI(self):
        layout = QFormLayout()
        delete = QHBoxLayout()
        delete.addWidget(QRadioButton("直接删除"))
        delete.addWidget(QRadioButton("回收到垃圾桶"))
        layout.addRow(QLabel("删除方式"), delete)
        self.tab1.setLayout(layout)

    def initTab2UI(self):
        pass

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.load_ini()
        if self.alwaysResponse:
            # 正常模式
            self.setWindowModality(Qt.NonModal)
        else:
            # 阻止其他窗体相应
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