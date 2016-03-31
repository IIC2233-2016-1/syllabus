from PyQt4.QtGui import QApplication
from .game_interface import GameInterface
from .variables import variables
from .game import Game

__game = None
""" :type: Game"""

__app = None


def set_quality(quality):
    if quality in ["low", "medium", "high", "ultra"]:
        variables.QUALITY = quality
    else:
        raise Exception("Valores validos: low, medium, high y ultra")


def set_animations(animations):
    if isinstance(animations, bool):
        variables.ANIMATIONS = animations
    else:
        raise TypeError("bool expected")


def set_scale(scale):
    if (isinstance(scale, float) or isinstance(scale, int)) and not isinstance(scale, bool):
        variables.SCALE = scale
    else:
        raise TypeError("float expected")


def set_points(points):
    __game.setPoints(points)


def add_piece(i, j, piece_type=None, on_move_ended=None, number=5):
    __game.addPiece(i, j, piece_type, on_move_ended, number)


def get_piece(i, j):
    return __game.getPiece(i, j)


def pop_piece(i, j):
    return __game.popPiece(i, j)


def move_piece(i, j, piece, on_move_ended=None):
    __game.movePiece(i, j, piece, on_move_ended)


def set_game_interface(_game_interface):
    if isinstance(_game_interface, GameInterface):
        variables.GAME_INTERFACE = _game_interface
    else:
        raise TypeError("GameInterface class expected")


def init():
    global __game, __app
    __app = QApplication([])
    __game = Game()
    __game.initUi()


def run():
    global __game, __app
    __game.show()
    __app.exec()

