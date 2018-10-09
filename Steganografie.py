import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar
from PyQt5 import QtGui, uic

qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Steganografie(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)


if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = Steganografie()
   window.show()
   sys.exit(app.exec_())

