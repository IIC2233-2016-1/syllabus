import math
import os
import random
import sip

from PyQt4.QtGui import QFont, QLabel, QPixmap, QWidget
from PyQt4.QtCore import Qt, QEvent, QTimer
from .variables import variables


PATH = os.path.dirname(os.path.abspath(__file__))


class Piece(QWidget):

    def __init__(self, type, parent=None):
        super().__init__(parent)
        self.__type = type
        self.setFixedSize(100*variables.SCALE, 91*variables.SCALE)
        self.__section = 7
        self.main_label = QLabel(self)
        self._pixmap = None
        self._selected_pixmap = None
        self.__timer = None
        self.__selected = False
        self.setMouseTracking(True)
        self.__init_main_label()

    def __init_main_label(self):
        if "star_" in self.__type:
            self._pixmap = QPixmap(PATH + os.sep + "assets" + os.sep + "{}.png".format(self.__type[5:]))\
                .scaled(100*variables.SCALE, 91*variables.SCALE, Qt.KeepAspectRatio)
            self._selected_pixmap = QPixmap(PATH + os.sep + "assets" + os.sep +
                                            "{}_selected.png".format(self.__type[5:]))\
                .scaled(100*variables.SCALE, 91*variables.SCALE, Qt.KeepAspectRatio)
            self.__star_label = QLabel(self)
            self.__star_pixmap = QPixmap(PATH + os.sep + "assets" + os.sep + "tiny_star.png")\
                .scaled(variables.STAR_SIZE*variables.SCALE, variables.STAR_SIZE*variables.SCALE, Qt.KeepAspectRatio)
            self.__star_label.setPixmap(self.__star_pixmap)
            self.__star_label.move((50 - variables.STAR_SIZE*variables.SCALE/2)*variables.SCALE,
                                   (46 - variables.STAR_SIZE*variables.SCALE/2)*variables.SCALE)
            self.__star_label.setMouseTracking(True)
        else:
            self._pixmap = QPixmap(PATH + os.sep + "assets" + os.sep + "{}.png".format(self.__type))\
                .scaled(100*variables.SCALE, 91*variables.SCALE, Qt.KeepAspectRatio)
            self._selected_pixmap = QPixmap(PATH + os.sep + "assets" + os.sep + "{}_selected.png".format(self.__type))\
                .scaled(100*variables.SCALE, 91*variables.SCALE, Qt.KeepAspectRatio)
        self.main_label.setPixmap(self._pixmap)
        self.main_label.setMask(self._pixmap.mask())
        self.setMask(self.main_label.mask())
        self.main_label.setFixedSize(100*variables.SCALE, 91*variables.SCALE)
        self.main_label.show()
        self.main_label.setMouseTracking(True)

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value):
        self.__set_selected(value)

    def __set_selected(self, selected):
        self.__selected = selected
        if selected:
            self.main_label.setPixmap(self._selected_pixmap)
        else:
            self.main_label.setPixmap(self._pixmap)

    def leaveEvent(self, event):
        self.__section = 7

    def mousePressEvent(self, QMouseEvent):
        self.parent().pieceClickedSignal.emit(PieceClickedEvent(self.column, self.row, self.__section, self))
        QMouseEvent.accept()

    def mouseMoveEvent(self, event):
        v1 = event.y() - 45*variables.SCALE
        v2 = event.x() - 46.3*variables.SCALE
        u1 = 45*variables.SCALE
        u2 = 75*variables.SCALE

        numerator = abs(u1*v1 + u2*v2)
        denominator = math.sqrt(u1**2 + u2**2) * math.sqrt(v1**2 + v2**2)
        if denominator != 0:
            angle = math.degrees(math.acos(numerator/denominator))

            if (45/75)*event.x() + 15*variables.SCALE >= event.y():
                if (-75/45)*event.x() + 128.33*variables.SCALE < event.y():
                    angle = 180 - angle
            else:
                if (-75/45)*event.x() + 128.33*variables.SCALE >= event.y():
                    angle = 360 - angle
                else:
                    angle += 180

            if 0 <= angle <= 60:
                self.section_entered(1)
            elif 60 < angle <= 120:
                self.section_entered(2)
            elif 120 < angle <= 180:
                self.section_entered(3)
            elif 180 < angle <= 240:
                self.section_entered(4)
            elif 240 < angle <= 300:
                self.section_entered(5)
            else:
                self.section_entered(6)
        else:
            # Mouse en el centro
            pass

    def section_entered(self, section):
        if self.__section != section:
                self.__section = section
                variables.GAME_INTERFACE.piece_section_entered(section, self)

    def animated_move(self, final_pos, on_move_end=None):
        if variables.ANIMATIONS:
            if self.__timer is None:
                self.__timer = MovePieceTimer(self, final_pos, self.parent(), on_move_end)
                self.__timer.start()
            else:
                if not sip.isdeleted(self.__timer):
                    self.__timer.deleteLater()
                self.__timer = MovePieceTimer(self, final_pos, self.parent(), on_move_end)
                self.__timer.start()
        else:
            self.move(*final_pos)


class Bomb(Piece):

    def __init__(self, piece_type, number=5, parent=None):
        super().__init__(piece_type, parent)
        self._number = number
        self._number_label = QLabel(self)
        self._number_label.setText(str(self._number))
        self._number_label.move(40, 38)
        font = QFont()
        font.setBold(True)
        font.setPixelSize(30)
        self._number_label.setFont(font)
        self._number_label.setStyleSheet("color: white;")
        self._number_label.show()

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
        self._number_label.setText(str(self._number))


class PieceClickedEvent:

    def __init__(self, column, i, section, piece):
        self.column = column
        self.row = i
        self.piece = piece
        self.section = section


class MovePieceTimer(QTimer):

    def __init__(self, hexagon, final_pos, parent=None, on_move_end=None):
        super().__init__(parent)
        self.hexagon = hexagon
        self.delta_x = final_pos[0] - self.hexagon.x()
        self.delta_y = final_pos[1] - self.hexagon.y()
        self.first_x = hexagon.x()
        self.first_y = hexagon.y()
        self.ticks = 0
        self.on_move_end = on_move_end
        self.timeout.connect(self.tick)

    def start(self, p_int=None):
        if p_int is None:
            super().start(variables.TICKS_INTERVAL[variables.QUALITY])
        else:
            super().start(p_int)

    def tick(self):
        if self.ticks <= variables.TOTAL_TICKS[variables.QUALITY] and not sip.isdeleted(self.hexagon):
            new_x = self.first_x + (self.delta_x * (self.ticks/variables.TOTAL_TICKS[variables.QUALITY]))
            new_y = self.first_y + (self.delta_y * (self.ticks/variables.TOTAL_TICKS[variables.QUALITY]))
            self.hexagon.move(new_x, new_y)
            self.ticks += 1
        else:
            self.deleteLater()
            self.hexagon.timer = None
            if self.on_move_end is not None:
                self.on_move_end()
