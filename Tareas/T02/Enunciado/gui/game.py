import os


from .grid import Grid
from .piece import Piece
from PyQt4.QtGui import QHBoxLayout, QLabel, QPixmap, QVBoxLayout, QWidget, QFont, QPushButton
from PyQt4.QtCore import Qt
from .variables import variables

PATH = os.path.dirname(os.path.abspath(__file__))


class Game(QWidget):

    def __init__(self):
        super().__init__()
        self.hbox = QHBoxLayout()
        self.grid = Grid(self)
        self.vbox = QVBoxLayout()
        self.label_puntaje = QLabel("0")
        self.button = QPushButton("Invertir")
        self.orientation = QLabel()
        self.__clockwise_pm = QPixmap(PATH + os.sep + "assets" + os.sep + "clockwise.png").scaled(128*variables.SCALE,
                                                                                                  128*variables.SCALE)
        self.__anticlockwise_pm = QPixmap(PATH + os.sep + "assets" + os.sep + "anticlockwise.png")\
            .scaled(128*variables.SCALE, 128*variables.SCALE)
        self.clockwise = True
        # self.initUi()

    def initUi(self):
        self.setWindowTitle('BLABLABLA')
        self.setMouseTracking(True)
        # self.setGeometry(50, 50, 1024, 768)
        # self.setMaximumSize(1024, 768)
        # self.setMinimumSize(800, 600)
        self.setLayout(self.hbox)
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.grid)
        self.grid.show()
        self.vbox.addStretch(1)
        font = QFont()
        font.setBold(True)
        font.setPixelSize(30*variables.SCALE)
        label = QLabel("PUNTAJE")
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(label)
        font2 = QFont()
        font2.setPixelSize(30*variables.SCALE)
        self.label_puntaje.setFont(font2)
        self.label_puntaje.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.label_puntaje)
        self.vbox.addWidget(self.button)
        self.vbox.addWidget(self.orientation)
        self.orientation.setAlignment(Qt.AlignCenter)
        self.orientation.setPixmap(self.__clockwise_pm)
        self.vbox.addStretch(1)
        self.button.clicked.connect(self.invertirPressed)

        self.grid.initUI()

    def invertirPressed(self):
        self.clockwise = not self.clockwise
        if self.clockwise:
            self.orientation.setPixmap(self.__clockwise_pm)
        else:
            self.orientation.setPixmap(self.__anticlockwise_pm)
        variables.GAME_INTERFACE.reverse_clicked(self.clockwise)

    def addPiece(self, i, j, hexagon_type, on_move_ended=None, number=5):
        self.grid.addPiece(i, j, hexagon_type, on_move_ended, number)

    def getPiece(self, i, j):
        return self.grid.getPiece(i, j)

    def popPiece(self, i, j):
        return self.grid.popPiece(i, j)

    def movePiece(self, i, j, piece, on_move_end=None):
        self.grid.movePiece(i, j, piece, on_move_end)

    def setPoints(self, points):
        self.label_puntaje.setText(str(points))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            variables.GAME_INTERFACE.save_game()
        elif event.key() == Qt.Key_H:
            variables.GAME_INTERFACE.hint_asked()
        elif event.key() == Qt.Key_Space:
            self.invertirPressed()
