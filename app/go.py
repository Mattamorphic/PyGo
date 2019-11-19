'''
    Core Go Application
'''
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
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
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.makeConnection(self.board)

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        '''
            Centers the window on the screen
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
