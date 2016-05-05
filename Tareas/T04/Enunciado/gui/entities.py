from PyQt4.QtGui import QLabel, QPixmap, QTransform, QWidget
from PyQt4.QtCore import Qt
import os

_SCALE = 0.5
_PATH = os.path.dirname(os.path.abspath(__file__))
_debugging = False


class Entity(QWidget):

    def __init__(self, base_image, parent=None):
        super().__init__(parent)
        self._base_label = QLabel(self)
        self._base_image = base_image

        self._decor_label = QLabel(self)
        self._decor_pixmap = None

        self.__pixmap = None
        """:type: PyQt4.QtGui.QPixmap"""

        self.__cord_x = 0
        self.__cord_y = 0
        self.__angle = 0
        self.setAlignment(Qt.AlignCenter)
        self.updatePixmap()

        if _debugging:
            self.setStyleSheet("border: 1px solid black")

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle
        self.updatePixmap()

    @property
    def cord_x(self):
        return self.__cord_x

    @cord_x.setter
    def cord_x(self, cord):
        self.__cord_x = cord
        self.move(self.cord_x, self.cord_y)

    @property
    def cord_y(self):
        return self.__cord_y

    @cord_y.setter
    def cord_y(self, cord):
        self.__cord_y = cord
        self.move(self.cord_x, self.cord_y)

    def add_decoration(self, path):
        if path is None:
            self._decor_label.hide()
        else:
            self._decor_label = QLabel(self)
            self._decor_pixmap = QPixmap(path)
            self._decor_pixmap = self._decor_pixmap.scaled(self._decor_pixmap.width() * _SCALE,
                                                           self._decor_pixmap.height() * _SCALE)
            self._decor_pixmap = self._decor_pixmap.transformed(QTransform().rotate(self.angle))
            self._decor_label.setPixmap(self._decor_pixmap)

    def updatePixmap(self):
        path = _PATH + os.sep + "assets" + os.sep + self._base_image
        self.__pixmap = QPixmap(path)
        self.__pixmap = self.__pixmap.scaled(self.__pixmap.width()*_SCALE, self.__pixmap.height()*_SCALE)
        self.__pixmap = self.__pixmap.transformed(QTransform().rotate(self.angle))
        self._base_label.setPixmap(self.__pixmap)
        self.setFixedSize(self.__pixmap.width(), self.__pixmap.height())

    def setFixedSize(self, x, y):
        super().setFixedSize(x, y)
        self._base_label.setFixedSize(x, y)

    def setAlignment(self, alignment):
        self._base_label.setAlignment(alignment)
        self._decor_label.setAlignment(alignment)


class Human(Entity):

    BRAVE = "brave"
    COWARD = "coward"
    CARELESS = "careless"
    CAUTIOUS = "cautious"
    RATIONAL = "rational"
    STUPID = "stupid"

    WEAPON_LONG = "long"
    WEAPON_SHORT = "short"
    NO_WEAPON = "noweapon"

    def __init__(self, personality, weapon, cord_x=0, cord_y=0, parent=None):
        super().__init__("human_{}_{}.png".format(personality, weapon), parent=parent)
        self.personality = personality
        self.weapon = weapon
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.setFixedSize(73 * _SCALE, 73 * _SCALE)

    def change_weapon(self, weapon):
        self.weapon = weapon
        self._base_image = "human_{}_{}.png".format(self.personality, self.weapon)
        self.updatePixmap()

    def updatePixmap(self):
        path = _PATH + os.sep + "assets" + os.sep + self._base_image
        self.__pixmap = QPixmap(path)
        self.__pixmap = self.__pixmap.scaled(self.__pixmap.width() * _SCALE, self.__pixmap.height() * _SCALE)
        self.__pixmap = self.__pixmap.transformed(QTransform().rotate(self.angle))
        self._base_label.setPixmap(self.__pixmap)


class Zombie(Entity):

    def __init__(self, cord_x=0, cord_y=0, parent=None):
        super().__init__("zombie.png", parent=parent)
        self.cord_x = cord_x
        self.cord_y = cord_y
        self.setFixedSize(73 * _SCALE, 73 * _SCALE)


class Bullet(Entity):

    def __init__(self, cord_x=0, cord_y=0, parent=None):
        super().__init__("bullet.png", parent=parent)
        self.cord_x = cord_x
        self.cord_y = cord_y


class Building(Entity):

    def __init__(self, cord_x=0, cord_y=0, parent=None):
        super().__init__("building.png", parent=parent)
        self.cord_x = cord_x
        self.cord_y = cord_y


class GunShopLong(Entity):

    def __init__(self, cord_x=0, cord_y=0, parent=None):
        super().__init__("gun_shop_long.png", parent=parent)
        self.cord_x = cord_x
        self.cord_y = cord_y


class GunShopShort(Entity):

    def __init__(self, cord_x=0, cord_y=0, parent=None):
        super().__init__("gun_shop_short.png", parent=parent)
        self.cord_x = cord_x
        self.cord_y = cord_y