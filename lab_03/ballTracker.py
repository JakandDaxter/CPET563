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
    layout_selectBall = QHBoxLayout()
    layout_loadImage = QHBoxLayout()
    layout_centroidLabel = QHBoxLayout()
    layout_centroidValue = QHBoxLayout()
    layout_loadsaveParam = QHBoxLayout()
    layout_sliders = QVBoxLayout()

    self.ballSelectLabel = QLabel(self)
    self.ballSelectLabel.setText("Select which ball to track:")

    self.blueBallBtn = QRadioButton("Blue ball")
    self.blueBallBtn.setChecked(False)
    self.blueBallBtn.toggled.connect(lambda:self.setParamViaBtn(self.blueBallBtn))

    self.greenBallBtn = QRadioButton("Green ball")
    self.greenBallBtn.setChecked(False)
    self.greenBallBtn.toggled.connect(lambda:self.setParamViaBtn(self.greenBallBtn))

    self.ballColorGroup = QButtonGroup()
    self.ballColorGroup.addButton(self.blueBallBtn)
    self.ballColorGroup.addButton(self.greenBallBtn)

    self.loadImageBtn = QPushButton("Load Image File")
    self.loadImageBtn.clicked[bool].connect(self.loadImageButtonClicked)

    self.loadParamFileBtn = QPushButton("Load Parameters File")
    self.loadParamFileBtn.clicked[bool].connect(self.loadParamFileButtonClicked)

    self.saveParamFileBtn = QPushButton("Save Parameters File")
    self.saveParamFileBtn.clicked[bool].connect(self.saveParamFileButtonClicked)

    self.XcentroidLabel = QLabel(self)
    self.XcentroidLabel.setText("X-centroid:")
    self.XcentroidValueLabel = QLabel(self)
    self.XcentroidValueLabel.setText("")

    self.YcentroidLabel = QLabel(self)
    self.YcentroidLabel.setText("Y-centroid:")
    self.YcentroidValueLabel = QLabel(self)
    self.YcentroidValueLabel.setText("")

    self.rMinLabel = QLabel(self)
    self.rMinLabel.setText("Red min")
    self.rMinSlider = QSlider(Qt.Horizontal)
    self.rMinSlider.setMinimum(0)
    self.rMinSlider.setMaximum(255)
    self.rMinSlider.valueChanged.connect(self.sliderValueChanged_redMin)

    self.rMaxLabel = QLabel(self)
    self.rMaxLabel.setText("Red max")
    self.rMaxSlider = QSlider(Qt.Horizontal)
    self.rMaxSlider.setMinimum(0)
    self.rMaxSlider.setMaximum(255)
    self.rMaxSlider.valueChanged.connect(self.sliderValueChanged_redMax)

    self.gMinLabel = QLabel(self)
    self.gMinLabel.setText("Green min")
    self.gMinSlider = QSlider(Qt.Horizontal)
    self.gMinSlider.setMinimum(0)
    self.gMinSlider.setMaximum(255)
    self.gMinSlider.valueChanged.connect(self.sliderValueChanged_greenMin)

    self.gMaxLabel = QLabel(self)
    self.gMaxLabel.setText("Green max")
    self.gMaxSlider = QSlider(Qt.Horizontal)
    self.gMaxSlider.setMinimum(0)
    self.gMaxSlider.setMaximum(255)
    self.gMaxSlider.valueChanged.connect(self.sliderValueChanged_greenMax)

    self.bMinLabel = QLabel(self)
    self.bMinLabel.setText("Blue min")
    self.bMinSlider = QSlider(Qt.Horizontal)
    self.bMinSlider.setMinimum(0)
    self.bMinSlider.setMaximum(255)
    self.bMinSlider.valueChanged.connect(self.sliderValueChanged_blueMin)

    self.bMaxLabel = QLabel(self)
    self.bMaxLabel.setText("Blue max")
    self.bMaxSlider = QSlider(Qt.Horizontal)
    self.bMaxSlider.setMinimum(0)
    self.bMaxSlider.setMaximum(255)
    self.bMaxSlider.valueChanged.connect(self.sliderValueChanged_blueMax)

    layout_selectBall.addWidget(self.ballSelectLabel)
    layout_selectBall.addWidget(self.blueBallBtn)
    layout_selectBall.addWidget(self.greenBallBtn)

    layout_loadImage.addWidget(self.loadImageBtn)

    layout_centroidLabel.addWidget(self.XcentroidLabel)
    layout_centroidLabel.addWidget(self.YcentroidLabel)

    layout_centroidValue.addWidget(self.XcentroidValueLabel)
    layout_centroidValue.addWidget(self.YcentroidValueLabel)

    layout_loadsaveParam.addWidget(self.loadParamFileBtn)
    layout_loadsaveParam.addWidget(self.saveParamFileBtn)

    layout_sliders.addWidget(self.rMinLabel)
    layout_sliders.addWidget(self.rMinSlider)
    layout_sliders.addWidget(self.rMaxLabel)
    layout_sliders.addWidget(self.rMaxSlider)

    layout_sliders.addWidget(self.gMinLabel)
    layout_sliders.addWidget(self.gMinSlider)
    layout_sliders.addWidget(self.gMaxLabel)
    layout_sliders.addWidget(self.gMaxSlider)

    layout_sliders.addWidget(self.bMinLabel)
    layout_sliders.addWidget(self.bMinSlider)
    layout_sliders.addWidget(self.bMaxLabel)
    layout_sliders.addWidget(self.bMaxSlider)

    layout.addLayout(layout_selectBall)
    layout.addLayout(layout_sliders)
    layout.addLayout(layout_loadImage)
    layout.addLayout(layout_centroidLabel)
    layout.addLayout(layout_centroidValue)
    layout.addLayout(layout_loadsaveParam)
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
        self.rMax = 50
        self.gMin = 0
        self.gMax = 255
        self.bMin = 0
        self.bMax = 120

  def uncheckRadioButton(self):
    self.ballColorGroup.setExclusive(False)
    self.blueBallBtn.setChecked(False)
    self.greenBallBtn.setChecked(False)
    self.ballColorGroup.setExclusive(True)

  def sliderValueChanged_redMin(self):
    value = self.rMinSlider.value()
    self.rMin = value
    self.uncheckRadioButton()
    try:
      self.doTracker(self.small_img)
    except:
      pass

  def sliderValueChanged_redMax(self):
    value = self.rMaxSlider.value()
    self.rMax = value
    self.uncheckRadioButton()
    try:
      self.doTracker(self.small_img)
    except:
      pass

  def sliderValueChanged_greenMin(self):
    value = self.gMinSlider.value()
    self.gMin = value
    self.uncheckRadioButton()
    try:
      self.doTracker(self.small_img)
    except:
      pass

  def sliderValueChanged_greenMax(self):
    value = self.gMaxSlider.value()
    self.gMax = value
    self.uncheckRadioButton()
    try:
      self.doTracker(self.small_img)
    except:
      pass

  def sliderValueChanged_blueMin(self):
    value = self.bMinSlider.value()
    self.bMin = value
    self.uncheckRadioButton()
    try:
      self.doTracker(self.small_img)
    except:
      pass

  def sliderValueChanged_blueMax(self):
    value = self.bMaxSlider.value()
    self.bMax = value
    self.uncheckRadioButton()
    try:
      self.doTracker(self.small_img)
    except:
      pass

  def displayCentroidValue(self, which, val):
    if val != "" and val != 0:
      if which == "X":
        self.XcentroidValueLabel.setText(str(val))
        print "X-centroid = " + str(val)
      else:
        self.YcentroidValueLabel.setText(str(val))
        print "Y-centroid = " + str(val)
    # If empty or invalid, reset labels
    else:
      self.XcentroidValueLabel.setText("NA")
      self.YcentroidValueLabel.setText("NA")

  def doTracker(self, small_img):
    if not small_img.any():
      # No image loaded
      print "error loading image"
    else:
      x = 0
      y = 0
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
      self.displayCentroidValue("X", x)
      self.displayCentroidValue("Y", y)

###############################################################################
# Load an image file
###############################################################################
  def loadImageButtonClicked(self):
    fileName = QFileDialog.getOpenFileName(None, "Select an image",".","Images (*.jpg *.png)")
    if not fileName:
      pass
    else:
      img = cv2.imread(str(fileName))
      self.small_img = cv2.resize(img,(640,480))
      # cv2.imshow(str(fileName),self.small_img)
      self.doTracker(self.small_img)

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
      # Uncheck all radio buttons selecting which ball
      # because a custom parameters file has been loaded
      self.uncheckRadioButton()

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
