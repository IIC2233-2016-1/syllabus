__author__ = 'Florencia Barrios, Maria Jose Hidalgo'

class Sistema:

    usuarios = {}
    productos_venta = {}
    contador_compras = 0

    def login(self, user, passw, rut):

        rut_valido = self.rut_valido(rut)
        if rut_valido:
            usuario_existe = self.revisar_usuario(user, passw, rut)
            if usuario_existe:
                print("Bienvenido(a) {}! Ya ha ingresado al sistema.".format(user))
                return True
            else:
                print("Usuario o clave incorrectas.")
                return False
        else:
            print("Rut invalido.")
            return False

    def rut_valido(self, rut):

        l = [3, 2, 7, 6, 5, 4, 3, 2]
        digitos, verificador = rut.split("-")
        digitos = list(digitos)

        if len(digitos) == 8:
            suma_digitos = sum(map(lambda a: a[0] * a[1], zip(l, digitos)))
            resto = suma_digitos % 11
            dif = 11 - resto
            if dif == 11:
                digito_verificador = 0
            elif dif == 10:
                digito_verificador = "K"
            else:
                digito_verificador = dif

            if digito_verificador == int(verificador):
                return True
            else:
                return False
        else:
            return False

    def revisar_usuario(self, user, passw, rut):

        passord = Sistema.usuarios[rut].password
        usuario = Sistema.usuarios[rut].user

        if passord == passw and usuario == user:
            return True
        else:
            return False

    def crear_cuenta(self, user):

        Sistema.usuarios.update({user.rut: user})

    def busqueda(self, nombre_producto):

        contador = 0

        for id in Sistema.productos_venta:
            if Sistema.productos_venta[id][0].nombre == nombre_producto:
                contador += 1

        print("Se han encontrado {} productos del tipo {}.".format(contador, nombre_producto))
        return contador

    @classmethod
    def vender_producto_a_comprador(self, descuento, id, user):

        # 1 = 0% descuento, 0.7 = 30% descuento, 0 = 100% descuento

        producto, dueño = Sistema.productos_venta[id]
        precio = producto.precio

        if user.dinero >= precio:
            user.dinero -= precio * descuento
            for vendedor in Sistema.usuarios.values():
                if vendedor.user == dueño.user:
                    Sistema.contador_compras += 1
                    dueño.dinero += precio * descuento
                    dueño.productos[producto.id] = producto
                    del Sistema.productos_venta[id]
                    print("Ha comprado el producto: {}".format(producto.nombre))

                    return True, (dueño, producto, descuento)

            else:
                return False, None

        else:
            print("Saldo insuficiente.")
            return False, None

    @classmethod
    def agregar_producto_en_venta(self, producto, id, user):

        print("Puso en venta el producto {} en ${} pesos".format(producto.nombre, producto.precio))
        Sistema.productos_venta.update({id: (producto, user)})

        return Sistema.productos_venta

class Usuario:

    def __init__(self, user, email, dinero, password, productos, rut):
        self.user = user
        self.password = password
        self.email = email
        self.dinero = dinero
        self.productos = {producto.id: producto for producto in productos}
        self._calificacion = []
        self.rut = rut

    @property
    def calificacion(self):

        x = sum(self._calificacion) / len(self._calificacion)
        return x

    def vender_producto(self, id):

        producto = self.productos[id]

        return Sistema.agregar_producto_en_venta(producto, id, self)

    def comprar_producto(self, id, descuento):

        return Sistema.vender_producto_a_comprador(descuento, id, self)

    def calificar_user(self, user, nota):

        user._calificacion.append(nota)
        print("Se ha calificado a {} con nota {}.".format(user.user, nota))
        return user._calificacion

    def generar_orden_de_compra(self, producto, descuento, name):

        des = int(1 - descuento) * 100

        with open(name, "w") as orden:
            orden.write("Orden de compra para el producto: {}\n".format(producto.nombre))
            orden.write("-" * 40)
            orden.write("\nId del producto: {0.id}\n"
                        "Precio del producto: {0.precio}\n"
                        "Descuento aplicado: {1}%\n"
                        "Total: {0.precio}\n".format(producto, des))

            orden.write("Nombre: {0.user}\nRut : {0.rut}".format(self))


class Producto:

    id = 0

    def __init__(self, precio, nombre):
        self.id = Producto.id
        self.precio = precio
        self.nombre = nombre
        Producto.id += 1

"""
NO MODIFICAR DESDE AQUI
"""

if __name__ == '__main__':

    sistema = Sistema()

    usuario_1 = Usuario("cotehidalgov", "mjhidalgo@uc.cl",
                        20000, 831,
                        [Producto(3990, "estuche"),
                         Producto(5900, "polera")],
                        "18345763-2")

    usuario_2 = Usuario("fbarrios1", "fbarrios1@uc.cl",
                        20000, 123,
                        [Producto(345, "lapiz pasta"),
                         Producto(15000, "vestido")],
                        "19234665-7")

    usuario_3 = Usuario("jperez", "jperez@uc.cl",
                        20000, 345,
                        [],
                        182346653)

    sistema.crear_cuenta(usuario_1)

    if sistema.login(usuario_1.user, usuario_1.password, usuario_1.rut):

        usuario_1.vender_producto(2)
        usuario_1.vender_producto(0)
        usuario_1.vender_producto(1)
        result_1, datos_1 = usuario_1.comprar_producto(2, 0.7)

        if result_1:
            user, producto, descuento = datos_1
            usuario_1.calificar_user(user, 6)
            usuario_1.generar_orden_de_compra(producto,
                                              descuento,
                                              "Orden de compra {}.txt".format(sistema.contador_compras))

    print("La calificación de {} es: {}".format(usuario_1.user, usuario_1.calificacion))

    sistema.login(usuario_2.user, usuario_2.password, usuario_2.rut)
    sistema.login(usuario_3.user, usuario_3.password, usuario_3.rut)
    usuario_3.rut = "182346653"
    sistema.login(usuario_3.user, usuario_3.password, usuario_3.rut)
    sistema.crear_cuenta(usuario_2)

    if sistema.login(usuario_2.user, usuario_2.password, usuario_2.rut):

        usuario_2.vender_producto(2)

        result_2, datos_2 = usuario_2.comprar_producto(0, "30")

        if result_2:
            user_2, producto_2, descuento_2 = datos_2
            usuario_2.calificar_user(user_2, "A")
            usuario_2.generar_orden_de_compra(producto_2,
                                              descuento_2,
                                              "Orden de compra {}.txt".format(sistema.contador_compras))

        result_3, datos_3 = usuario_2.comprar_producto(0, 0.3)

        if result_3:
            user_3, producto_3, descuento_3 = datos_3
            usuario_2.calificar_user(user_3, "A")
            usuario_2.generar_orden_de_compra(producto_3,
                                              descuento_3,
                                              "Orden de compra {}.txt".format(sistema.contador_compras))

        result_4, datos_4 = usuario_2.comprar_producto(1, 1)

        if result_4:
            user_4, producto_4, descuento_4 = datos_4
            usuario_2.calificar_user(user_4, 2)
            usuario_2.generar_orden_de_compra(producto_4,
                                              descuento_4,
                                              "Orden de compra {}.txt".format(sistema.contador_compras))

        usuario_2.vender_producto(3)

    print("La calificación de {} es: {}".format(usuario_1.user, usuario_1.calificacion))
