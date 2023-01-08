# -*- coding: utf-8 -*-
 
import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QApplication
 
 
class Button(QPushButton):
    # 需要重新实现某些方法才能使 QPushButton 接受拖放操作。# 因此我们创建了继承自 QPushButton 的 Button 类。
    def __init__(self, title, parent):
        super().__init__(title, parent)
    # 使该控件接受 drop(放下）事件。self.setAcceptDrops(True)
 
    def dragEnterEvent(self, e):
        # 我们重新实现了 dragEnterEvent()方法，# 并设置可接受的数据类型（在这里是普通文本）。
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()
 
    def dropEvent(self, e):
        # 通过重新实现 dropEvent()方法，# 我们定义了在 drop 事件发生时的行为。这里我们改变了按钮的文字。
        self.setText(e.mimeData().text())
 
 
class Example(QWidget):
    def __init__(self):
        super().__init__()
 
        self.initUI()
 
    def initUI(self):
        edit = QLineEdit('', self)
        # QLineEdit 内置了对 drag(拖动）操作的支持。# 我们只需要调用 setDragEnabled()方法就可以了。
        edit.setDragEnabled(True)
        edit.move(30, 65)
 
        button = Button("Button", self)
        button.move(190, 65)
 
        self.setWindowTitle('Simple drag & drop')
        self.setGeometry(300, 300, 300, 150)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()  