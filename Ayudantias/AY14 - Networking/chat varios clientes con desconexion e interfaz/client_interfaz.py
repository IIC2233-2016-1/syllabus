import socket
from sys import exit
from threading import Thread
from PyQt4 import QtGui, uic


'''
Interfaz de chat de un cliente.
'''


# Cargamos la interfaz creada mediante QTDesigner
formulario = uic.loadUiType("cliente.ui")


class ClientWindow(formulario[0], formulario[1]):

    # Ventana para poner el chat actual dado un usuario.
    # los mensajes se van agregando a un QListWidget.

    def __init__(self, usuario):
        super().__init__()
        self.setupUi(self)

        # usuario es una QLabel
        self.usuario.setText("USUARIO: {}".format(usuario))

        self.input.setText("Escriba mensaje...")
        self.enter.clicked.connect(self.enviar_mensaje)

        # creamos el cliente...
        self.cliente = Client(username=username, window=self)

    def enviar_mensaje(self):
        message = self.input.text()
        if message != "":
            self.cliente.send_message(message)
            self.input.setText("")

    def agregar_mensaje_enviado(self, mensaje):
        # creo una "fila" para agregar a la QListWidget
        item = QtGui.QListWidgetItem(mensaje)
        # agrego color al fondo de la fila
        item.setBackgroundColor(QtGui.QColor(180, 220, 255))
        self.conversacion.addItem(item)

    def agregar_mensaje_recibido(self, mensaje):
        # creo una "fila" para agregar a la QListWidget
        item = QtGui.QListWidgetItem(mensaje)
        # agrego color al fondo de la fila
        item.setBackgroundColor(QtGui.QColor(135, 255, 155))
        self.conversacion.addItem(item)


class Client:

    def __init__(self, username, window):
        self.username = username
        self.window = window

        host = socket.gethostname()
        port = 1234
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = True
        try:
            # Un cliente se puede conectar solo a un servidor
            self.socket_client.connect((host, port))
            # Nos conectamos al servidor (a.k.a receiver)
            receiver = Thread(target=self.hear_messages)
            receiver.daemon = True
            receiver.start()

        except socket.error:
            print("No fue posible realizar la conexión")
            exit()

    def hear_messages(self):
        while self.connection:
            data = self.socket_client.recv(1024)
            message = data.decode('utf-8')

            self.window.agregar_mensaje_recibido(message)

            if message.split(": ", 1)[1] == "exit":
                self.disconnect()

    def send_message(self, message):
        final_message = "{}: {}".format(self.username, message)
        self.socket_client.send(final_message.encode('utf-8'))
        self.window.agregar_mensaje_enviado(final_message)

    def disconnect(self):
        print("Conexión cerrada")
        self.connection = False
        self.socket_client.close()
        exit()


if __name__ == '__main__':
    username = input("Username: ")

    app = QtGui.QApplication([])
    window = ClientWindow(username)
    window.show()
    app.exec_()



