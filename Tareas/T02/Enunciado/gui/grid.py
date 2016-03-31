from PyQt4.QtGui import QApplication, QHBoxLayout, QWidget
from PyQt4.QtCore import pyqtSignal, Qt, QEvent
from .piece import Bomb, Piece, PieceClickedEvent
import math
import random
from .variables import variables


class Grid(QWidget):

    pieceClickedSignal = pyqtSignal(PieceClickedEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hbox = QHBoxLayout()
        self.columns = []
        self.__matrix = []
        self.__pos_matrix = []

        self.__init_matrix()
        self.__init_pos_matrix()

        self.__registerEvents()

        # self.initUI()

    def initUI(self):
        self.setFixedSize(98*variables.SCALE*7.9, 91*variables.SCALE*9)

    def __init_matrix(self):
        self.__matrix = []
        for j in range(0, 10):
            if j % 2 == 0:
                self.__matrix.append([None for i in range(0, 8)])
            else:
                self.__matrix.append([None for i in range(0, 9)])

    def __init_pos_matrix(self):
        self.__pos_matrix = []
        for j in range(0, 10):
            if j % 2 == 0:
                self.__pos_matrix.append([(j*75*variables.SCALE, math.floor(i*91*variables.SCALE) +
                                           (45.5*variables.SCALE))
                                          for i in range(0, 8)])
            else:
                self.__pos_matrix.append([(j*75*variables.SCALE, math.floor(i*91*variables.SCALE)) for i in range(0, 9)])

    def __registerEvents(self):
        self.pieceClickedSignal.connect(self.onPieceClicked)

    def getPiece(self, row, column):
        return self.__matrix[column][row]

    def addPiece(self, row, column, piece_type=None, on_move_ended=None, number=5):
        if piece_type is None:
            piece_type = random.choice(variables.TYPES)
        if self.getPiece(row, column) is None:
            if "bomb" in piece_type:
                piece = Bomb(piece_type, parent=self, number=number)
            else:
                piece = Piece(piece_type, parent=self)
            piece.show()
            piece.row = row
            piece.column = column
            piece.move(self.__pos_matrix[column][0][0], -96*variables.SCALE)
            piece.animated_move(self.__pos_matrix[column][row], on_move_ended)
            self.__matrix[column][row] = piece
        else:
            raise Exception("Espacio ocupado")

    def movePiece(self, row, column, piece, on_move_end=None):
        if self.getPiece(row, column) is None:
            piece.row = row
            piece.column = column
            piece.animated_move(self.__pos_matrix[column][row], on_move_end)
            self.__matrix[column][row] = piece
        else:
            raise Exception("Espacio ocupado")

    def popPiece(self, row, column):
        piece = self.__matrix[column][row]
        self.__matrix[column][row] = None
        return piece

    def onPieceClicked(self, event):
        variables.GAME_INTERFACE.piece_clicked(event.row, event.column, event.section, event.piece)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.columns[0].removeHexagon(4)

if __name__ == "__main__":
    app = QApplication([])
    game = Grid()
    game.show()
    app.exec()
