import sys
import pwm_cmd
from PyQt4 import QtGui

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
        
        btn.clicked.connect(self.buttonClicked)
        
        self.setLayout(grid)
        
        self.show()
        
    def buttonClicked(self):
            enable = self.enableEdit.text()
            period = self.periodEdit.text()
            dutyCycle = self.dutyCycleEdit.text()
            pwm_cmd.Enable(enable)
            pwm_cmd.Period(period)
            pwm_cmd.DutyCycle(dutyCycle)


def main():
    app = QtGui.QApplication(sys.argv)
    
    pwm = PWM()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()