from .main_widget import MainWidget
from PyQt4.QtGui import QApplication


__app = None
__main_widget = None


def init():
    global __main_widget, __app
    __app = QApplication([])
    __main_widget = MainWidget()


def add_entity(entity):
    entity.setParent(__main_widget)
    return entity


def set_size(x, y):
    __main_widget.setMinimumSize(x, y)


def run(main, delay=25):
    __main_widget.show()
    __main_widget.startMain(main, delay)
    # __main_widget.showFullScreen()
    __app.exec()
