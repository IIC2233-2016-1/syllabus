from PyQt4.QtGui import QWidget, QLabel, QPixmap
from PyQt4.Qt import QTimer
import os


_PATH = os.path.dirname(os.path.abspath(__file__))


class MainWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__timer = QTimer(self)
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(_PATH + os.sep + "assets" + os.sep + "background.png"))

    def startMain(self, main, delay=25):
        self.__timer.timeout.connect(main)
        self.__timer.start(delay)
