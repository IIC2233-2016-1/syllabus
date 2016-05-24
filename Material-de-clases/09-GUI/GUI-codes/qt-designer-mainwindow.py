__author__ = 'cppie_000'

from PyQt4 import QtGui
from ui_mainwindow import Ui_MainWindow


class MainWindow(Ui_MainWindow, QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ''' Se crean las conexiones con los puertos'''
        self.pushButton1.clicked.connect(self.click_button)

    def click_button(self):
        self.label_3.setText('= ' + str(float(self.lineEdit1.text()) / float(self.lineEdit2.text())))



if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()