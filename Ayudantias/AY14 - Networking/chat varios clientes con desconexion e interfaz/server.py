import socket
from sys import exit
from threading import Thread


'''
Servidor para varios clientes.
Recibe un mensaje (hear_message) y se lo reenvia a todos los clientes menos a quien lo envio
'''


class Server:

    def __init__(self, username):
        self.username = username
        # Conexión TCP con IPv4
        # AF = AddressFamily
        # AF_INET = Par (host, port) o direccion IPv4
        # SOCK = SocketKind
        # SOCK_STREAM = TCP
        # SOCK_DGRAM = UDP
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 1234
        # Coloca el software en la direccion indicada
        self.socket_server.bind((host, port))
        # Numero de conexiones "en espera"
        self.socket_server.listen(5)
        self.connections = list()

        # thread para estar constantemente aceptando clientes
        thread_accept = Thread(target=self.accept_client, args=tuple())
        thread_accept.daemon = True
        thread_accept.start()

        self.connected = True

    def accept_client(self):
        while True:
            socket_client, address = self.socket_server.accept()
            self.connections.append(socket_client)

            # para cada cliente se crea un thread que lo conecta a
            thread_messages = Thread(
                target=self.hear_messages, args=(socket_client, ))
            thread_messages.daemon = True
            thread_messages.start()

    def hear_messages(self, client):
        while self.connected:
            # recibe mensaje codificado en bytes mediante el comando
            # .recv(n) donde n = numero de bytes maximo que va a recibir
            data = client.recv(1024)
            for connection in self.connections:
                if connection is not client:
                    connection.send(data)
            print(data.decode('utf-8'))

    def send_message(self, message):
        # envia mensajes a todos los clientes.
        final_message = "{}: {}".format(self.username, message)
        for connection in self.connections:
            connection.send(final_message.encode('utf-8'))

    def disconnect(self):
        self.send_message("exit")
        self.connected = False
        self.socket_server.close()
        exit()

if __name__ == '__main__':
    username = "Admin"
    server = Server(username)
    while True:
        message = input()
        server.send_message(message)
