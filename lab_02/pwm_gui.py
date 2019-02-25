# Author: Adib Yahaya
# Date: 2/24/2019
# CPET563 Lab 2: PWM module with GUI

import sys
import pwm_cmd
from PyQt4 import QtGui, QtCore

class PWM(QtGui.QWidget):
    def __init__(self):
        super(PWM, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PWM Module')
        self.resize(350, 250)

        enable = QtGui.QLabel('Enable')
        period = QtGui.QLabel('Period')
        dutyCycle = QtGui.QLabel('Duty Cycle')
        self.status = QtGui.QLabel('')

        self.enableEdit = QtGui.QLineEdit()
        self.periodEdit = QtGui.QLineEdit()
        self.dutyCycleEdit = QtGui.QLineEdit()

        btn = QtGui.QPushButton('Set configurations', self)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(enable, 1, 0)
        grid.addWidget(self.enableEdit, 1, 1)

        grid.addWidget(period, 2, 0)
        grid.addWidget(self.periodEdit, 2, 1)

        grid.addWidget(dutyCycle, 3, 0)
        grid.addWidget(self.dutyCycleEdit, 3, 1)

        grid.addWidget(btn, 4, 0)
        
        grid.addWidget(self.status, 5, 0)

        btn.clicked.connect(self.buttonClicked)

        self.setLayout(grid)

        self.show()

    def buttonClicked(self):
        enable    = self.enableEdit.text()
        period    = self.periodEdit.text()
        dutyCycle = self.dutyCycleEdit.text()

        # Send value written on GUI to Snickerdoodle /dev/mem
        # Enable: reg = 0
        # Period: reg = 4
        # Duty Cycle: reg = 8
        en_result        = pwm_cmd.WriteToMem(enable, 0)
        period_result    = pwm_cmd.WriteToMem(period, 4)
        dutyCycle_result = pwm_cmd.WriteToMem(dutyCycle, 8)

        if (en_result and period_result and dutyCycle_result):
            if (enable == '1'):
                self.status.setText("PWM is running!")
            else:
                self.status.setText("PWM is not running")
        else:
            # Disable PWM if failed to write to any reg
            pwm_cmd.WriteToMem(0, 0)
            self.status.setText("Error occurred")

def main():
    app = QtGui.QApplication(sys.argv)
    pwm = PWM()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
