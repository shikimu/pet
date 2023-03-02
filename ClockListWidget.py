# -*- coding: utf-8 -*

import os
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QTableView, QPushButton
from PyQt5.QtGui import *

class ClockListWidget(QWidget):
    
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
        
        saveButton = QPushButton("保存修改")
        saveButton.clicked.connect(self.save_change)
        addButton = QPushButton("添加")
        addButton.clicked.connect(self.add_clock)
        deleteButton = QPushButton("删除")
        deleteButton.clicked.connect(self.delete_clock)
        nowButton = QPushButton("当前信息")
        nowButton.clicked.connect(self.showTableInfo)
        
        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
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
            # a = QStandardItem("1")
            # a.setFlags(Qt.ItemIsEnabled)
            model.setItem(row, 0, QStandardItem( "%s"%(clock['hour'])))
            model.setItem(row, 1, QStandardItem( "%s"%(clock['minute'])))
            model.setItem(row, 2, QStandardItem( "%s"%(clock['once'])))
            model.setItem(row, 3, QStandardItem( "%s"%(clock['remake'])))
            model.setItem(row, 4, QStandardItem( "%s"%(clock['music'])))
            model.setItem(row, 5, QStandardItem( "%s"%(clock['play'] == 'False')))
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
            
    def save_change(self):
        pass

    def add_clock(self):
        pass
    
    def delete_clock(self):
        path = self.tableView.selectionModel().selection().indexes()
        del self.clock_list['list'][path[0].row()]
        self.save_clock()
        self.set_table()
                
    def showTableInfo(self):
        a = QStandardItemModel(self.tableView.model())
        
        # a.item()
        print(a)
