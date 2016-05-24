__author__ = 'cppie_000'

from PyQt4 import QtGui, QtCore


class MainForm(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()

        ''' Configura geometría de la ventana'''
        self.setWindowTitle('Ventana con Boton')
        self.setGeometry(200, 100, 300, 250)

        ''' Configura como Widget Central el formulario creado anteriormente.'''
        self.form = MiFormulario()
        self.setCentralWidget(self.form)


class MiFormulario(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.init_GUI()

    def init_GUI(self):
        ''' Este método inicializa la interfaz y sus elementos'''
        grilla = QtGui.QGridLayout()
        self.setLayout(grilla)

        valores = ['1', '2', '3',
                   '4', '5', '6',
                   '7', '8', '9',
                   '*', '0', '#']

        posicion = [(i,j) for i in range(4) for j in range(3)]

        for posicion, valor in zip(posicion, valores):
            if valor == '':
                continue
            boton = QtGui.QPushButton(valor)
            grilla.addWidget(boton, *posicion)

        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication([])

    ''' Se crea una ventana descendiente de QMainWindows'''
    form = MainForm()
    form.show()
    app.exec_()
