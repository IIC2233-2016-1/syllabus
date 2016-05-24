__author__ = 'christian pieringer'

from PyQt4 import QtGui

class MiVentana(QtGui.QWidget):
    pass

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MiVentana()
    window.resize(300, 300)
    window.setWindowTitle('Mi Primera Ventana')
    window.show()
    app.exec_()