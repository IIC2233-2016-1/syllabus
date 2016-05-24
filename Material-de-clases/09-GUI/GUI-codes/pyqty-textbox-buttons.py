__author__ = 'christian pieringer'

#import sys
from PyQt4 import QtGui, QtCore


class MainForm(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        self.form = MiFormulario()
        self.setCentralWidget(self.form)


class MiFormulario(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.init_GUI()

    def init_GUI(self):
        ''' Este método inicializa la interfaz y sus elementos'''

        self.label1 = QtGui.QLabel('Texto:', self)
        self.label1.move(10, 15)

        self.label2 = QtGui.QLabel('Aqui se escribe la respuesta', self)
        self.label2.move(10, 50)

        self.label3 = QtGui.QLabel('Origen de la señal:', self)
        self.label3.move(10, 250)

        self.edit1 = QtGui.QLineEdit('', self)
        self.edit1.setGeometry(45, 15, 100, 20)

        self.boton1 = QtGui.QPushButton('&Procesar', self)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.move(5, 70)
        self.boton1.clicked.connect(self.boton1_callback)
        self.boton1.clicked.connect(self.boton_presionado)

        self.boton2 = QtGui.QPushButton('&Salir', self)
        self.boton2.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.boton2.resize(self.boton2.sizeHint())
        self.boton2.move(90, 70)


        ''' Agrega todos los elementos al formulario '''
        #hbox = QtGui.QHBoxLayout()
        #hbox.addWidget(self.boton1)
        #hbox.addWidget(self.boton2)

        #self.boton1.clicked.connect(lambda: self.boton_apretado())

        self.setGeometry(200, 100, 300, 300)
        self.setWindowTitle('Ventana con Boton')
        #self.setLayout(hbox)
        self.show()

    def boton_presionado(self):
        sender = self.sender()
        self.label3.setText('{0} {1}'.format(self.label3.text(), sender.text()))
        self.label3.resize(self.label3.sizeHint())

    def boton1_callback(self):
        self.label2.setText('{}'.format(self.edit1.text()))
        self.label2.resize(self.label2.sizeHint())

    def keyPressEvent(self, event):
        QtGui.QMessageBox.information(None,"Received Key Press Event!!",
				     "You Pressed: "+ event.text())

if __name__ == '__main__':
    app = QtGui.QApplication([])

    ''' Se crea una ventana descendiente de QMainWindows'''
    form = MainForm()
    #form = MiFormulario()
    app.exec_()

