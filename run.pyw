# -*- coding: utf-8 -*-

import sys

from TimerThread import TimerThread
from SetTab import SetTab
from ClockWidget import ClockAddWidget, ClockMessageWidget, ShutdownWidget
from RyougiPet import RyougiPet
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    timer = TimerThread()
    timer.start()

    app = QApplication(sys.argv)
    petView = RyougiPet()
    setView = SetTab()
    clockView = ClockAddWidget()
    shutdownView = ShutdownWidget()
    clockView.clock_list = timer.clock_list
    petView.setting_signal.connect(setView.show)
    petView.clock_signal.connect(clockView.show)
    petView.shutdown_signal.connect(shutdownView.show)
    petView.quite_signal.connect(timer.shutdown_save)
    
    clockView.clock_add_signal.connect(timer.load_clock)
    shutdownView.change_signal.connect(timer.load_shutdownInfo)

    clockMessageView = ClockMessageWidget()
    clockMessageView.end_signal.connect(timer.clock_stop)
    timer.clock_signal.connect(clockMessageView.show)

    petView.show()
    sys.exit(app.exec_())