# NO PUEDES MODIFICAR NINGUNA DE LAS SIGUIENTES CLASES Y FUNCIONES.
# SOLO PUEDES DECORARLAS.


class Product:

    def __init__(self, name, price, stock):
        self.name = name
        self._price = price
        self._stock = stock

    def IncreasePrice(self, amount):
        self._price += amount

    def sell(self, amount=1):
        self._stock -= amount
        print("Se vendieron {0} productos en ${1}"
              .format(amount, amount * self.final_price))

    def ChangePrice(self, new_price):
        print("Has accedido a un metodo que debiese ser privado")
        self._price = new_price

    @property
    def FinalPrice(self):
        return self._price * 1.08


if __name__ == "__main__":
    ej = Product("Auto", 1000000, 100)
    print("IncreasePrice: 'hola'(str)")
    ej.increase_price('hola')
    print("Precio: {}".format(ej.final_price))
    print()

    print("IncreasePrice: 100(int)")
    ej.increase_price(100)
    print("Precio: {}".format(ej.final_price))
