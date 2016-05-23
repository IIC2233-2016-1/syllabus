''' Pochamon Thread Example '''

import threading
from time import sleep
from random import choice
from abc import ABCMeta, abstractmethod

# Pochamon hereda de thread y ademas es una clase abstracta
class Pochamon(threading.Thread, metaclass=ABCMeta):

    def __init__(self, name, hp, stamina, attacks):
        super().__init__()
        self.name = name
        self.hp = hp
        self.stamina = stamina
        self.max_stamina = stamina
        self.attacks = attacks
        self.enemy = None

    def find_enemy(self, enemy):
        self.enemy = enemy

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def rest(self):
        pass

# TrainedPochamon hereada de Pochamon (Que era abstracta), y se convierte en un thread.
class TrainedPochamon(Pochamon):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Cuando hacemos nombre_thread.start(), el metodo busca el metodo run() para ejecutarlo
    def run(self):

        while True:
            if self.hp > 0 and self.enemy.hp > 0:
                self.attack() if self.stamina > 0 else self.rest()
            elif self.hp < 0:
                print("{0} Ha sido derrotado y humillado por {1}! :D".format(self.name, self.enemy.name))
                break
            elif self.enemy.hp < 0:
                print("{0} Ha muerto de una manera brutal! :D, {1} es un pochamon increible!".format(self.enemy.name, self.name))
                break

    def attack(self):
        next_attack = choice(self.attacks)
        print("{0} [hp:{1} stamina:{2}] ataca a {3} con {4}".format(self.name, self.hp, self.stamina, self.enemy.name, next_attack[0]))
        self.enemy.hp -= next_attack[1]
        print("A {0} le quedan {1} puntos de vida".format(self.enemy.name, self.enemy.hp))
        self.stamina -= next_attack[1]
        sleep(2)

    def rest(self):
        print("{} esta descansando".format(self.name))
        sleep(5)
        self.stamina = self.max_stamina
        if self.hp > 0:
            print ("{} recupera su máxima stamina y está listo para seguir peleando".format(self.name))


attacks1 = [
    ("Sexy Naked Dance", 30),
    ("Fus Ro Dah", 80),
    ("Pocket Nuke", 100),
    ("Onda vital coñooo", 150)
    ]

attacks2 = [
    ("Saitama's Absolutly Normal Punch", 30),
    ("Sasha Grey's Scream", 80),
    ("A Fcking Minigun", 100),
    ("Midterm Programación Avanzada", 150)
    ]

# Instanciamos nuestros threads
pochamon1 = TrainedPochamon(name="ThuuBhenjithaaax", hp=469, stamina=400, attacks=attacks1)
pochamon2 = TrainedPochamon(name="Flooryh", hp=666, stamina=200, attacks=attacks2)


print("Daedalus reta a Antonio a un combate Pochamon!")
print("Daedalus: {} Yo te elijo".format(pochamon1.name))
print("Antonio: {} Yo te elijo".format(pochamon2.name))
pochamon1.find_enemy(pochamon2)
pochamon2.find_enemy(pochamon1)
sleep(2)

print("FIGHT!!")

#Se busca al metodo run de cada uno de los objetos
pochamon1.start()
pochamon2.start()
