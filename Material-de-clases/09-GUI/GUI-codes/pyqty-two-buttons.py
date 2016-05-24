__author__ = 'christian pieringer'

#import sys
from PyQt4 import QtGui, QtCore


class MiFormulario(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.init_GUI()

    def init_GUI(self):
        ''' Este método inicializa la interfaz y sus elementos'''

        self.boton1 = QtGui.QPushButton('&Boton1', self)
        self.boton1.resize(self.boton1.sizeHint())
        #self.boton1.move(5, 10)

        self.boton2 = QtGui.QPushButton('&Salir', self)
        self.boton2.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.boton2.resize(self.boton2.sizeHint())
        #self.boton2.move(5, 40)

        ''' Agrega todos los elementos al formulario '''
        hbox = QtGui.QHBoxLayout()
        #hbox = QtGui.QVBoxLayout()
        hbox.addWidget(self.boton1)
        hbox.addWidget(self.boton2)

        self.setGeometry(200, 100, 300, 300)
        self.setWindowTitle('Ventana con Boton')
        self.setLayout(hbox)
        self.show()


if __name__ == '__main__':
    app = QtGui.QApplication([])

    ''' Se crea una ventana descendiente de QMainWindows'''
    windows = MiFormulario()
    app.exec_()

