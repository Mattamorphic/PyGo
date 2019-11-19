'''
    Represents the Score Board
'''
# TODO import additional Widget classes as desired
from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import pyqtSlot


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
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
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
        # when the clickLocationSignal is emitted in board
        # the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board
        # the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

    # Ensure the slot is receiving an argument of the type 'str'
    @pyqtSlot(str)
    def setClickLocation(self, clickLoc):
        '''
            Updates the label to show the click location

            Args:
                clickLoc (str): The location of the click
        '''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

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
        print('slot ' + update)
        # self.redraw()
