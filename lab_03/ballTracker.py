# Name: Adib Yahaya
# Date: 3/3/2019
# CPET563 Lab 3: Embedded Tennis Ball Tracker
# Description: Ball Tracker widget

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2

class BallTracker(QWidget):
  def __init__(self, parent=None):
    super(BallTracker, self).__init__(parent)
    self.initUI()
    self.initParam()

  def initUI(self):
    layout = QVBoxLayout()
    layout2 = QHBoxLayout()
    layout3 = QHBoxLayout()

    self.ballSelectLabel = QLabel(self)
    self.ballSelectLabel.setText("Select which ball to track:")

    self.blueBallBtn = QRadioButton("Blue ball")
    self.blueBallBtn.setChecked(True)

    self.greenBallBtn = QRadioButton("Green ball")
    self.greenBallBtn.setChecked(False)

    self.loadImageBtn = QPushButton("Load Image File")
    self.loadImageBtn.clicked[bool].connect(self.loadImageButtonClicked)

    self.loadParamFileBtn = QPushButton("Load Parameters File")
    self.loadParamFileBtn.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    self.loadParamFileBtn.clicked[bool].connect(self.loadParamFileButtonClicked)

    self.saveParamFileBtn = QPushButton("Save Parameters File")
    self.saveParamFileBtn.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    self.saveParamFileBtn.clicked[bool].connect(self.saveParamFileButtonClicked)

    layout.addWidget(self.loadImageBtn)
    layout2.addWidget(self.ballSelectLabel)
    layout2.addWidget(self.blueBallBtn)
    layout2.addWidget(self.greenBallBtn)
    layout3.addWidget(self.loadParamFileBtn)
    layout3.addWidget(self.saveParamFileBtn)

    layout.addLayout(layout2)
    layout.addLayout(layout3)
    self.setLayout(layout)

  def initParam(self):
    self.rMin = 0
    self.rMax = 0
    self.gMin = 0
    self.gMax = 0
    self.bMin = 0
    self.bMax = 0

###############################################################################
# Load an image file
###############################################################################
  def loadImageButtonClicked(self):
    fileName = QFileDialog.getOpenFileName(None, "Select an image",".","Images (*.jpg *.png)")
    if not fileName:
      pass
    else:
      img = cv2.imread(str(fileName))
      cv2.imshow(str(fileName),img)

###############################################################################
# save and load ball detection parameters files
###############################################################################
  def loadParamFileButtonClicked(self):
    fileName = QFileDialog.getOpenFileName(None, "Load parameter file",".txt","(*.txt)")
    if not fileName:
      pass
    else:
      with open(fileName) as f:
        self.rMin = int(f.readline().split("= ")[1])
        self.rMax = int(f.readline().split("= ")[1])
        self.gMin = int(f.readline().split("= ")[1])
        self.gMax = int(f.readline().split("= ")[1])
        self.bMin = int(f.readline().split("= ")[1])
        self.bMax = int(f.readline().split("= ")[1])


  def saveParamFileButtonClicked(self):
    fileName = QFileDialog.getSaveFileName(None, "Save parameter file",".txt","(*.txt)")
    if fileName == "":
      return
    with open(fileName,"w") as f:
      f.write("rMin = " + str(self.rMin)                + "\n")
      f.write("rMax = " + str(self.rMax)                + "\n")
      f.write("gMin = " + str(self.gMin)                + "\n")
      f.write("gMax = " + str(self.gMax)                + "\n")
      f.write("bMin = " + str(self.bMin)                + "\n")
      f.write("bMax = " + str(self.bMax))
