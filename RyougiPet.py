# -*- coding: utf-8 -*-

import sys
import os
import configparser
import platform

from PIL import Image
from SFLabel import SFLabel
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class RyougiPet(QWidget):

    config = configparser.ConfigParser()

    roleIndex = 1

    width = 128
    height = 128
    
    alwayResponse = False
    rightPress = False

    setting_signal = pyqtSignal()
    clock_signal = pyqtSignal()
    quite_signal = pyqtSignal()
    shutdown_signal = pyqtSignal()

    def __init__(self):
        super(RyougiPet, self).__init__()

        # 获取屏幕宽高
        self.windows_rect = QApplication.desktop().screenGeometry()
        self.windows_width = self.windows_rect.width()
        self.windows_height = self.windows_rect.height() 
        self.load_role_ini()
        # 位置初始化
        self.pos_now = self.pos()

        # self.clock = QTimer()
        # self.clock.timeout.connect(self.clock_start)
        # self.clock.start(1000)
        self.initUI()
        self.mini_iconUI()

    def initUI(self):
        self.setGeometry(self.windows_width - self.width - 30, self.windows_height - self.height, self.width, self.height)
        self.setWindowTitle("Ryougi Pet")
        
        # 自定label使用
        self.sfLabel = SFLabel(self)

        # 配置读取
        self.load_label_ini(self.sfLabel)

        self.sfLabel.baseImgSet(basePath="Resources/Role/{}".format(self.roleIndex))
        self.sfLabel.baseSet(self.width, self.height)
        self.sfLabel.labelDoubelClickSig.connect(self.labelDoubelClickEvent)
        # 右键菜单
        self.sfLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sfLabel.customContextMenuRequested.connect(self.rightMenuInit)
        # 基础图像设置
        # self.base_label = QLabel(self)
        # self.base_pixmap = QPixmap(self.base_img)
        # self.base_label.setPixmap(self.base_pixmap)
        # self.base_label.setShortcutAutoRepeat(1000)
        self.setAutoFillBackground(True)
        # 背景透明
        # Qt.FramelessWindowHint(无框) Qt.WindowStaysOnTopHint(置顶) Qt.SubWindow(无底) Qt.NoDropShadowWindowHint(默认阴影边界) Qt.Tool(window，无问题）)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint | Qt.Tool)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        # 重设宽高（切换图片调用）
        # self.setStyleSheet("") 设置qss 与css基本一致 "SFLabel {background: red} "

        # self.sfLabel.setAutoFillBackground(True)
        # self.sfLabel.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.sfLabel.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.resize(720, 406)
        self.shortcut = QShortcut(QKeySequence("Esc"), self)
        self.shortcut.activated.connect(self.hide)

        if platform.system() == "Windows":
            self.setAttribute(Qt.WA_TranslucentBackground, True) # mac 失效对于qwidget (也可能多出一层图？，设置后setstylesheet无效)原因未知
        elif platform.system() == "Darwin":
            self.setStyleSheet("RyougiPet{background: transparent}") # windows则背景为黑 设置背景透明

        

    # mini菜单
    def mini_iconUI(self):
        mini_icon = QSystemTrayIcon(self)
        mini_icon.setIcon(QIcon("icon.ico"))

        mQuitAction = QAction("退出", self, triggered=self.quit)
        # mQuitAction.setShortcut(QKeySequence("Ctrl+Q"))
        mSetAction = QAction("设置", self, triggered=self.setting)
        miniMenu = QMenu(self)
        mShowAction = QAction("显示/隐藏", self, triggered=self.hideOrShow)
        miniMenu.addAction(mShowAction)
        miniMenu.addSeparator()
        miniMenu.addActions([mSetAction, mQuitAction])
        mini_icon.setContextMenu(miniMenu)
        if platform.system() == "Windows":
            mini_icon.activated.connect(self.miniAct)
        mini_icon.show()

    # 右键菜单
    def rightMenuInit(self):
        self.sfLabel.isMenu = True
        rightMenu = QMenu(self)
        setAction = QAction("设置", self, triggered=self.setting)
        clockAction = QAction("闹钟", self, triggered=self.clock)
        shutdownAction = QAction("关机", self, triggered=self.shutdown)
        quitAction = QAction("退出", self, triggered=self.quit)
        hideAction = QAction("隐藏", self, triggered=self.hide)
        # quitAction.setShortcut(QKeySequence("Ctrl+Q"))
        rightMenu.addActions([setAction, clockAction, shutdownAction])
        rightMenu.addSeparator()
        rightMenu.addActions([hideAction, quitAction])
        rightMenu.popup(QCursor.pos())

    # 鼠标按键
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.pos_now = event.globalPos() - self.pos()
            event.accept()
            self.sfLabel.isMove = True
            if self.sfLabel.isLeft:
                self.sfLabel.setImage(self.sfLabel.dragLUrl)
            else:
                self.sfLabel.setImage(self.sfLabel.dragRUrl)
            # 拖拽光标设定，可自定义
            self.setCursor(QCursor(Qt.ClosedHandCursor))
        elif event.button() == Qt.RightButton:
            self.rightPress = True
            event.ignore()
            
    # 鼠标移动
    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.rightPress:
            self.move(event.globalPos() - self.pos_now)
            # print(self.pos())
            self.x, self.y = self.pos().x, self.pos().y
            nowWidth = self.x() + (self.width / 2)
            if (nowWidth < (self.windows_width / 2)) and self.sfLabel.isLeft == False:
                self.sfLabel.isLeft = True
                self.sfLabel.setImage(self.sfLabel.dragLUrl)
                # print("右到左")
            elif (nowWidth >= (self.windows_width / 2)) and self.sfLabel.isLeft == True:
                self.sfLabel.isLeft = False
                self.sfLabel.setImage(self.sfLabel.dragRUrl)
                # print("左到右")
            event.accept()

    # 鼠标释放
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.sfLabel.isMove = False
        self.sfLabel.setImage(self.sfLabel.baseUrl, tran=self.sfLabel.isLeft)
        if self.rightPress:
            self.rightPress = False
        print("释放")

    # 双击事件
    def labelDoubelClickEvent(self):
        print("双击")
        # TODO: 切换图片
    
    # 窗体进入
    def enterEvent(self, event: QEvent):
        print("窗体进入")
        # TODO: 浮窗

    # 窗体离开
    def leaveEvent(self, event: QEvent):
        # print("窗体离开")
        pass

    # 设置
    def setting(self):
        print("设置")
        self.sfLabel.menuEnd()
        self.setting_signal.emit()

    def clock(self):
        print("设置闹钟")
        self.sfLabel.menuEnd()
        self.clock_signal.emit()

    def miniAct(self, reason):
        if reason == 3:
            if self.isHidden():
                self.show()
        if reason == 1:
            if self.isHidden():
                return

    def shutdown(self):
        print('设置关机')
        self.sfLabel.menuEnd()
        self.shutdown_signal.emit()

    # 退出
    def quit(self):
        self.close()
        sys.exit()

    def hide(self) -> None:
        self.sfLabel.menuEnd()
        return super().hide()

    def closeEvent(self, a0: QCloseEvent) -> None:
        print('退出')
        self.quite_signal.emit()
        return super().closeEvent(a0)
    
    def hideOrShow(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
    
    # 配置装载
    def load_label_ini(self, label: SFLabel):
        config_path = r'setting/config.ini'
        self.config.read(config_path)
        if os.path.exists(config_path) and self.config.has_section("Delete"):
            label.setAcceptDrops(self.config.get('Delete', 'Drop') == "True")
            label.acceptDropDelete = self.config.get('Delete', 'Drop') == "True"
            label.deleteTip = self.config.get('Delete', 'Tip') == "True"
            label.deleteToAshbin = self.config.get('Delete', 'ToAsh') == "True"
        else:
            self.config.add_section("Delete")    
            self.config.set("Delete", "Drop", "True")
            self.config.set("Delete", "Tip", "False")
            self.config.set("Delete", "ToAsh", "True")
            self.config.write(open(config_path, "w"))
            label.setAcceptDrops(True)
            label.acceptDropDelete = True
            label.deleteTip = False
            label.deleteToAshbin = True

    def load_role_ini(self):
        config_path = r'setting/config.ini'
        self.config.read(config_path)
        if self.config.has_section("Role"):
            self.roleIndex = int(self.config.get("Role", "Index"))
        else:
            self.config.add_section("Role")
            self.config.set("Role", "Index", "1")
            self.config.write(open(config_path, "w"))
            self.roleIndex = 1
        
        img = Image.open(r'./Resources/Role/{}/base.png'.format(self.roleIndex))
        self.width, self.height = img.size
        



        