# -*- coding: utf-8 -*-

import sys

from ClockThread import ClockThread
from SetTab import SetTab
from ClockWidget import ClockAddWidget, ClockMessageWidget
from RyougiPet import RyougiPet
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    clock = ClockThread()
    clock.start()

    app = QApplication(sys.argv)
    petView = RyougiPet()
    setView = SetTab()
    clockView = ClockAddWidget()
    clockView.clock_list = clock.clock_list
    petView.setting_signal.connect(setView.show)
    petView.clock_signal.connect(clockView.show)
    clockView.clock_add_signal.connect(clock.load_clock)

    clockMessageView = ClockMessageWidget()
    clock.clock_signal.connect(clockMessageView.show)

    petView.show()
    sys.exit(app.exec_())