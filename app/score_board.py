'''
    Represents the Score Board
'''
# TODO import additional Widget classes as desired
from PyQt5.QtWidgets import (QDockWidget, QVBoxLayout, QWidget, QLabel)
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
        self.players = {
            Piece.White: {
                "scoreLabel": QLabel("White: 0"),
                "timeLabel": QLabel("White Time Remaining: 120"),
                "score": 0
            },
            Piece.Black: {
                "scoreLabel": QLabel("Black: 0"),
                "timeLabel": QLabel("Black Time Remaining: 120"),
                "score": 0
            }
        }
        self.logicMessage = QLabel("Take your turn")
        self.mainWidget.setLayout(self.mainLayout)
        for id, player in self.players.items():
            self.mainLayout.addWidget(player["scoreLabel"])
            self.mainLayout.addWidget(player["timeLabel"])
        self.mainLayout.addWidget(self.logicMessage)

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
        board.updatePlayersTimer.connect(self.updatePlayersTimer)
        board.updateScoreSignal.connect(self.updateScore)
        board.updateLogicSignal.connect(self.updateLogicMessage)

    # Ensure the slot is receiving an argument of the type 'int'
    @pyqtSlot(object)
    def updatePlayersTimer(self, players):
        '''
            Updates the time remaining label to show the time remaining

            Args:
                players (Dict): Players
        '''
        for id, player in players.items():
            self.players[id]["timeLabel"].setText(
                f"{player.getName()}: {player.getTimeRemaining()}")

    @pyqtSlot(object)
    def updateScore(self, players):
        for id, player in players.items():
            score = player.getScore()
            self.players[id]["scoreLabel"].setText(
                f"{player.getName()}: {score}")
            self.players[id]["score"] = score

    @pyqtSlot(str)
    def updateLogicMessage(self, message):
        self.logicMessage.setText(message)
