'''
    App Runner - Executes the QApplication
'''
from PyQt5.QtWidgets import QApplication
from app.go import Go
import sys

app = QApplication([])
myGo = Go()
sys.exit(app.exec_())
