from collections import deque


# # # # #
# Modelo
# # # # #


class Pizza:
    _id = 0

    def __init__(self):
        self.id_pizza = Pizza._id
        Pizza._id += 1


class Horno:

    def __init__(self):
        # Tiempo de coccion es contante
        self.tiempo_coccion = 10

        self.pizza_horneandose = None
        self.tiempo_fin_coccion = None

    @property
    def ocupado(self):
        return self.pizza_horneandose is not None


# # # # # # # # # # # #
# Simulacion Sincrona
# # # # # # # # # # # #


class PizzeriaSincrona:

    def __init__(self):

        # Tiempos relevantes
        self.tiempo_actual = 0
        self.tiempo_fin_simulacion = 100
        self.llegada_prox_pedido = 0
        # Elementos de la simulacion
        self.horno = Horno()
        self.cola_pizzas = deque()

    def run_simulacion_sincrona(self):

        # Simulacion Sincrona:
        # MIENTRAS el tiempo simulacion no termine
        #   aumentar tiempo en una unidad
        #   SI ocurren eventos en este intervalo de tiempo:
        #       simular los eventos
        while self.tiempo_actual < self.tiempo_fin_simulacion:

            if self.tiempo_actual == self.llegada_prox_pedido:
                # Si AHORA llega un pedido
                nueva_pizza = Pizza()
                self.cola_pizzas.append(nueva_pizza)
                self.llegada_prox_pedido += 7

                print('[{}]: Llega pedido numero {}'.format(
                    self.tiempo_actual, nueva_pizza.id_pizza))

            if self.horno.tiempo_fin_coccion == self.tiempo_actual:
                # Si AHORA termina la coccion de una pizza
                print('[{}]: Sale pizza {} del horno'.format(
                    self.tiempo_actual, self.horno.pizza_horneandose.id_pizza))
                self.horno.pizza_horneandose = None

            if not self.horno.ocupado:
                # Si el horno NO esta ocupado
                pizza_al_horno = self.cola_pizzas.popleft()
                self.horno.pizza_horneandose = pizza_al_horno
                self.horno.tiempo_fin_coccion = self.tiempo_actual + self.horno.tiempo_coccion

                print('[{}]: Entra pizza {} al horno'.format(
                    self.tiempo_actual, pizza_al_horno.id_pizza))

            # Termino este periodo y paso al siguiente
            self.tiempo_actual += 1


# # # # # # # # # # # #
# Simulacion Discreta
# # # # # # # # # # # #


class PizzeriaDiscreta:

    def __init__(self):

        # Tiempo relevantes
        self.tiempo_actual = 0
        self.tiempo_fin_simulacion = 100
        self.llegada_prox_pedido = 0
        # Elementos de la simulacion
        self.horno = Horno()
        self.cola_pizzas = deque()

    @property
    def prox_evento(self):
        # si el horno esta desocupado, el tiempo_fin_coccion es de la ultima vez que se uso (por ende ya habria pasado)
        # si el horno esta ocupado el tiempo_fin_coccion es mayor al tiempo
        # actual
        if self.horno.ocupado:
            if self.llegada_prox_pedido > self.horno.tiempo_fin_coccion:
                return self.horno.tiempo_fin_coccion
        return self.llegada_prox_pedido

    def run_simulacion_discreta(self):

        # Simulacion Discreta:
        # MIENTRAS la lista de eventos no este vacia y el tiempo de simulacion no termine
        #   tomar un evento desde el principio de la lista de eventos
        #   avanzar el tiempo de simulacion al tiempo del evento
        #   simular el evento
        while self.tiempo_actual < self.tiempo_fin_simulacion:

            if self.tiempo_actual == self.llegada_prox_pedido:
                # Si AHORA llega un pedido
                nueva_pizza = Pizza()
                self.cola_pizzas.append(nueva_pizza)
                self.llegada_prox_pedido += 7
                print('[{}]: LLega pedido numero {}'.format(
                    self.tiempo_actual, nueva_pizza.id_pizza))

            if self.horno.tiempo_fin_coccion == self.tiempo_actual:
                # Si AHORA termina la coccion de una pizza
                print('[{}]: Sale pizza {} del horno'.format(
                    self.tiempo_actual, self.horno.pizza_horneandose.id_pizza))
                self.horno.pizza_horneandose = None

            if not self.horno.ocupado:
                # Si el horno NO esta ocupado
                pizza_al_horno = self.cola_pizzas.popleft()
                self.horno.pizza_horneandose = pizza_al_horno
                self.horno.tiempo_fin_coccion = self.tiempo_actual + self.horno.tiempo_coccion

                print('[{}]: Entra pizza {} al horno'.format(
                    self.tiempo_actual, pizza_al_horno.id_pizza))

            self.tiempo_actual = self.prox_evento

if __name__ == '__main__':

    print('------------Simulacion sincrona----------')
    pizzeria_sincrona = PizzeriaSincrona()
    pizzeria_sincrona.run_simulacion_sincrona()

    print('\n\n')

    print('------------Simulacion discreta-----------')
    pizzeria_discreta = PizzeriaDiscreta()
    pizzeria_discreta.run_simulacion_discreta()
