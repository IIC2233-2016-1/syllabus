import time
from gui.entities import Human, Zombie, Bullet, Building, GunShopLong, GunShopShort
import gui
import random
import math


gui.init()
human = Human(Human.COWARD, Human.NO_WEAPON, cord_x=100, cord_y=100)
human.add_decoration("gui/assets/bullet.png")
zombie = Zombie()
human.angle = 0
ticks = 0


def tick():
    human.cord_x += 1
    human.cord_y += 1
    human.angle += 1

zombies = []
for i in range(20):
    zombie = Zombie(cord_x=random.randint(0, 800), cord_y=random.randint(0, 800))
    gui.add_entity(zombie)
    zombies.append(zombie)


gui.add_entity(human)
gui.add_entity(zombie)
gui.add_entity(GunShopLong(100, 200))
gui.add_entity(GunShopShort(300, 300))
gui.add_entity(Building(300, 200))
gui.add_entity(Bullet(50, 50))
gui.run(tick, 50)
