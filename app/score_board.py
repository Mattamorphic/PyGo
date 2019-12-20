'''
    Represents the Score Board
'''
from PyQt5.QtWidgets import (QDockWidget, QVBoxLayout, QWidget, QLabel,
                             QSizePolicy)
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
        self.mainWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # create two labels which will be updated by signals
        self.players = {
            Piece.White: {
                "scoreLabel":
                self.makeScoreLabel("White: 0", (0, 0, 0), (255, 255, 255)),
                "score":
                0
            },
            Piece.Black: {
                "scoreLabel":
                self.makeScoreLabel("White: 0", (255, 255, 255), (0, 0, 0)),
                "score":
                0
            }
        }
        self.logicMessage = QLabel()
        self.updateLogicMessage()
        self.mainWidget.setLayout(self.mainLayout)
        for id, player in self.players.items():
            self.mainLayout.addWidget(player["scoreLabel"])
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
        board.updateScoreSignal.connect(self.updateScore)
        board.updateLogicSignal.connect(self.updateLogicMessage)

    def makeScoreLabel(self, message, background, foreground):
        label = QLabel(message)
        label.setStyleSheet("""
            QLabel {
                background-color: rgb(""" +
                            ",".join([str(v) for v in background]) + """);
                color: rgb(""" + ",".join([str(v) for v in foreground]) + """);
                font-size: 20px;
                padding-top: 10px;
                padding-bottom: 10px;
                text-align: center;
            }
        """)
        return label

    @pyqtSlot(object)
    def updateScore(self, players):
        for id, player in players.items():
            score = player.getScore()
            self.players[id]["scoreLabel"].setText(
                f"{player.getName()}: {score}")
            self.players[id]["score"] = score

    @pyqtSlot(str)
    def updateLogicMessage(self, message=None):
        background = "red"
        if not message:
            background = "green"
            message = "Valid"
        self.logicMessage.setStyleSheet("""
            QLabel {
                background-color: """ + background + """;
                color: white;
                font-size: 20px;
                margin-top:20px;
                padding-top: 10px;
                padding-bottom: 10px;
                text-align: center;
            }
        """)
        self.logicMessage.setText(message)
