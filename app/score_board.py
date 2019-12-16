'''
    Represents the Score Board
'''
# TODO import additional Widget classes as desired
from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import pyqtSlot
from .piece import Piece


class ScoreBoard(QDockWidget):
    '''
        Base the score_board on a QDockWidget
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
            Initiates ScoreBoard UI
        '''
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # create two labels which will be updated by signals
        self.playerA = QLabel("Player White: 0")
        self.playerB = QLabel("Player Black: 0")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.logicMessage = QLabel("Take your turn")
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.playerA)
        self.mainLayout.addWidget(self.playerB)
        self.mainLayout.addWidget(self.logicMessage)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.setWidget(self.mainWidget)
        self.show()

    def center(self):
        '''
            Centers the window on the screen,
                you do not need to implement this method
        '''
        pass

    def makeConnection(self, board):
        '''
            This handles a signal sent from the board class

            Args:
                board (Board): The board
        '''
        # when the updateTimerSignal is emitted in the board
        # the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        board.updateScoreSignal.connect(self.updateScore)
        board.updateLogicSignal.connect(self.updateLogicMessage)

    # Ensure the slot is receiving an argument of the type 'int'
    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''
            Updates the time remaining label to show the time remaining

            Args:
                timeRemainng (Int): Time remaining
        '''
        update = "Time Remaining:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        # print('slot ' + update)
        # self.redraw()

    @pyqtSlot(object)
    def updateScore(self, players):
        self.playerA.setText(f"Player A: {players[Piece.White].score}")
        self.playerB.setText(f"Player B: {players[Piece.Black].score}")

    @pyqtSlot(str)
    def updateLogicMessage(self, message):
        self.logicMessage.setText(message)
