'''
    Core Go Application
'''
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget,QToolBar,QLabel
from PyQt5.QtCore import Qt
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
        # self.scoreBoard = ScoreBoard()
        # self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        # self.scoreBoard.makeConnection(self.board)

        self.resize(1000, 800)
        self.center()
        self.setWindowTitle('Go')
        self.setWindowIcon(QIcon("./icon/go.png"))
        self.show()
        buttonPlay = QMessageBox.question(self, 'Welcome TO Play Go Game', "Rules OF the Game ",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        ''' #board=setBoard(start)
        self.browser=QWebView()
        self.browser.setUrl(QUrl("https://www.britgo.org/intro/intro2.html"))'''
        if buttonPlay == QMessageBox.Yes:
            buttonReply = QMessageBox.question(self, 'Play Go Game', "Would you like to play Go Game ",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReplay == QMessageBox.Yes:
            self.resetGame()
        else:
            self.ignore()
        self.show()

    def resetGame(self):
        self.toolbar = QToolBar()
        self.toolbar.setFixedWidth(200)

        self.addToolBar(Qt.RightToolBarArea, self.toolbar)
        self.PlayerOneLabel = QLabel(" Player 1 : " + " Player Name here")
        self.PlayerTwoLabel = QLabel(" Player 2 : " + " Player Name here")
        self.whoseTurnLabel = QLabel(" whose Turn")
        self.player1ScoreLabel = QLabel(" player 1 Score")
        self.player2ScoreLabel = QLabel(" player 2 Score")
        self.player1TerritoryLabel = QLabel("Controlled teritory by  player 1 ")
        self.player2TerritoryLabel = QLabel(" Controlled teritory by player 2 ")
        self.player1PrisonerLabel = QLabel(" Prisoner by player 1 ")
        self.player2PrisonerLabel = QLabel(" Prisoner by player 2 ")
        self.Player1PassLabel = QLabel(" player 1 pass")
        self.Player2PassLabel = QLabel(" player 2 pass")
        self.redoLabel = QLabel(" redo")
        self.undoLabel = QLabel(" undo")
        self.resetLabel = QLabel(" reset/new Game")
        self.winnerLabel = QLabel("winer is balck/white")

        self.toolbar.addWidget(self.PlayerOneLabel)
        self.toolbar.addWidget(self.PlayerTwoLabel)
        self.toolbar.addWidget(self.whoseTurnLabel)
        self.toolbar.addWidget(self.player1ScoreLabel)
        self.toolbar.addWidget(self.player2Scoreabel)
        self.toolbar.addWidget(self.player1TerritoryLabel)
        self.toolbar.addWidget(self.player2TerritoryLabel)
        self.toolbar.addWidget(self.player1PrisonerLabel)
        self.toolbar.addWidget(self.player2PrisonerLabel)
        self.toolbar.addWidget(self.Player1PassLabel)
        self.toolbar.addWidget(self.Player2PassLabel)
        self.toolbar.addWidget(self.redoLabel)
        self.toolbar.addWidget(self.undoLabel)
        self.toolbar.addWidget(self.resetLabel)
        self.toolbar.addWidget(self.winnerLabel)

    def redo(self):
        '''we need to place redo a logic under here'''
    def undo(self):
          '''we need to place a logic under here'''


    def center(self):
        '''
            Centers the window on the screen
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
