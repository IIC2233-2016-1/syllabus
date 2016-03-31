from .game_interface import GameInterface


class VariableHolder:

    def __init__(self):
        self.QUALITY = "low"
        self.ANIMATIONS = True
        self.TOTAL_TICKS = {
            "low": 5,
            "medium": 10,
            "high": 20,
            "ultra": 40
        }
        self.TICKS_INTERVAL = {
            "low": 200,
            "medium": 100,
            "high": 50,
            "ultra": 30,
        }
        self.SCALE = 1
        self.GAME_INTERFACE = GameInterface()
        self.STAR_SIZE = 40
        self.TYPES = ["red", "purple", "green", "yellow", "blue", "star_red", "star_purple", "star_green",
                      "star_yellow", "star_blue", "star", "mirror", "black_pearl", "bomb_red",
                      "bomb_purple", "bomb_green", "bomb_yellow", "bomb_blue"]
        self.HEXAGON_TYPES = ["red", "purple", "green", "yellow", "blue"]
        self.STAR_HEXAGON_TYPES = ["star_red", "star_purple", "star_green", "star_yellow", "star_blue"]
        self.BOMB_TYPES = ["bomb_red", "bomb_purple", "bomb_green", "bomb_yellow", "bomb_blue"]
        self.SPECIAL_PIECES = ["star", "mirror", "black_pearl"]


variables = VariableHolder()
