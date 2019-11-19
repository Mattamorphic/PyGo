'''
    Represents the board
'''
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QBasicTimer, pyqtSignal, QPoint
# from PyQt5.QtGui import QPainter # TODO Uncomment when we instantiate
# from .piece import Piece # TODO Uncomment when we start using this


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(
        str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 0  # TODO this needs updating - board is 0 squares wide
    boardHeight = 0  #
    timerSpeed = 1  # the timer updates ever 1 second
    counter = 10  # the number the counter will count down from

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

        # TODO - create a 2d int/Piece array to store the state of the game
        self.boardArray = []

        # TODO - uncomment this method after create the array above
        # self.printBoardArray()

    def printBoardArray(self):
        '''
            Pretty prints the boardArray to the terminal
        '''
        print("boardArray:")
        print('\n'.join([
            '\t'.join([str(cell) for cell in row]) for row in self.boardArray
        ]))

    def mousePosToColRow(self, event):
        '''
            Convert the mouse click event to a row and column

            Args:
                event (Event): The mouse click event
        '''
        pass  # pass means ignore the code block - supresses errors

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
        print("start () - timer is started")

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
            print('timerEvent()', self.counter)
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
        # painter = QPainter(self)
        # self.drawBoardSquares(painter)
        # self.drawPieces(painter)
        pass

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
        # TODO set the default colour of the brush
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                # TODO set value equal the transformation
                #   in the column direction
                colTransformation = self.squareWidth() * col
                # TODO set this value equal the transformation
                #   in the row direction
                rowTransformation = 0
                painter.translate(colTransformation, rowTransformation)
                painter.fillRect()  # TODO provide the required arguments
                painter.restore()
                # TODO change the colour of the brush so a checkered board is
                # drawn - alternating on each iteration

    def drawPieces(self, painter):
        '''
            Draw the prices on the board

            Args:
                painter (QPainter): The painter to paint with
        '''
        # empty square could be modeled with transparent pieces
        # colour = Qt.transparent
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate()

                # TODO draw some the pieces as ellipses
                # TODO choose colour & set the painter brush to correct colour
                radius = (self.squareWidth() - 2) / 2
                center = QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
