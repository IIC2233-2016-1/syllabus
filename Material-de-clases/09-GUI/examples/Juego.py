from PyQt4 import QtGui, uic
from sys import argv
from random import randint, choice

__author__ = "figarrido"


# uic.loadUiType entrega una lista con dos elementos
# [Ui_MainWindow, PyQt4.QtGui.QMainWindow]
# El primer elemento corresponde a la clase de la ventana
# creada en QtDesigner y la segunda a la clase que hereda
form_classes = uic.loadUiType("VisualGame.ui")

OPERACIONES = [('suma', '+'), ('resta', '-'), ('mult', '*'), ('div', '/')]
NIVELES = ['facil', 'medio', 'dificil']
DIFICULTAD = 20


class Juego(form_classes[0], form_classes[1]):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # Números aleatorios, ya que la primera operación es una suma
        self.ledit_1.setText(str(randint(0, DIFICULTAD)))
        self.ledit_2.setText(str(randint(0, DIFICULTAD)))

        # Conexión de eventos
        self.btn_new.clicked.connect(self.btn_newGame_clicked)
        self.btn_result.clicked.connect(self.btn_result_clicked)

        # Conectar los QRadioButton que tienen nombres parecidos 
        for oper in OPERACIONES:
            getattr(
                self, 'rbtn_' + oper[0]).toggled.connect(self.btn_newGame_clicked)

        for nivel in NIVELES:
            getattr(
                self, 'rbtn_' + nivel).toggled.connect(self.rbtn_cambiar_dificultad)

        # Esta variable es para que el usuario no presione el botón
        # Resultado continuamente y se vea obligado a presionar el
        # botón Nuevo Juego
        self.siguiente = True

    # BONUS #######
    def rbtn_cambiar_dificultad(self):
        global DIFICULTAD
        for nivel in NIVELES:
            if getattr(self, 'rbtn_' + nivel).isChecked():
                if nivel == 'facil':
                    DIFICULTAD = 20
                elif nivel == 'medio':
                    DIFICULTAD = 100
                else:
                    DIFICULTAD = 1000

        self.label_juegos.setText('0')
        self.label_buenos.setText('0')
        self.label_malos.setText('0')
        self.btn_newGame_clicked()
    ###############

    def btn_newGame_clicked(self):
        self.siguiente = True
        self.feedback.setText('')
        self.ledit_result.setText('')

        # Bonus #########
        if self.rbtn_random.isChecked():
            oper = choice(OPERACIONES)
            self.label_op.setText(oper[1])
        #################
        else:
            for oper in OPERACIONES:
                if getattr(self, 'rbtn_' + oper[0]).isChecked():
                    self.label_op.setText(oper[1])
                    break

        a = randint(0, DIFICULTAD)
        b = randint(0, DIFICULTAD)

        # Se quiere que las divisiones sean enteras
        if oper[0] == 'div' and (b == 0 or b > a or a % b != 0):
            b = randint(1, DIFICULTAD)
            c = randint(0, DIFICULTAD)
            a = c * b

        # Trabajar con números positivos
        elif oper[0] == 'resta' and b > a:
            a, b = b, a

        self.ledit_1.setText(str(a))
        self.ledit_2.setText(str(b))

    def btn_result_clicked(self):
        if not self.siguiente:
            self.feedback.setText('Debes comenzar un nuevo juego.')
            return

        # Se obtienen los datos de la interfaz
        a = int(self.ledit_1.text())
        b = int(self.ledit_2.text())
        operacion = self.label_op.text()
        entrada = self.ledit_result.text()

        # Verificar que ingresa algo
        if not entrada:
            self.feedback.setText('Debe ingresar un número.')
            return

        # Verificar que se ingresan números
        for digito in entrada:
            if not entrada.isdigit():
                self.feedback.setText('El resultado debe ser un número.')
                return

        # Se aumenta el número de juegos
        actual_juegos = int(self.label_juegos.text())
        self.label_juegos.setText(str(actual_juegos + 1))

        if operacion == '+':
            resultado = a + b
        elif operacion == '-':
            resultado = a - b
        elif operacion == '*':
            resultado = a * b
        elif operacion == '/':
            resultado = a // b

        # Se verifica si el usuario respondió bien o mal
        if resultado == int(entrada):
            self.feedback.setText('Está correcto!')
            actual_buenos = int(self.label_buenos.text())
            self.label_buenos.setText(str(actual_buenos + 1))

        else:
            self.feedback.setText(
                'No está correcto.\nLa respuesta correcta es {}.'.format(resultado))
            actual_malos = int(self.label_malos.text())
            self.label_malos.setText(str(actual_malos + 1))

        self.siguiente = False

app = QtGui.QApplication(argv)
MiJuego = Juego()
MiJuego.show()
app.exec_()
