import gui
from gui.variables import variables
import random


class MyInterface(gui.GameInterface):

    def piece_clicked(self, row, column, section, piece):
        piece.selected = not piece.selected
        print("{}, {} Section: {}".format(row, column, section))

    def reverse_clicked(self, clockwise):
        print(clockwise)
        gui.set_points(100)

    def piece_section_entered(self, section, piece):
        print("Section entered {}".format(section))

    def hint_asked(self):
        print("Para k kieres saber eso jaja saludos")

    def save_game(self):
        print("Save game")

gui.init()
gui.set_quality("ultra")  # low, medium, high ultra
gui.set_animations(False)
gui.set_scale(1)  # Any float different from 0
gui.set_game_interface(MyInterface())  # GUI Listener
gui.add_piece(0, 0, random.choice(variables.HEXAGON_TYPES))


gui.run()

