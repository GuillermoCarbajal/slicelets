from __main__ import vtk, qt, ctk, slicer
import sys
import time

# class SleepProgress(qt.QThread):
#     
#  procDone = qt.pyqtSignal(bool)
#  partDone = qt.pyqtSignal(int)
#  def run(self):
#        print 'proc started'
#        for a in range(1, 1+35):
#              self.partDone.emit(float(a)/35.0*100)
#              print 'sleep', a
#              time.sleep(0.13)
# 
#        self.procDone.emit(True)   
#        print 'proc ended'
#  
 
class AddProgresWin(qt.QWidget):
 def __init__(self, parent=None):
       super(AddProgresWin, self).__init__(parent)

       #self.thread = SleepProgress()

       self.nameLabel = qt.QLabel("0.0%")
       self.nameLine = qt.QLineEdit()
       
       self.taskLabel = qt.QLabel("The volume is being processed. Please wait...")
       
       
       self.progressbar = qt.QProgressBar()
       self.progressbar.setMinimum(0)
       self.progressbar.setMaximum(0)

       mainLayout = qt.QVBoxLayout()
       mainLayout.addWidget(self.taskLabel)
       mainLayout.addWidget(self.progressbar)
       #mainLayout.addWidget(self.nameLabel, 0, 1)

       self.setLayout(mainLayout)
       self.setWindowTitle("Work in progress")

       #self.thread.partDone.connect(self.updatePBar)
       #self.thread.procDone.connect(self.fin)

       #self.thread.start()

 def updatePBar(self, val):
       self.progressbar.setValue(val)   
       perct = "{0}%".format(val)
       self.nameLabel.setText(perct)

 def fin(self):
      sys.exit()
      ##self.hide()        