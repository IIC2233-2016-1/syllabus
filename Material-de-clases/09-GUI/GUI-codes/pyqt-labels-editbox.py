__author__ = 'cppie_000'

from PyQt4 import QtGui, QtCore


class MiFormulario(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.init_GUI()

    def init_GUI(self):
        ''' Este método inicializa la interfaz y todos sus elementos o Widgets una vez que es llamado el formulario'''

        self.label1 = QtGui.QLabel('Texto:', self)
        self.label1.move(10, 15)

        self.label2 = QtGui.QLabel('Esta etiqueta es variable', self)
        self.label2.move(10, 50)

        self.edit1 = QtGui.QLineEdit('', self)
        self.edit1.setGeometry(45, 15, 100, 20)

        ''' Agrega todos los elementos al formulario '''
        self.setGeometry(200, 100, 200, 300)
        self.setWindowTitle('Ventana con Boton')
        self.show()


if __name__ == '__main__':
    app = QtGui.QApplication([])

    ''' Se crea una ventana descendiente de QMainWindows'''
    form = MiFormulario()
    app.exec_()