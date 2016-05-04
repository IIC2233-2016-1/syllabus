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

        # Vamos guardando los datos que nos interesan
        self.tiempo_in = 0
        self.tiempo_out = 0

    @property
    def duracion_pedido(self):
        # Properties FTW
        if self.tiempo_in and self.tiempo_out:
            return self.tiempo_out - self.tiempo_in
        return None


class Horno:
    _id = 1

    def __init__(self):
        # Aun necesitamos diferenciar hornos
        self.id_horno = Horno._id

        self.tiempo_fin_coccion = None
        self.pizza_horneandose = None

        Horno._id += 1

    @property
    def ocupado(self):
        return self.pizza_horneandose is not None

    def nuevo_tiempo_coccion(self, tiempo_actual):
        self.tiempo_fin_coccion = tiempo_actual + round(uniform(10, 17))


class Telefono:
    _id = 1

    def __init__(self, tasa):
        self._tasa = tasa
        self.prox_pedido = round(expovariate(self._tasa))

        self.id_telefono = Telefono._id
        Telefono._id += 1

    def nuevo_prox_pedido(self):
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
        # Ahora nos interesa llevar un registro
        self.pedidos_terminados = []

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
                    nueva_pizza.tiempo_in = self.tiempo_actual
                    self.cola_pizzas.append(nueva_pizza)
                    telefono.nuevo_prox_pedido()
                    print('[{}]: Llega pedido numero {} al telefono {}'.format(
                        self.tiempo_actual, nueva_pizza.id_pizza, telefono.id_telefono))

            # Revisamos si el proximo evento ...
            for horno in self.hornos:
                # ... corresponde a que termine la coccion de una pizza
                if horno.tiempo_fin_coccion == self.tiempo_actual:
                    # Guardamos la informacion relevante
                    pizza_saliendo = horno.pizza_horneandose
                    pizza_saliendo.tiempo_out = self.tiempo_actual
                    self.pedidos_terminados.append(pizza_saliendo)
                    print('[{}]: Sale pizza {} del horno {}'.format(
                        self.tiempo_actual, pizza_saliendo.id_pizza, horno.id_horno))
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

    def estadisticas(self):
        # Aqui mostraremos toda la informacion que nos podria interesar
        tiempo_pizzas_terminadas = list(
            map(lambda pizza: pizza.duracion_pedido, self.pedidos_terminados))
        print('CANTIDAD DE PEDIDOS TERMINADOS: {}'.format(
            len(tiempo_pizzas_terminadas)))
        print('MINIMO TIEMPO: {}'.format(min(tiempo_pizzas_terminadas)))
        print('MAXIMO TIEMPO: {}'.format(max(tiempo_pizzas_terminadas)))
        print('PROMEDIO TIEMPO: {}'.format(
            sum(tiempo_pizzas_terminadas) / len(tiempo_pizzas_terminadas)))

        pizzas_no_terminadas = list(self.cola_pizzas)
        for horno in self.hornos:
            if horno.pizza_horneandose:
                pizzas_no_terminadas.append(horno.pizza_horneandose)
        print('CANTIDAD DE PEDIDOS NO TERMINADOS: {}'.format(
            len(pizzas_no_terminadas)))

if __name__ == '__main__':

    print('------------Simulacion discreta-----------')
    pizzeria_discreta = PizzeriaDiscreta()
    pizzeria_discreta.run_simulacion_discreta()

    print('\n\n')

    print('------------Estadisticas Simulacion-----------')
    pizzeria_discreta.estadisticas()
