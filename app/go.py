'''
    Core Go Application
'''
from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QDialog, QLCDNumber,
                             QDialogButtonBox, QLabel, QToolBar, QPushButton,
                             QHBoxLayout, QVBoxLayout, QWidget)
from PyQt5.QtCore import Qt, pyqtSlot
from .board import Board
from .score_board import ScoreBoard


class Go(QMainWindow):
    '''
        Go extends from QMainWindow
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        '''
            Getter for board

            Returns:
                Board
        '''
        return self.board

    def getScoreBoard(self):
        '''
            Getter for score board

            Returns:
                ScoreBoard
        '''
        return self.scoreBoard

    def initUI(self):
        '''
            Initiates application UI
        '''
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.makeConnection(self.board)

        self.resize(1000, 800)
        self.center()
        # self.setWindowTitle('Go')
        self.show()

        # Create a toolbar to display player controls
        self.toolbar = QToolBar()
        # This should be at the top
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        # If there are no players, then just await state

        player = QWidget()
        playerLayout = QHBoxLayout()
        playerLayout.addWidget(QLabel("Player:"))
        self.currentPlayerLabel = QLabel("Awaiting game")
        playerLayout.addWidget(self.currentPlayerLabel)
        playerLayout.addWidget(QLabel("with"))
        # Create a timer for the player
        self.playerTimeDisplay = self.makeLCD()
        playerLayout.addWidget(self.playerTimeDisplay)
        playerLayout.addWidget(QLabel("seconds left"))
        player.setLayout(playerLayout)

        # Get the current player from the board
        self.updatePlayer(self.board.getCurrentPlayer())
        # Add these widgets to the toolbar
        self.toolbar.addWidget(player)

        # Create toolbar buttons for the player

        # Restart the game
        reset = QPushButton("Restart")
        reset.clicked.connect(self.board.resetGame)
        self.toolbar.addWidget(reset)

        # Skip a turn
        skip = QPushButton("Skip")
        skip.clicked.connect(self.trySkip)
        self.toolbar.addWidget(skip)

        # Undo a turn
        undo = QPushButton("Undo")
        undo.clicked.connect(self.board.undo)
        self.toolbar.addWidget(undo)


        # Menu

        ## TODO: Add menu with help option, displays rules of GO in dialog
        ## TODO: Add menu options to reset game

        # Connect any signals from the board to helper methods
        self.makeConnection()

    def makeLCD(self):
        '''
            Make a QLCDNumber

            Returns:
                QLCDNumber
        '''
        lcd = QLCDNumber()
        lcd.setSegmentStyle(QLCDNumber.Flat)
        lcd.setStyleSheet("""QLCDNumber {
                                background-color: black;
                                color: white; }""")
        return lcd

    def makeConnection(self):
        '''
            Connect board signals to methods
        '''
        self.board.updatePlayersTimer.connect(self.updatePlayerTimer)
        self.board.updateCurrentPlayerSignal.connect(self.updatePlayer)
        self.board.updateGameOverSignal.connect(self.updateGameOver)

    @pyqtSlot(object)
    def updatePlayer(self, player):
        '''
            Given a player object, update the player

            Args:
                player (Player): The current player
        '''
        self.currentPlayerLabel.setText(f"{player.name}")
        background = "rgb(" + ",".join([str(v)
                                        for v in player.getColor()]) + ")"
        self.currentPlayerLabel.setStyleSheet("""
            QLabel {
                background-color : """ + background + """;
                color :  rgb(127, 127, 127);
                font-weight: bold
            }
        """)

    @pyqtSlot(object)
    def updatePlayerTimer(self, _):
        '''
            Update the player timer from players
        '''
        self.playerTimeDisplay.display(
            self.board.getCurrentPlayer().getTimeRemaining())

    def trySkip(self):
        '''
            Try and skip a go
        '''
        self.board.skip()

    @pyqtSlot()
    def updateGameOver(self):
        '''
            On GameOver, trigger a dialog
        '''
        # Create dialog
        self.gameOverDialog = QDialog(self)

        # Create a layout to add to the dialog
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Game Over"))

        # Display winner
        ## TODO: Add winner info

        # Create a button holder for the dialog
        buttonBox = QDialogButtonBox(Qt.Vertical)


        # Add some options
        buttonBox.addButton("&Restart", QDialogButtonBox.AcceptRole)
        buttonBox.addButton("&Leave", QDialogButtonBox.RejectRole)

        # Connect methods to each of the buttons for different scenarios
        buttonBox.accepted.connect(self.restartGame)
        buttonBox.rejected.connect(self.close)

        # Add the buttons to the layout
        layout.addWidget(buttonBox)

        # Set the layout, and launch the dialog
        self.gameOverDialog.setLayout(layout)
        self.gameOverDialog.exec_()

    def restartGame(self):
        '''
            Close the dialog and restart the game
        '''
        self.board.resetGame()
        self.gameOverDialog.close()

    def center(self):
        '''
            Centers the window on the screen
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
