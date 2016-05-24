from PyQt4 import QtGui, uic
from sys import argv, exit
from random import randint

__author__ = "figarrido"
__author__ = 'cpieringer, 2015.05.11'

'''
uic.loadUiType entrega una lista con dos elementos
[Ui_MainWindow, PyQt4.QtGui.QMainWindow]
El primer elemento corresponde a la clase de la ventana
creada en QtDesigner y la segunda a la clase que hereda
'''
form_classes = uic.loadUiType("VisualGame.ui")

OPERACIONES = [('suma', '+'), ('resta', '-'), ('mult', '*'), ('div', '/')]
DIFICULTAD = 20


class Juego(form_classes[0], form_classes[1]):

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        '''  Genera aleatoriamente los números de la jugada '''
        self.ledit_1.setText(str(randint(0, DIFICULTAD)))
        self.ledit_2.setText(str(randint(0, DIFICULTAD)))

        ''' Conexión de eventos '''
        self.btn_new.clicked.connect(self.btn_newGame_clicked)
        self.btn_result.clicked.connect(self.btn_result_clicked)

        ''' Conectar los QRadioButton que tienen nombres parecidos '''
        for oper in OPERACIONES:
            getattr(
                self, 'rbtn_' + oper[0]).toggled.connect(self.btn_newGame_clicked)

        '''
        Esta variable es para que el usuario no presione el botón
        Resultado continuamente y se vea obligado a presionar el
        botón Nuevo Juego
        '''
        self.siguiente = True


    def btn_newGame_clicked(self):
        self.siguiente = True
        self.ledit_result.setText('')

        for oper in OPERACIONES:
            if getattr(self, 'rbtn_' + oper[0]).isChecked():
                self.label_op.setText(oper[1])

        a = randint(0, DIFICULTAD)
        b = randint(0, DIFICULTAD)

        ''' Se quiere que las divisiones sean enteras, trabajar con números positivos '''
        if oper[0] == 'div' and (b == 0 or b > a or a % b != 0):
            b = randint(1, DIFICULTAD)
            c = randint(0, DIFICULTAD)
            a = c * b

        elif oper[0] == 'resta' and b > a:
            a, b = b, a

        self.ledit_1.setText(str(a))
        self.ledit_2.setText(str(b))

    def btn_result_clicked(self):
        try:
            if not self.siguiente:
                raise Warning('Debes comenzar un nuevo juego.')

            ''' Se obtienen los datos de la interfaz'''
            a = int(self.ledit_1.text())
            b = int(self.ledit_2.text())

            operacion = self.label_op.text()
            entrada = self.ledit_result.text()

            ''' Verificar que ingresa algo '''
            if not entrada:
                raise ValueError('Debes ingresar un número')

            ''' Verificar que se ingresan números '''
            if not entrada.isdigit():
                raise TypeError('Tu respueta debe ser un número.')

            if operacion == '+':
                resultado = a + b
            elif operacion == '-':
                resultado = a - b
            elif operacion == '*':
                resultado = a * b
            elif operacion == '/':
                resultado = a // b

            ''' Se verifica si el usuario respondió bien o mal '''
            if resultado == int(entrada):
                mensaje = 'Está correcto!'
            else:
                mensaje = 'Incorrecto :-(\n{0} {1} {2} = {3}'.format(a, operacion, b, resultado)

        except Warning as err:
            QtGui.QMessageBox.about(self, ' ', '{}'.format(err))
        except TypeError as err:
            QtGui.QMessageBox.about(self, ' ', '{}'.format(err))
        except ValueError as err:
            QtGui.QMessageBox.about(self, ' ', '{}'.format(err))
        else:
            ''' Genera un cuadro de mensajes para desplegar el mensaje '''
            QtGui.QMessageBox.about(self, ' ', mensaje)
            self.siguiente = False

if __name__ == '__main__':
    app = QtGui.QApplication(argv)
    MiJuego = Juego()
    MiJuego.show()
    exit(app.exec_())