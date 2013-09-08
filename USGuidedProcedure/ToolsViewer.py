'''
Created on 28/03/2013

@author: Usuario
'''
import os
from PropertiesMenu import *

from __main__ import vtk, qt, ctk, slicer

class ToolsViewer():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.notVisibleStyle ="background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d55, stop: 0.1 #e66, stop: 0.49 #c44, stop: 0.5 #b33, stop: 1 #c44);"
        self.visibleStyle =  "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5d5, stop: 0.1 #6e6, stop: 0.49 #4c4, stop: 0.5 #3b3, stop: 1 #4c4);"
        self.noTrackingStyle = "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ddd, stop: 0.1 #eee, stop: 0.49 #ccc, stop: 0.5 #bbb, stop: 1 #ccc);"
        self.toolsWidget = qt.QFrame() 
        self.toolsWidget.setLayout( qt.QHBoxLayout() )
        
        # stylus semaphore
        self.stylusSemaphore=qt.QPushButton()
        self.stylusSemaphore.setEnabled(False)
        self.stylusSemaphore.setStyleSheet(self.noTrackingStyle)
        self.stylusSemaphore.setText("S") 
        
        # probe semaphore
        self.probeSemaphore=qt.QPushButton()
        self.probeSemaphore.setEnabled(False)
        self.probeSemaphore.setStyleSheet(self.noTrackingStyle)
        self.probeSemaphore.setText("P") 
        
        # reference semaphore
        self.referenceSemaphore=qt.QPushButton()
        self.referenceSemaphore.setEnabled(False)
        self.referenceSemaphore.setStyleSheet(self.noTrackingStyle)
        self.referenceSemaphore.setText("R") 
        
        self.toolsWidget.layout().addWidget(self.stylusSemaphore) 
        self.toolsWidget.layout().addWidget(self.probeSemaphore) 
        self.toolsWidget.layout().addWidget(self.referenceSemaphore) 
         
        print("Constructor of ToolViewer executed")
        self.toolsWidget.show()
        
        
    def getToolsWidget(self):
      return self.toolsWidget
      
    def setModuleLogic(self,logic):   
        self.logic=logic
          
#     def listenToScene(self):     
#         igtl=slicer.modules.openigtlinkif
#         logic=igtl.logic()
#         logic.SetMRMLScene(slicer.mrmlScene)
#         #self.connectorNode=self.logic.getConnectorNode()
#         logic.AddObserver('ModifiedEvent',self.onConnectedEventCaptured)

     
#     def onConnectedEventCaptured(self, caller,  event):
#         print "An OpenIGTLink connection was captured!"
#         igtlConnectorNode = slicer.util.getNode("Plus Server Connection") 
#         if igtlConnectorNode is not None:
#             self.startListeningToTransformationsModifications()
            
    def startListeningToTransformationsModifications(self):    
        print "Tools viewer is listening to the scene"
        
        referenceToTrackerNode = slicer.util.getNode("ReferenceToTracker")
        #if referenceToTrackerNode is not None:
        #    self.onReferenceTransformationModified()
        referenceToTrackerNode.AddObserver('ModifiedEvent', self.onReferenceTransformationModified)
       
        probeToReference = slicer.util.getNode("ProbeToReference")
        #if probeToReference is not None:
        #    self.onProbeTransformationModified()
        probeToReference.AddObserver('ModifiedEvent', self.onProbeTransformationModified)
       
        stylusToReference = slicer.util.getNode("StylusTipToReference")
        #if stylusToReference is not None:
        #    self.onStylusTransformationModified()
        stylusToReference.AddObserver('ModifiedEvent', self.onStylusTransformationModified)
        stylusModelNode=self.logic.getStylusModel()
        self.stylusModelDisplayNode=stylusModelNode.GetDisplayNode()
        self.stylusModelDisplayNode.SetVisibility(False)    
        
        
    def onReferenceTransformationModified(self, caller,  event):
        if self.logic.isValidTransformation("ReferenceToTracker"):
          self.referenceSemaphore.setStyleSheet(self.visibleStyle) 
        else:
          self.referenceSemaphore.setStyleSheet(self.notVisibleStyle)  
    
    def onProbeTransformationModified(self, caller,  event):
        if self.logic.isValidTransformation("ProbeToReference"):
          self.probeSemaphore.setStyleSheet(self.visibleStyle) 
        else:
          self.probeSemaphore.setStyleSheet(self.notVisibleStyle)   
          
    def onStylusTransformationModified(self):
        if self.logic.isValidTransformation("StylusTipToReference"):
          self.stylusSemaphore.setStyleSheet(self.visibleStyle) 
          self.stylusModelDisplayNode.SetVisibility(True)  
        else:
          self.stylusSemaphore.setStyleSheet(self.notVisibleStyle)
          self.stylusModelDisplayNode.SetVisibility(False)    
                    
         
        