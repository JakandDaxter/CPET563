# Name: Adib Yahaya
# Date: 3/3/2019
# CPET563 Lab 3: Embedded Tennis Ball Tracker
# Description: Main window

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
from ballTracker import *

# main window class that holds everything
class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()

    self.setWindowTitle("Ball Tracker")

    self.statusBar()
    self.initMenuBar()
    self.instantiateWidgets()
    self.initDocks()

    self.show()

  def initMenuBar(self):
    mainMenu = self.menuBar()
    fileMenu = mainMenu.addMenu('&Menu')

    loadImageAction = QAction("&Open", self)
    loadImageAction.setShortcut("Ctrl+O")
    loadImageAction.setStatusTip('Opens an image file')
    loadImageAction.triggered.connect(self.loadFileMenuClicked)

    fileMenu.addAction(loadImageAction)

  def instantiateWidgets(self):
    self.ballTracker = BallTracker(self)

  def initDocks(self):
    self.initBallTrackerDock()

    DOCKOPTIONS = QMainWindow.AllowTabbedDocks
    DOCKOPTIONS = DOCKOPTIONS|QMainWindow.AllowNestedDocks
    DOCKOPTIONS = DOCKOPTIONS|QMainWindow.AnimatedDocks
    self.setDockOptions(DOCKOPTIONS)
    self.setTabPosition(Qt.AllDockWidgetAreas,QTabWidget.North)

  def initBallTrackerDock(self):
    self.ballTrackerDock = QDockWidget(self)
    self.ballTrackerDock.setWidget(self.ballTracker)
    self.ballTrackerDock.setWindowTitle("Ball Tracker")
    self.ballTrackerDock.setObjectName("Ball Tracker")
    self.ballTrackerDock.setContentsMargins(0, 0, 0, 0)
    self.ballTrackerDock.setFeatures(QDockWidget.AllDockWidgetFeatures)
    self.ballTrackerDock.setAllowedAreas(Qt.AllDockWidgetAreas)
    self.addDockWidget(Qt.LeftDockWidgetArea, self.ballTrackerDock)

###############################################################################
# Load an image file
###############################################################################
  def loadFileMenuClicked(self):
    fileName = QFileDialog.getOpenFileName(None, "Select an image",".","Images (*.jpg *.png)")
    if not fileName:
      pass
    else:
      img = cv2.imread(str(fileName))
      cv2.imshow(str(fileName),img)

# start of the program that instantiates a MainWindow class
def main():
  app = QApplication(sys.argv)
  mainWindow = MainWindow()

  sys.exit(app.exec_())

if __name__ == '__main__':
    main()