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

    self.loadFileBtn = QPushButton("Load File")
    self.loadFileBtn.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    self.loadFileBtn.clicked[bool].connect(self.loadFileButtonClicked)

    self.saveFileBtn = QPushButton("Save File")
    self.saveFileBtn.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    self.saveFileBtn.clicked[bool].connect(self.loadFileButtonClicked)

    layout2.addWidget(self.ballSelectLabel)
    layout2.addWidget(self.blueBallBtn)
    layout2.addWidget(self.greenBallBtn)
    layout3.addWidget(self.loadFileBtn)
    layout3.addWidget(self.saveFileBtn)

    layout.addLayout(layout2)
    layout.addLayout(layout3)
    self.setLayout(layout)

###############################################################################
# save and load ball detection parameters files
###############################################################################
  def loadFileButtonClicked(self):
    fileName = QFileDialog.getOpenFileName(None, "Enter Filename.",".txt","(*.txt)")
    if not fileName:
      pass
    else:
      with open(fileName) as f:
        # Todo: read file
        pass

  def saveFileButtonClicked(self):
    fileName = QFileDialog.getSaveFileName(None, "Enter Filename",".txt","(*.txt)")
    if fileName == "":
      return
    with open(fileName,"w") as f:
      # Todo: write parameters to file
      pass