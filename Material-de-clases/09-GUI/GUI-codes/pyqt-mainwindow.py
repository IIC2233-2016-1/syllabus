__author__ = 'cppie_000'

from PyQt4 import QtGui, QtCore


class MainForm(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()

        ''' Configura geometría de la ventana'''
        self.setWindowTitle('Ventana con Boton')
        self.setGeometry(200, 100, 300, 250)

        ''' Definición de acciones'''
        ver_status = QtGui.QAction(QtGui.QIcon(None), '&Cambiar Status', self)
        ver_status.setStatusTip('Este es un ítem de prueba')
        ver_status.triggered.connect(self.cambiar_status_bar)

        salir = QtGui.QAction(QtGui.QIcon(None), '&Exit', self)
        salir.setShortcut('Ctrl+Q')
        salir.setStatusTip('Exit application')
        salir.triggered.connect(QtGui.qApp.quit)


        ''' Creación de la barra de menús y de los menús'''
        menubar = self.menuBar()
        archivo_menu = menubar.addMenu('&Archivo') # primero menú
        archivo_menu.addAction(ver_status)
        archivo_menu.addAction(salir)


        otro_menu = menubar.addMenu('&Otro Menú') # segundo menú
        ''' Incluye la barra de estado'''
        self.statusBar().showMessage('Listo')

        ''' Configura como Widget Central el formulario creado anteriormente.'''
        self.form = MiFormulario()
        self.setCentralWidget(self.form)

    def cambiar_status_bar(self):
        self.statusBar().showMessage('Cambié el Status')


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

        self.label3 = QtGui.QLabel('Origen de la señal: ', self)
        self.label3.move(10, 180)

        self.edit1 = QtGui.QLineEdit('', self)
        self.edit1.setGeometry(45, 15, 100, 20)

        self.boton1 = QtGui.QPushButton('&Procesar', self)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.move(5, 70)
        self.boton1.clicked.connect(self.boton1_callback)
        self.boton1.clicked.connect(self.boton_presionado)

    def boton_presionado(self):
        sender = self.sender()
        self.label3.setText('Origen de la señal: {0}'.format(sender.text()))
        self.label3.resize(self.label3.sizeHint())

    def boton1_callback(self):
        self.label2.setText('{}'.format(self.edit1.text()))
        self.label2.resize(self.label2.sizeHint())


if __name__ == '__main__':
    app = QtGui.QApplication([])

    ''' Se crea una ventana descendiente de QMainWindows'''
    form = MainForm()
    form.show()
    app.exec_()
