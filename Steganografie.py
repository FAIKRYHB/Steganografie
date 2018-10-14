import sys
import math

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFileDialog
from PyQt5 import QtGui, uic
from PIL import Image

qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Steganografie(QMainWindow, Ui_MainWindow):
    image = ""
    zprava = ""
    dest = "tmp.png"

    def error(self,msg):
        print(msg)
    def fileChooser(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "PNG files (*.png);;BMP Files (*.bmp)", options=options)
        if fileName:
            self.image = fileName
            obrazek = Image.open(self.image)
            total = math.floor((obrazek.width * obrazek.height - 1) / 8)

            self.info.setText("max: " + str(total) + " znaků")

            self.beforePicture.setPixmap(QtGui.QPixmap(self.image).scaled(171, 140))
    def loadMessage(self):
        self.zprava = self.messageEdit.toPlainText()

    def codeMessage(self, target='tmp.png'):
       if not self.image:
           self.error("Není definovaný obrázek")
           return 0

       if not self.zprava:
            self.error("Není text")
            return 0

       obrazek = Image.open(self.image)
       mapa = obrazek.load()
       if not target:
           target = self.dest

       for i in range(0, obrazek.width):
           for j in range(0, obrazek.height):
               rgb = mapa[i, j]
               nrgb = (rgb[0] & 254, rgb[1] & 254, rgb[2] & 254)
               mapa[i, j] = nrgb

       zprava = self.zprava
       binar = ""

       for i in range(0, len(zprava)):
            temp = str(bin(ord(zprava[i])))
            temp = temp[2:]
            for j in range(len(temp), 8):
                temp = "0" + temp
            binar += temp

       pocitadlo = 0
       x = 0

       for i in range(0, obrazek.width):
            if pocitadlo == (len(binar)):
                if x > 0:
                    i -= 1
                rgb = mapa[i, x]
                nrgb = (rgb[0] + 1, rgb[1] + 1, rgb[2] + 1)  # liché číslo u všech barev = konec zprávy
                mapa[i, x] = nrgb
                break
            for j in range(0, obrazek.height):
                if binar[pocitadlo] == "1":
                    rgb = mapa[i, j]
                    nrgb = (rgb[0] + 1, rgb[1], rgb[2])
                    mapa[i, j] = nrgb
                pocitadlo += 1
                if pocitadlo == (len(binar)):
                    if j + 1 < obrazek.height:
                        x = j + 1
                    break
       obrazek.save(target)
       obrazek.close()

       self.dest = target


       self.afterPicture.setPixmap(QtGui.QPixmap(self.dest).scaled(171, 151))

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                               "PNG files (*.png);;BMP Files (*.bmp)", options=options)
        ext = _.split(".")[1].replace(")","")

        if(fileName.find(ext) < 0):
            fileName = fileName + "." + ext

        self.codeMessage(fileName)

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.setupUi(self)
        self.fileButton.clicked.connect(self.fileChooser)
        self.applyButton.clicked.connect(self.codeMessage)
        self.saveButton.clicked.connect(self.saveFile)
        self.messageEdit.textChanged.connect(self.loadMessage)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Steganografie()
    window.show()
    sys.exit(app.exec_())
