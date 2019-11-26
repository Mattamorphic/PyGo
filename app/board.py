'''
    Represents the board
'''
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
# from .piece import Piece # TODO Uncomment when we start using this


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(
        str)  # signal sent when there is a new click location

    boardWidth = 7
    boardHeight = 7
    timerSpeed = 1  # the timer updates ever 1 second
    counter = 10  # the number the counter will count down from

    checkColours = [(255, 235, 205), (205, 133, 63)]

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''
            Initiates the board
        '''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer
        self.boardArray = [[0 for j in range(self.boardWidth)]
                           for i in range(self.boardHeight)]
        self.printBoardArray()

    def printBoardArray(self):
        '''
            Pretty prints the boardArray to the terminal
        '''
        print("boardArray:")
        print('\n'.join([
            '\t'.join([str(cell) for cell in row]) for row in self.boardArray
        ]))

    def squareWidth(self):
        '''
            Returns the width of one square in the board

            Returns:
                float
        '''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''
            Returns the height of one square of the board

            Returns:
                float
        '''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''
            Start the game
        '''
        self.isStarted = True  # determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed,
                         self)  # start the timer with the correct speed
        # print("start () - timer is started")

    def timerEvent(self, event):
        '''
            This event is automatically called when the timer is updated.
            Based on the timerSpeed variable.

            Args:
                event (Event): Timer event
        '''
        # TODO adapter this code to handle your timers
        # if the timer that has 'ticked' is the one in this class
        if event.timerId() == self.timer.timerId():
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            # print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            # if we do not handle an event pass it to the parent class
            super(Board, self).timerEvent(event)

    def paintEvent(self, event):
        '''
            Paints the board and the pieces of the game

            Args:
                event (Event): The paint event
        '''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''
            Mouse press event handler

            Args:
                event (Event): The mouse press event
        '''
        clickLoc = "click location [" + str(event.x()) + "," + str(
            event.y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        row, col = self.getSquareRowCol(event.x(), event.y())
        print(f"Click in {col, row}")
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''
            Clears pieces from the board'
        '''
        # TODO write code to reset game
        pass

    def tryMove(self, newX, newY):
        '''
            Tries to move a piece

            Args:
                newX (Int): X axis position
                newY (Int): Y axis position
        '''
        pass

    def drawBoardSquares(self, painter):
        '''
            Draw all the square on the board

            Args:
                painter (QPainter): The painter to paint on the widget with
        '''
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                self.drawSquare(
                    painter, col, row, self.checkColours[0] if
                    (col + row) % 2 == 1 else self.checkColours[1])

    def drawPieces(self, painter):
        '''
            Draw the prices on the board

            Args:
                painter (QPainter): The painter to paint with
        '''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                square = self.boardArray[row][col]
                if square == 0:
                    self.drawEmptySpace(painter, col, row)
                elif square == 1:
                    self.drawWhitePiece(painter, col, row)
                else:
                    self.drawBlackPiece(painter, col, row)

    def drawEmptySpace(self, painter, col, row):
        '''
            Helper method to draw an empty space at the given col, row

            Args:
                painter (QPainter): The painter
                col     (int):      The column to draw at
                row     (int):      The row to draw at
        '''
        self.drawPiece(painter, col, row, Qt.transparent)

    def drawBlackPiece(self, painter, col, row):
        '''
            Helper method to draw a black piece at the given col, row

            Args:
                painter (QPainter): The painter
                col     (int):      The column to draw at
                row     (int):      The row to draw at
        '''
        self.drawPiece(painter, col, row, Qt.black)

    def drawWhitePiece(self, painter, col, row):
        '''
            Helper method to draw a white piece at the given col, row

            Args:
                painter (QPainter): The painter
                col     (int):      The column to draw at
                row     (int):      The row to draw at
        '''
        self.drawPiece(painter, col, row, Qt.white)

    def drawPiece(self, painter, col, row, color):
        '''
            Draw a piece at the given col, row

            Args:
                painter (QPainter): The painter
                col     (int):      The column to draw at
                row     (int):      The row to draw at
                color   (Qt.color): The color for the piece
        '''
        painter.save()
        painter.setPen(QPen(QColor(color), 2))
        painter.translate(*self.getSquareCoords(col, row))
        radius = (self.squareWidth() - 2) / 2
        center = QPoint(radius, radius)
        painter.drawEllipse(center, radius, radius)
        painter.restore()

    def drawSquare(self, painter, col, row, color):
        '''
            Draw a board square on the board

            Args:
                painter (QPainter): The QPainter instance we are using
                col     (int)     : The current column we are rendering in
                row     (row)     : The current row we are rendering in
                rgb     (iter)    : The rgba int values
        '''
        width = int(self.squareWidth())
        height = int(self.squareHeight())
        midWidth = width // 2
        midHeight = height // 2
        painter.save()
        painter.translate(*self.getSquareCoords(col, row))
        painter.fillRect(0, 0, width, height, QColor(*color))
        painter.setPen(QPen(QColor(139, 69, 19), 2))
        painter.drawRect(0, 0, width, height)
        painter.drawLine(0, midHeight, width, midHeight)
        painter.drawLine(midWidth, 0, midWidth, height)
        painter.restore()

    def getSquareCoords(self, col, row):
        '''
            Calculate the square coords

            Args:
                col (int): The currrent col
                row (int): The current row

            Returns:
                Tuple
        '''
        return (self.squareWidth() * col, self.squareHeight() * row)

    def getSquareRowCol(self, x, y):
        '''
            Given X and Y find the column and the row

            Args:
                x (int):    The X POS
                y (int):    The Y POS

            Returns:
                Tuple
        '''
        return (int(y // self.squareHeight()), int(x // self.squareWidth()))
