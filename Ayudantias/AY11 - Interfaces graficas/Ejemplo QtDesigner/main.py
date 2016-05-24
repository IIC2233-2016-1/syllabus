from PyQt4 import QtGui, uic

# Se entrega el path de la interfaz disenhada
form_sumar = uic.loadUiType("sumar.ui")
# form_sumar es una lista con dos clases: la ventana disenhada
# y la clase del widget de PyQt4 de donde hereda


# La clase ventana hereda de las dos clases de form_sumar
class Ventana(form_sumar[0], form_sumar[1]):

    def __init__(self):
        super().__init__()
        # self.setupUi(self) inicializa los widgets contenidos
        # en la ventana disenhada. Prueba que pasa si comentas esta linea.
        self.setupUi(self)
        # Es una buena practica crear metodos auxiliares del __init__ para que
        # este no sea muy largo y enredado
        self.__init_gui()
        self.__connect()

    def __init_gui(self):
        for widget in (self.sumando1LineEdit,
                       self.sumando2LineEdit,
                       self.resultadoLabel):
            widget.setText("0")

    def __connect(self):
        # Cuando el texto se cambia, se envia una señal
        # para ejecutar el metodo self.add en el backend.
        # Como este ejemplo es corto, el backend esta integrado en el frontend
        # Eviten hacer esto para proyectos mas extensos.
        self.sumando1LineEdit.textChanged.connect(self.add)
        self.sumando2LineEdit.textChanged.connect(self.add)

    def add(self):
        # Siempre que se recibe input de un usuario,
        # se deben manejar excepciones acorde a lo que se ingresa
        try:
            a = int(self.sumando1LineEdit.text() if self.sumando1LineEdit.text().isdigit() else 0)
            b = int(self.sumando2LineEdit.text() if self.sumando2LineEdit.text().isdigit() else 0)
            self.resultadoLabel.setText(str(a+b))
        except ValueError:
            pass


if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = Ventana()
    form.show()
    app.exec_()
