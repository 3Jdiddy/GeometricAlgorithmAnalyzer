from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Algortihm Visualizer")
    
        label = QtWidgets.QLabel(self)
        label.setText("This is a label")
        label.move(100, 100)

def event():
    print("event happened")

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    button1 = QtWidgets.QPushButton(win)
    button1.setText("Run Event")
    button1.clicked.connect(event)

    win.show()
    sys.exit(app.exec_())


window()
