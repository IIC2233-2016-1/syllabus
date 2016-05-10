# <Dining philosophers problem>

import threading
import time

# Constantes:
FORKS_AMOUNT = 5
EATING_TIME = 1

# Mensajes:
not_enough_philosophers_warn = '¡Necesitamos más filósofos!'


class Philosopher(threading.Thread):
    # Mensajes:
    eat_warn = '¡{0.name} está comiendo de un rico plato de Spaghetti!'
    fork_acquired_warn = '¡{0.name} ha adquirido el tenedor {1}!'
    fork_released_warn = '¡{0.name} ha liberado el tenedor {1}!'

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.table = None
        self.forks = {'left': None, 'right': None}

    def eat(self):
        time.sleep(EATING_TIME)  # Come durante <EATING_TIME> segundo(s).
        print(Philosopher.eat_warn.format(self))

    def run(self):
        while True:
            with self.forks['left']:
                fork_acquired_left = table.forks.index(self.forks['left'])
                print(Philosopher.fork_acquired_warn.format(self, fork_acquired_left))
                with self.forks['right']:
                    fork_acquired_right = table.forks.index(self.forks['right'])
                    print(Philosopher.fork_acquired_warn.format(self, fork_acquired_right))
                    self.eat()
                    print(Philosopher.fork_released_warn.format(self, fork_acquired_right))
                print(Philosopher.fork_released_warn.format(self, fork_acquired_left))


class Table:

    def __init__(self, philosophers):
        # Creamos <FORKS_AMOUNT> tenedores.
        self.forks = [threading.Lock() for _ in range(FORKS_AMOUNT)]
        self.philosophers = philosophers

    def setup_philosophers(self):
        # Entregamos los tenedores a los filósofos.
        i = int()
        for philosopher in self.philosophers.values():
            philosopher.forks['left'] = self.forks[i]
            philosopher.forks['right'] = self.forks[i + 1 if i + 1 < len(self.forks) else 0]
            i += 1

    def start_discussion(self):
        # ¡Nuestro filósofos comienzan a discutir mientras cenan!
        for philosopher in self.philosophers.values():
            philosopher.start()


if __name__ == '__main__':
    # Creamos a los filósofos y la mesa en la que cenarán.
    names = ('Benjamín', 'Freddie', 'Antonio', 'Andrés', 'Ariel')
    philosophers = {name: Philosopher(name) for name in names}
    table = Table(philosophers)

    if FORKS_AMOUNT == len(philosophers):
        table.setup_philosophers()
        table.start_discussion()
    else:
        print(not_enough_philosophers_warn)
