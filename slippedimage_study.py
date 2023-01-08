
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QWidget, QApplication

class SlippedImgWidget(QWidget):

    def __init__(self, bg, fg, *args, **kwargs):
        super(SlippedImgWidget, self).__init__(*args, **kwargs)

        # 鼠标跟踪