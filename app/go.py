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
        # self.setWindowTitle('Go')

        self.show()

        self.toolbar = QToolBar()
        self.toolbar.setFixedWidth(200)

        self.addToolBar(Qt.RightToolBarArea,self.toolbar)
        self.PlayerOneLabel = QLabel(" Player 1 : "  + " Player Name here")
        self.PlayerTwoLabel = QLabel(" Player 2 : "  + " Player Name here")
        self.toolbar.addWidget(self.PlayerOneLabel)
        self.toolbar.addWidget(self.PlayerTwoLabel)







    def center(self):
        '''
            Centers the window on the screen
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
