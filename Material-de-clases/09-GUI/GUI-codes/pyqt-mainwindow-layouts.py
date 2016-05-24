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

        my_signal = QtCore.pyqtSignal().connect()
        self.label1 = QtGui.QLabel('Texto:', self)
        self.label1.move(10, 15)

        self.edit1 = QtGui.QLineEdit('', self)
        self.edit1.setGeometry(45, 15, 100, 20)

        self.boton1 = QtGui.QPushButton('&Calcular', self)
        self.boton1.resize(self.boton1.sizeHint())

        ''' Aquí se crea el objeto QHBoxLayout() y QVBoxLayout() y se agregan los Widgets mediante el método addWidget. El método
            stretch() permite incluir un espaciador que expande el layout hacia la derecha y hacia abajo.'''
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.label1)
        hbox.addWidget(self.edit1)
        hbox.addWidget(self.boton1)
        hbox.addStretch(1)
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignTop)
        #vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox) # el layout horizontal está contenido en el vertical

    def cambia_estado(self):

if __name__ == '__main__':
    app = QtGui.QApplication([])

    ''' Se crea una ventana descendiente de QMainWindows'''
    form = MainForm()
    form.show()
    app.exec_()
