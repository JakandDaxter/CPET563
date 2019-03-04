# Name: Adib Yahaya
# Date: 3/3/2019
# CPET563 Lab 3: Embedded Tennis Ball Tracker
# Description: Main window

import sys
from PyQt4 import QtGui, QtCore
import cv2

# main window class that holds everything
class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()

    self.setWindowTitle("Ball Tracker")

    self.statusBar()
    self.InitMenuBar()

    self.show()

  def InitMenuBar(self):
    mainMenu = self.menuBar()
    fileMenu = mainMenu.addMenu('&Menu')

    loadImageAction = QtGui.QAction("&Open", self)
    loadImageAction.setShortcut("Ctrl+O")
    loadImageAction.setStatusTip('Opens an image file')
    loadImageAction.triggered.connect(self.loadFileMenuClicked)

    fileMenu.addAction(loadImageAction)

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


# start of the program that instantiates a MainWindow class
def main():
  app = QtGui.QApplication(sys.argv)
  mainWindow = MainWindow()

  sys.exit(app.exec_())

if __name__ == '__main__':
    main()