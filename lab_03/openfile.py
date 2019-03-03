# Name: Adib Yahaya
# Date: 3/3/2019
# CPET563 Lab 3: Embedded Tennis Ball Tracker
# Description: Load images via a file menu

import sys
from PyQt4 import QtGui, QtCore
import cv2

# main window class that holds everything
class OpenFile(QtGui.QMainWindow):
  def __init__(self):
    super(OpenFile, self).__init__()

    self.setWindowTitle("Load Image")

    loadImageAction = QtGui.QAction("&Open", self)
    loadImageAction.setShortcut("Ctrl+O")
    loadImageAction.setStatusTip('Opens an image file')
    loadImageAction.triggered.connect(self.loadFileMenuClicked)

    self.statusBar()

    mainMenu = self.menuBar()
    fileMenu = mainMenu.addMenu('&Menu')
    fileMenu.addAction(loadImageAction)

    self.show()

###############################################################################
# Load an image file
###############################################################################
  def loadFileMenuClicked(self):
    fileName = QtGui.QFileDialog.getOpenFileName(None, "Select an image",".","Images (*.jpg *.png)")
    if not fileName:
      pass
    else:
      img = cv2.imread(str(fileName))
      cv2.imshow(str(fileName),img)


# start of the program that instantiates a OpenFile class
def main():
  app = QtGui.QApplication(sys.argv)
  openFile = OpenFile()

  sys.exit(app.exec_())

if __name__ == '__main__':
    main()