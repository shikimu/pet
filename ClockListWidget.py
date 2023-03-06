# -*- coding: utf-8 -*

import os
import json

from ClockWidget import ClockAddWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QTableView, QPushButton
from PyQt5.QtGui import *

class ClockListWidget(QWidget):
    
    clock_change_signal = pyqtSignal()
    
    clock_list = {
        "list": []
    }
    
    def __init__(self):
        super(ClockListWidget, self).__init__()
        windows_rect = QApplication.desktop().screenGeometry()
        self.screen_width = windows_rect.width()
        self.screen_height = windows_rect.height()
        self.setFixedSize(1000, 700)
        self.initUI()
        
    def initUI(self):
        self.setGeometry(int(self.screen_width / 2) - 500, int(self.screen_height / 2) - 350, 1000, 700)
        self.setWindowTitle("闹钟列表")
        self.autoFillBackground = True
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        
        self.load_clock()
        
        hLayout = QHBoxLayout()
        tableLayout = QVBoxLayout()
        self.tableView = QTableView()
        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tableView.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.set_table()
        tableLayout.addWidget(self.tableView)
        buttonLayout = QVBoxLayout()
        
        # saveButton = QPushButton("保存修改")
        # saveButton.clicked.connect(self.save_change)
        addButton = QPushButton("添加")
        addButton.clicked.connect(self.add_clock)
        deleteButton = QPushButton("删除")
        deleteButton.clicked.connect(self.delete_clock)
        changeButton = QPushButton("修改")
        changeButton.clicked.connect(self.change_clock)
        nowButton = QPushButton("当前信息")
        nowButton.clicked.connect(self.showTableInfo)
        
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addWidget(changeButton)
        buttonLayout.addWidget(nowButton)
        
        hLayout.addLayout(tableLayout)
        hLayout.addLayout(buttonLayout)
        hLayout.setStretch(0, 4)
        hLayout.setStretch(1, 1)
        self.setLayout(hLayout)
    
    def set_table(self):
        model = QStandardItemModel(len(self.clock_list["list"]), 6)
        model.setHorizontalHeaderLabels(['时', '分', '仅一次', '备注', '音乐路径', '启用'])
        for row in range(len(self.clock_list['list'])):
            clock = self.clock_list['list'][row]
            for index, str in enumerate(["%s"%(clock['hour']), "%s"%(clock['minute']), "%s"%(clock['once']), "%s"%(clock['remake']), "%s"%(clock['music']), "%s"%(clock['play'] == 'False')]):
                item = QStandardItem(str)
                item.setFlags(Qt.ItemIsSelectable)
                model.setItem(row, index, item)
        self.tableView.setModel(model)
    
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
                
    def save_clock(self):
        with open(r'setting/clock.json', "w") as outfile:
            json.dump(self.clock_list, outfile)
            self.clock_change_signal.emit()
            
    def change_clock(self):
        pass

    def add_clock(self):
        addView = ClockAddWidget()
        addView.clock_add_signal.connect(self.add_clock_list)
        addView.show()
    
    def add_clock_list(self, hour: int, minute: int, once: str, remake: str, music: str, play: str):
        self.tableView.model().rowCount()
        pass
        
    
    def delete_clock(self):
        rows = self.tableView.selectionModel().selectedRows()
        if rows:
            del self.clock_list['list'][rows[0].row()]
            self.save_clock()
            self.set_table()
                
    def showTableInfo(self):
        a = QStandardItemModel(self.tableView.model())
        
        # a.item()
        print(a)
