import socket
import threading
import sys
import pickle
from time import sleep

'''
Chat que envia objetos...
'''


class SuperMensaje:
    _id = 1

    def __init__(self, texto):
        self.texto = texto
        self.id = SuperMensaje._id
        self.remitente = None
        SuperMensaje._id += 1

    def __setstate__(self, state):
        # notar que para obtener un atributo de la instancia
        # se tiene que usar el diccionario 'state' que recibe
        print("Se esta deserializando el Mensaje {} ".format(state["id"]))
        self.__dict__ = state

    def __getstate__(self):
        dict_clase = self.__dict__.copy()
        print("Se está serializando el Mensaje {}".format(self.id))
        return dict_clase


class Cliente:

    def __init__(self, usuario):
        self.usuario = usuario
        self.host = '127.0.0.1'
        self.port = 3491
        self.mensaje = None
        self.s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Un cliente se puede conectar solo a un servidor.
            self.s_cliente.connect((self.host, self.port)) # El cliente revisa que el servidor esté disponible
            # Una vez que se establece la conexión, se pueden recibir mensajes
            recibidor = threading.Thread(target=self.recibir_mensajes, args=())
            recibidor.daemon = True
            recibidor.start()
        except socket.error:
            print("No fue posible realizar la conexión")
            sys.exit()

    def recibir_mensajes(self):
        while True:
            data = self.s_cliente.recv(1024)
            obj_mensaje = pickle.loads(data)
            print("Mensaje {} recibido: {}".format(obj_mensaje.id, obj_mensaje.texto))

    def enviar(self, mensaje):
        mns_final = pickle.dumps(mensaje)
        self.s_cliente.send(mns_final)
        print("Se envia el mensaje al servidor")


class Servidor:

    def __init__(self, usuario, num_clients=2):
        self.usuario = usuario
        self.host = '127.0.0.1'
        self.port = 3491
        self.s_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_servidor.bind((self.host, self.port))
        self.s_servidor.listen(num_clients)
        self.clientes = []

        thread_aceptar = threading.Thread(target=self.aceptar, args=())
        thread_aceptar.daemon = True
        thread_aceptar.start()

    def aceptar(self):
        while True:
            cliente_nuevo, address = self.s_servidor.accept()
            self.clientes.append(cliente_nuevo)
            thread_mensajes = threading.Thread(target=self.reenviar_mensajes, args=(cliente_nuevo,))
            thread_mensajes.daemon = True
            thread_mensajes.start()

    def reenviar_mensajes(self, cliente):
        while True:
            data = cliente.recv(1024)
            print("Servidor deserializa mensaje para ver su id")
            mensaje = pickle.loads(data)
            # notar que podemos llamar a los atributos y metodos del SuperMensaje
            # en este caso llamamos a mensaje.id
            print("Mensaje {} ha llegado al servidor".format(mensaje.id))
            msn_final = pickle.dumps(mensaje)
            print("Servidor reenvia mensaje\n\n")
            for c in self.clientes:
                if c is not cliente:
                    c.send(msn_final)


if __name__ == "__main__":

    pick = input("Ingrese S si quiere ser servidor o C si desea ser cliente: ")
    if pick == "S":
        nombre = "Admin"
        server = Servidor(nombre, num_clients=2)

        # el siguiente while true es para mantener vivo el programa principal del servidor
        while True:
            sleep(1)

    else:
        nombre = input("Ingrese el nombre del usuario: ")
        client = Cliente(nombre)
        while True:
            texto = input()
            mensaje = SuperMensaje(texto)
            client.enviar(mensaje)
