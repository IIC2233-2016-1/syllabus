from collections import deque
from random import uniform, expovariate


# # # # #
# Modelo
# # # # #


class Pizza:
    _id = 0

    def __init__(self):
        self.id_pizza = Pizza._id
        Pizza._id += 1


class Horno:
    _id = 1

    def __init__(self):
        # Diferenciar hornos
        self.id_horno = Horno._id

        self.pizza_horneandose = None
        self.tiempo_fin_coccion = None

        Horno._id += 1

    @property
    def ocupado(self):
        return self.pizza_horneandose is not None

    def nuevo_tiempo_coccion(self, tiempo_actual):
        # Le agregamos variabilidad a los tiempos
        self.tiempo_fin_coccion = tiempo_actual + round(uniform(10, 17))


class Telefono:
    _id = 1

    def __init__(self, tasa):
        # Mas variabilidad
        self._tasa = tasa
        self.prox_pedido = round(expovariate(self._tasa))

        self.id_telefono = Telefono._id
        Telefono._id += 1

    def nuevo_prox_pedido(self):
        # Otra vez dependemos de una distribucion aleatoria
        self.prox_pedido += round(expovariate(self._tasa))


# # # # # # # # # # # #
# Simulacion Discreta
# # # # # # # # # # # #


class PizzeriaDiscreta:

    def __init__(self):

        # Tiempos relevantes
        self.tiempo_actual = 0
        self.tiempo_fin_simulacion = 100
        # Elementos de la simulacion
        self.hornos = [Horno(), Horno()]
        self.cola_pizzas = deque()
        self.telefonos = [Telefono(1 / 15), Telefono(1 / 10)]

    @property
    def prox_horno_desocupado(self):
        # Tiempos en que los hornos estaran desocupados
        return [horno.tiempo_fin_coccion for horno in self.hornos if horno.ocupado]

    @property
    def llegada_prox_pedido(self):
        # Tiempos en que lelgaran los proximos pedidos
        return [telefono.prox_pedido for telefono in self.telefonos]

    @property
    def prox_evento(self):
        # El tiempo del proximo evento
        _prox_evento = self.llegada_prox_pedido + self.prox_horno_desocupado
        return min(_prox_evento)

    def run_simulacion_discreta(self):

        # Simulacion Discreta:
        # MIENTRAS la lista de eventos no este vacia y el tiempo de simulacion no termine
        #   tomar un evento desde el principio de la lista de eventos
        #   avanzar el tiempo de simulacion al tiempo del evento
        #   simular el evento
        while self.tiempo_actual < self.tiempo_fin_simulacion:

            # Revisamos si el proximo evento...
            for telefono in self.telefonos:
                # ... corresponde a que llegue un pedido
                if self.tiempo_actual == telefono.prox_pedido:
                    # Si AHORA llega un pedido
                    nueva_pizza = Pizza()
                    self.cola_pizzas.append(nueva_pizza)
                    telefono.nuevo_prox_pedido()
                    print('[{}]: Llega pedido numero {} al telefono {}'.format(
                        self.tiempo_actual, nueva_pizza.id_pizza, telefono.id_telefono))

            # Revisamos si el proximo evento...
            for horno in self.hornos:
                # ... corresponde a que termine la coccion de una pizza
                if horno.tiempo_fin_coccion == self.tiempo_actual:
                    print('[{}]: Sale pizza {} del horno {}'.format(
                        self.tiempo_actual, horno.pizza_horneandose.id_pizza, horno.id_horno))
                    horno.pizza_horneandose = None

            # Revisamos si ...
            for horno in self.hornos:
                # ... tenemos un horno desocupado
                if not horno.ocupado:
                    if len(self.cola_pizzas) > 0:
                        pizza_al_horno = self.cola_pizzas.popleft()
                        horno.pizza_horneandose = pizza_al_horno
                        horno.nuevo_tiempo_coccion(self.tiempo_actual)
                        print('[{}]: Entra pizza {} al horno {}'.format(
                            self.tiempo_actual, pizza_al_horno.id_pizza, horno.id_horno))

            # Avanzamos en el tiempo hasta el proximo evento
            self.tiempo_actual = self.prox_evento

if __name__ == '__main__':

    print('------------Simulacion discreta-----------')
    pizzeria_discreta = PizzeriaDiscreta()
    pizzeria_discreta.run_simulacion_discreta()
