from .main_widget import MainWidget
from PyQt4.QtGui import QApplication
import gui2.entities as entities


__app = None
__main_widget = None


def init():
    global __main_widget, __app
    __app = QApplication([])
    __main_widget = MainWidget()


def add_entity(entity):
    entity.setParent(__main_widget)
    entity.show()
    return entity


def set_size(x, y):
    __main_widget.setFixedSize(x, y)
    entities._SCALE = 0.5 * y/800


def run(main, delay=25):
    __main_widget.show()
    __main_widget.startMain(main, delay)
    # __main_widget.showFullScreen()
    __app.exec()
