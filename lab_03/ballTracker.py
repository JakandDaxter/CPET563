# Name: Adib Yahaya
# Date: 3/3/2019
# CPET563 Lab 3: Embedded Tennis Ball Tracker
# Description: Ball Tracker widget

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
import numpy as np
import copy

class BallTracker(QWidget):
  def __init__(self, parent=None):
    super(BallTracker, self).__init__(parent)
    self.initUI()
    self.initParam()

  def initUI(self):
    layout = QVBoxLayout()
    layout2 = QHBoxLayout()
    layout3 = QHBoxLayout()
    layout4 = QHBoxLayout()

    self.ballSelectLabel = QLabel(self)
    self.ballSelectLabel.setText("Select which ball to track:")

    self.blueBallBtn = QRadioButton("Blue ball")
    self.blueBallBtn.setChecked(False)
    self.blueBallBtn.toggled.connect(lambda:self.setParamViaBtn(self.blueBallBtn))

    self.greenBallBtn = QRadioButton("Green ball")
    self.greenBallBtn.setChecked(False)
    self.greenBallBtn.toggled.connect(lambda:self.setParamViaBtn(self.greenBallBtn))

    self.loadImageBtn = QPushButton("Load Image File")
    self.loadImageBtn.clicked[bool].connect(self.loadImageButtonClicked)

    self.loadParamFileBtn = QPushButton("Load Parameters File")
    self.loadParamFileBtn.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    self.loadParamFileBtn.clicked[bool].connect(self.loadParamFileButtonClicked)

    self.saveParamFileBtn = QPushButton("Save Parameters File")
    self.saveParamFileBtn.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
    self.saveParamFileBtn.clicked[bool].connect(self.saveParamFileButtonClicked)

    layout2.addWidget(self.ballSelectLabel)
    layout2.addWidget(self.blueBallBtn)
    layout2.addWidget(self.greenBallBtn)
    layout3.addWidget(self.loadImageBtn)
    layout4.addWidget(self.loadParamFileBtn)
    layout4.addWidget(self.saveParamFileBtn)

    layout.addLayout(layout2)
    layout.addLayout(layout3)
    layout.addLayout(layout4)
    self.setLayout(layout)

  def initParam(self):
    self.rMin = 0
    self.rMax = 0
    self.gMin = 0
    self.gMax = 0
    self.bMin = 0
    self.bMax = 0

  def setParamViaBtn(self, btn):
    if btn.text() == "Blue ball":
      if btn.isChecked() == True:
        self.rMin = 0
        self.rMax = 60
        self.gMin = 0
        self.gMax = 70
        self.bMin = 46
        self.bMax = 101
    # Green ball
    else:
      if btn.isChecked() == True:
        self.rMin = 0
        self.rMax = 134
        self.gMin = 65
        self.gMax = 255
        self.bMin = 15
        self.bMax = 67

  def doTracker(self, small_img):
    # generate threshold array
    lower = np.array([self.bMin,self.gMin,self.rMin])
    upper = np.array([self.bMax,self.gMax,self.rMax])

    mask = cv2.inRange(small_img, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    maskedImage = cv2.bitwise_and(small_img,small_img,mask=mask)

    clone_img = copy.copy(small_img)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
      # find the largest contour in the mask, then use
      # it to compute the minimum enclosing circle and
      # centroid
      c = max(cnts, key=cv2.contourArea)
      ((x, y), radius) = cv2.minEnclosingCircle(c)
      M = cv2.moments(c)
      center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

      # only proceed if the radius meets a minimum size
      if radius > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(clone_img, (int(x), int(y)), int(radius),(0, 255, 255), 2)
        cv2.circle(clone_img, center, 5, (0, 0, 255), -1)

      cv2.imshow('Result',clone_img)
      print "X-centroid = " + str(x)
      print "y-centroid = " + str(y)

###############################################################################
# Load an image file
###############################################################################
  def loadImageButtonClicked(self):
    fileName = QFileDialog.getOpenFileName(None, "Select an image",".","Images (*.jpg *.png)")
    if not fileName:
      pass
    else:
      img = cv2.imread(str(fileName))
      small_img = cv2.resize(img,(640,480))
      # cv2.imshow(str(fileName),small_img)
      self.doTracker(small_img)

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
