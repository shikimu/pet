# -*- coding: utf-8 -*-

import os
import shutil
import platform

from PyQt5.QtWidgets import QLabel, QMessageBox
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap, QMouseEvent, QDragEnterEvent, QDragLeaveEvent, QDropEvent, QIcon
from PyQt5.QtCore import pyqtSignal, QEvent

class SFLabel(QLabel):

    imgUrl = "1_new.png"
    eimgUrl = "2_new.png"
    dragUrl = "3_new.png"

    isLeft = False

    acceptDropDelete = True
    deleteTip = False
    deleteToAshbin = False

    isMenu = False

    labelDoubelClickSig = pyqtSignal(str)

    def __int__(self):
        super(SFLabel, self).__init__()

    def baseImgSet(self, imgUrl: str, eimgUrl: str, dragUrl: str):
        self.imgUrl = imgUrl
        self.eimgUrl = eimgUrl
        self.dragUrl = dragUrl

    def baseSet(self, width: int = 360, height: int = 203):
        self.width = width
        self.height = height
        self.setImage()

    def updateImg(self, imgUrl: str):
        self.imgUrl = imgUrl
        self.setImage()

    def setImage(self, image = imgUrl):
        # 使用PIL（若控件水平翻转不成，使用此水平翻转图片）
        img = Image.open(image)
        if self.isLeft:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        qImg = ImageQt.ImageQt(img)
        pixmap = QPixmap.fromImage(qImg)
        sc_img = pixmap.scaled(self.width, self.height)
        self.setPixmap(sc_img)
        # 直接赋值
        # img = QPixmap(image)
        # sc_img = img.scaled(self.width, self.height)
        # self.setPixmap(sc_img)

    # 文件拖拽进入
    def dragEnterEvent(self, event: QDragEnterEvent):
        if self.acceptDropDelete:
            self.setImage(self.dragUrl)
            event.accept()
        else:
            event.ignore()
            

    def dropEvent(self, event: QDropEvent):
        if self.deleteTip:
            print("弹窗")
            messageBox = QMessageBox(self)
            messageBox.setWindowIcon(QIcon("icon128*128.ico"))
            messageBox.setWindowTitle("是否删除")
            messageBox.setText("是否删除")
            Qyes = messageBox.addButton(self.tr("删除"), QMessageBox.YesRole)
            QNo = messageBox.addButton(self.tr("取消"), QMessageBox.NoRole)
            messageBox.setDefaultButton(QNo)
            messageBox.exec_()
            if messageBox.clickedButton() == Qyes:
                print("点击删除")
                for url in event.mimeData().urls():
                    path = url.toLocalFile()
                    self.deleteFile(path)
            else:
                print("点击其他")
                self.setImage()
                event.ignore()
        else:
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                self.deleteFile(path)
       

    # 删除文件
    def deleteFile(self, path: str):
        print("删除")
        if self.deleteToAshbin:
            if platform.system() == "Windows":
                from win32com.shell import shell, shellcon
                print(platform.system())
            elif platform.system() == "Darwin":
                import subprocess
                # 会卡mac
                if os.path.exists(path):
                    absPath = os.path.abspath(path).replace("\\", "\\\\").replace('"','\\"')
                    cmd = ['osascript', '-e', 'tell app "Finder" to move {the POSIX file "' + absPath + '"} to trash']
                    subprocess.call(cmd, stdout=open(os.devnull, 'w'))
            else:
                print("暂不支持该平台移入回收站")
        else:
            if os.path.isdir(path):
                print("删除文件夹")
                shutil.rmtree(path)
            elif os.path.isfile(path):
                print("删除文件")
                os.remove(path)
            self.setImage()

    # 文件拖拽离开
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.setImage()
    
    # 双击
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        sigContent = self.objectName()
        self.labelDoubelClickSig.emit(sigContent)

    # 鼠标进入
    def enterEvent(self, event: QEvent):
        print("label进入")
        self.setImage(self.eimgUrl)
    
    # 鼠标离开
    def leaveEvent(self, event: QEvent):
        print("离开")
        if not self.isMenu:
            self.setImage()

    def menuEnd(self):
        self.isMenu = False
        self.setImage()
