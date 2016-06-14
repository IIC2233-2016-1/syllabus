import socket
from sys import exit
from threading import Thread



class Client:

    def __init__(self, username):
        self.username = username
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
            print(message)
            if message.split(": ", 1)[1] == "exit":
                self.disconnect()

    def send_message(self, message):
        final_message = "{}: {}".format(self.username, message)
        self.socket_client.send(final_message.encode('utf-8'))

    def disconnect(self):
        print("Conexión cerrada")
        self.connection = False
        self.socket_client.close()
        exit()

if __name__ == '__main__':
    username = input("Username: ")
    client = Client(username)
    while True:
        message = input()
        client.send_message(message)
