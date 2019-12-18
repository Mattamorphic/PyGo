'''
    Represents the board
'''
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
from .piece import Piece
from .game_logic import (GameLogic, GameOverPassError, KOError, SuicideError,
                         OccupiedError)


class Board(QFrame):  # base the board on a QFrame widget

    # Signal for the player timer being updated by timerEvent
    updatePlayersTimer = pyqtSignal(object)
    # Signal for updating the score
    updateScoreSignal = pyqtSignal(object)
    # Signal for if there is a logic error (KO/Suicide/Occupied)
    updateLogicSignal = pyqtSignal(str)
    # Signal for for the current player
    updateCurrentPlayerSignal = pyqtSignal(object)
    # Signal for game over
    updateGameOverSignal = pyqtSignal()

    boardWidth = 7
    boardHeight = 7
    # Timer speed is denoted in milliseconds
    timerSpeed = 1000

    # Colours to denote checks each representing an RGB tuple
    checkColours = [(255, 235, 205), (205, 133, 63)]

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''
            Initiates the board
        '''
        # Timer for tracking time
        self.timer = QBasicTimer()
        # Denotes if the game is underway
        self.isStarted = False
        # The initial board
        self.boardArray = [[Piece.NoPiece for j in range(self.boardWidth)]
                           for i in range(self.boardHeight)]
        # The gameLogic that controls play
        self.gameLogic = GameLogic(self.boardArray)
        # Start the game
        self.start()

    def getCurrentPlayer(self):
        '''
            Helper method to fetch the current player from the logic instance

            Returns:
                Player
        '''
        return self.gameLogic.getPlayers()[self.gameLogic.player]

    def printBoardArray(self, board):
        '''
            Pretty prints the boardArray to the terminal

            Args:
                board (list): A board
        '''
        print("boardArray:")
        print('\n'.join(
            ['\t'.join([str(cell) for cell in row]) for row in board]))

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
        self.timer.start(self.timerSpeed, self)

    def timerEvent(self, event):
        '''
            This event is automatically called when the timer is updated.
            Based on the timerSpeed variable.

            Args:
                event (Event): Timer event
        '''
        # if the timer that has 'ticked' is the one in this class
        if event.timerId() == self.timer.timerId():
            # Get the current player
            player = self.getCurrentPlayer()
            # If there is no time remaining, then game over
            if player.timeRemaining <= 0:
                self.updateGameOverSignal.emit()
            else:
                player.timeRemaining -= 1
            # Emit the new state of the timer
            self.updatePlayersTimer.emit(self.gameLogic.getPlayers())
        else:
            # if we do not handle an event pass it to the parent class
            super(Board, self).timerEvent(event)

    def paintEvent(self, event=None):
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
        # Get the current row/col where this click occured
        row, col = self.getSquareRowCol(event.x(), event.y())
        # On mouse press try and update the board logic
        try:
            self.gameLogic.updateBoard(row, col)
        # Handle all of the different logical errors that can occur
        except KOError:
            self.updateLogicSignal.emit(f"KO, try again ({row, col})")
        except SuicideError:
            self.updateLogicSignal.emit(f"Suicide, try again ({row, col})")
        except OccupiedError:
            self.updateLogicSignal.emit(f"Occupied, try again ({row, col})")
        # Whatever happens, update the board
        finally:
            self.boardArray = self.gameLogic.board
        # Emit the current player (this switches in the updateBoard logic)
        self.updateCurrentPlayerSignal.emit(self.getCurrentPlayer())
        # Emit the latest player objects
        self.updateScoreSignal.emit(self.gameLogic.getPlayers())
        # Redraw the GUI
        self.update()

    def resetGame(self):
        '''
            Clears pieces from the board'
        '''
        # Reset the logic
        self.gameLogic.reset()
        # Reset the board
        self.boardArray = self.gameLogic.board
        # Emit the player objects with reset scores
        self.updateScoreSignal.emit(self.gameLogic.getPlayers())
        # Emit the current player
        self.updateCurrentPlayerSignal.emit(self.getCurrentPlayer())
        # Redraw the GUI
        self.update()

    def undo(self):
        '''
            Undo last turn
        '''
        print("Not implemented")

    def skip(self):
        '''
            Handle skip / passes
        '''
        # Try and skip a go, unless there are two skips - then emit game over
        try:
            self.gameLogic.skip()
            self.updateCurrentPlayerSignal.emit(self.getCurrentPlayer())
        except GameOverPassError:
            self.updateGameOverSignal.emit()

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

                black and white squares being drawn on board
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
            pen is doing the circle
            brush is filling in the circle

            Args:
                painter (QPainter): The painter
                col     (int):      The column to draw at
                row     (int):      The row to draw at
                color   (Qt.color): The color for the piece
        '''
        painter.save()
        painter.setPen(QPen(QColor(color), 0))
        painter.setBrush(QColor(color))
        painter.translate(*self.getSquareCoords(col, row))
        radius = (self.squareWidth() - 2) / 5
        center = QPoint(self.squareWidth() // 2, self.squareHeight() // 2)
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
