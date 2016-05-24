__author__ = 'cppie_000'

import sys
from PyQt4 import QtGui, QtCore

class MiFormulario(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.inicializa_GUI()


    def inicializa_GUI(self):

        self.etiqueta1 = QtGui.QLabel('Etiqueta', self)
        self.etiqueta1.move(20, 10)
        self.resize(self.etiqueta1.sizeHint())

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    def mousePressEvent(self, event):
        '''  Este evento maneja cuando se presiona alguno de los botones del mouse.'''
        self.etiqueta1.setText('Presionaron el mouse')
        self.etiqueta1.resize(self.etiqueta1.sizeHint())

    def keyPressEvent(self, event):

        #self.etiqueta1.setText('Presionaron la tecla: {}'.format(event.text()))
        #self.etiqueta1.resize(self.etiqueta1.sizeHint())

def main():

    app = QtGui.QApplication(sys.argv)
    ex = MiFormulario()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
