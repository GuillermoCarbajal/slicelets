'''
Created on 28/03/2013

@author: Usuario
'''
import os

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
        self.stylusSemaphore.setText("Stylus Tip") 
        
        # probe semaphore
        self.probeSemaphore=qt.QPushButton()
        self.probeSemaphore.setEnabled(False)
        self.probeSemaphore.setStyleSheet(self.noTrackingStyle)
        self.probeSemaphore.setText("Probe") 
         
        self.toolsWidget.layout().addWidget(self.stylusSemaphore) 
        self.toolsWidget.layout().addWidget(self.probeSemaphore)  
        print("Constructor of ToolViewer executed")
        
        
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
       
        trackerToProbe = slicer.util.getNode("TrackerToProbe")
        trackerToProbe.RemoveAllObservers()
        #if probeToReference is not None:
        #    self.onProbeTransformationModified()
        trackerToProbe.AddObserver('ModifiedEvent', self.onProbeTransformationModified)
       
        stylusTipToTracker = slicer.util.getNode("StylusTipToTracker")
        stylusTipToTracker.RemoveAllObservers()
        #if stylusToReference is not None:
        #    self.onStylusTransformationModified()
        stylusTipToTracker.AddObserver('ModifiedEvent', self.onStylusTransformationModified)
       
        stylusModelNode=self.logic.getStylusModel()
        self.stylusModelDisplayNode=stylusModelNode.GetDisplayNode()
        self.stylusModelDisplayNode.SetVisibility(False)    
        
        
    
    def onProbeTransformationModified(self, caller,  event):
        if self.logic.isValidTransformation("TrackerToProbe"):
          self.probeSemaphore.setStyleSheet(self.visibleStyle) 
          #print "Probe Transformation is valid!!"
        else:
          self.probeSemaphore.setStyleSheet(self.notVisibleStyle)  
          #print "Probe Transformation is invalid!!" 
          
    def onStylusTransformationModified(self, caller,  event):
        if self.logic.isValidTransformation("StylusTipToTracker"):
          self.stylusSemaphore.setStyleSheet(self.visibleStyle) 
          self.stylusModelDisplayNode.SetVisibility(True)  
        else:
          self.stylusSemaphore.setStyleSheet(self.notVisibleStyle)
          self.stylusModelDisplayNode.SetVisibility(False)    
                    
     
    def listenToTransformationsSentToTheScene(self):
      self.sceneObserver = slicer.mrmlScene.AddObserver('ModifiedEvent', self.onTransformationsSentToTheScene)  
      
    def doNotListenToTransformationsSentToTheScene(self):
      slicer.mrmlScene.RemoveObserver(self.sceneObserver)

    def onTransformationsSentToTheScene(self, caller, event):
      image_Image = slicer.util.getNode("Image_Image")   
      if image_Image is not None: 
        self.doNotListenToTransformationsSentToTheScene() 
        self.logic.associateTransformations()  
        self.startListeningToTransformationsModifications()
        slicer.util.resetSliceViews() 
        slicer.util.resetThreeDViews()      
        