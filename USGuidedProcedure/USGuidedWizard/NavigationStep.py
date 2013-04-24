from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *

class NavigationStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '5. Navigation' )
    self.setDescription( 'Navigation step' )
   
    self.__parent = super( NavigationStep, self )
    self.igtlConnectorNode = None
    self.igtlRemoteLogic = None
    self.reconstructionSuspended = False
    self.reconstructionStarted = False
    self.outputVolFilename="PlusServerRecording.mha"
    self.outputVolDeviceName= "recvol_Reference"
    self.liveReconstruction=True
    self.volumesAddedToTheScene=[] #contains the unique ID of the volumes added to the scene 
  def createUserInterface( self ):
    '''
    '''
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()
    
    '''
    # Show the image in 3D
    showImageButton = qt.QPushButton("Show image in 3D")
    showImageButton.toolTip = "Shows the image in 3D"
    self.__layout.addWidget(showImageButton)
    showImageButton.connect('clicked(bool)', self.onShowRedSliceButtonClicked)

    
    # Show stylus
    showStylusButton = qt.QPushButton("Show stylus in 3D")
    showStylusButton.toolTip = "Shows stylus in 3D"
    self.__layout.addWidget(showStylusButton)
    showStylusButton.connect('clicked(bool)', self.onShowStylusButtonClicked)
    '''
    # Add Ultrasound Snapshot
    snapshotButton = qt.QPushButton("US snapshot")
    snapshotButton.toolTip = "Take an ultrasound snapshot"
    self.__layout.addWidget(snapshotButton)
    snapshotButton.connect('clicked(bool)', self.onSnapshotButtonClicked)
    
    # Volume reconstruction
    
    volumeReconstructionFrame=qt.QFrame()
    volumeReconstructionFrame.setLayout(qt.QHBoxLayout())
    volumeReconstructionLayout=volumeReconstructionFrame.layout()
    
     
    self.startReconstructionButton = qt.QPushButton("Start")
    self.startReconstructionButton.toolTip = "Start/Stop the volume reconstruction"
    volumeReconstructionLayout.addWidget(self.startReconstructionButton)
    self.startReconstructionButton.connect('clicked(bool)', self.onStartReconstructionButtonClicked)
    
    self.suspendReconstructionButton = qt.QPushButton("Suspend")
    self.suspendReconstructionButton.toolTip = "Suspend/Resume the volume reconstruction"
    self.suspendReconstructionButton.setEnabled(False)
    volumeReconstructionLayout.addWidget(self.suspendReconstructionButton)
    self.suspendReconstructionButton.connect('clicked(bool)', self.onSuspendReconstructionButtonClicked)
    
    self.getReconstructionSnapshotButton = qt.QPushButton("Snapshot")
    self.getReconstructionSnapshotButton.toolTip = "Get a volume reconstruction snapshot"
    volumeReconstructionLayout.addWidget(self.getReconstructionSnapshotButton)
    self.getReconstructionSnapshotButton.connect('clicked(bool)', self.onGetReconstructionSnapshotButtonClicked)
    
    self.__layout.addWidget(volumeReconstructionFrame)
    

    self.updateWidgetFromParameters(self.parameterNode())

    qt.QTimer.singleShot(0, self.killButton)

  def killButton(self):
    # hide useless button
    bl = slicer.util.findChildren(text='ReportROI')
    if len(bl):
      bl[0].hide()

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validationSucceeded(desiredBranchId)
    print("We are in the validate function of NavigationStep")

  def onEntry(self, comingFrom, transitionType):
    igtlRemote=slicer.modules.openigtlinkremote
    self.igtlRemoteLogic=igtlRemote.logic() 
    self.igtlRemoteLogic.SetMRMLScene(slicer.mrmlScene)
    self.igtlConnectorNode = slicer.util.getNode("Plus Server Connection")  
    
    super(NavigationStep, self).onEntry(comingFrom, transitionType)
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of NavigationStep")
    
    self.logic.showRedSliceIn3D()
    self.listenToScene()
    
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    

    super(NavigationStep, self).onExit(goingTo, transitionType) 
    print("We are in the onExit function of NavigationStep")
  def updateWidgetFromParameters(self, parameterNode):
    print("We are in the place fiducials step")


  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()

  def onShowRedSliceButtonClicked(self):
    self.logic.showRedSliceIn3D()

  def onShowStylusButtonClicked(self):
    self.logic.showStylusTipToRAS()
    
  def onSnapshotButtonClicked(self):
    self.logic.takeUSSnapshot2()  

  def onGetReconstructionSnapshotButtonClicked(self):
      self.logic.getVolumeReconstructionSnapshot(self.igtlRemoteLogic, self.igtlConnectorNode)
         
      
  def onStartReconstructionButtonClicked(self):
    self.reconstructionStarted = not self.reconstructionStarted
    if self.reconstructionStarted == True:
       self.logic.startVolumeReconstruction(self.igtlRemoteLogic, self.igtlConnectorNode,self.outputVolFilename,self.outputVolDeviceName)
       self.startReconstructionButton.setText("Stop")
       self.suspendReconstructionButton.setEnabled(True)
    else:
       self.logic.stopVolumeReconstruction(self.igtlRemoteLogic, self.igtlConnectorNode)
       self.startReconstructionButton.setText("Start")   
       self.suspendReconstructionButton.setEnabled(False)
    #while(not self.reconstructionSuspended):
    #print("Start sleeping")
    #time.sleep(5)
    #print("Finish sleeping")
    #self.logic.getVolumeReconstructionSnapshot(self.igtlRemoteLogic, self.igtlConnectorNode)
        
    
  def onSuspendReconstructionButtonClicked(self):
    self.reconstructionSuspended = not self.reconstructionSuspended
    if self.reconstructionSuspended == True:
       self.logic.suspendVolumeReconstruction(self.igtlRemoteLogic, self.igtlConnectorNode)
       self.suspendReconstructionButton.setText("Resume")
    else:
       self.logic.resumeVolumeReconstruction(self.igtlRemoteLogic, self.igtlConnectorNode)
       self.suspendReconstructionButton.setText("Suspend") 
       
       
  def listenToScene(self):
    self.sceneObserver = slicer.mrmlScene.AddObserver('ModifiedEvent', self.onVolumeAdded)
    
  def onVolumeAdded(self, caller,  event):  
     node=slicer.util.getNode(self.outputVolDeviceName)  
     if node is not None:
         isAlreadyAdded = False
         for object in self.volumesAddedToTheScene:
             if object is self.outputVolDeviceName:
                isAlreadyAdded = True 
         if not isAlreadyAdded:       
            self.volumesAddedToTheScene.append(self.outputVolDeviceName)
            print(self.outputVolDeviceName + " was added")
            
            volumePropertyNode=slicer.vtkMRMLVolumePropertyNode()
            slicer.mrmlScene.AddNode(volumePropertyNode)

            vrDisplayNode=slicer.vtkMRMLCPURayCastVolumeRenderingDisplayNode()
            vrDisplayNode.SetAndObserveVolumeNodeID(node.GetID())
            vrDisplayNode.SetAndObserveVolumePropertyNodeID(volumePropertyNode.GetID())
            slicer.mrmlScene.AddNode(vrDisplayNode)

            volumeDisplayNode=slicer.vtkMRMLScalarVolumeDisplayNode()
            volumeDisplayNode.SetThreshold(10,245)
            volumeDisplayNode.SetApplyThreshold(1)
            volumeDisplayNode.SetScalarRange(0,255)
            volumeDisplayNode.SetAutoWindowLevel(1)
            slicer.mrmlScene.AddNode(volumeDisplayNode)

            node.AddAndObserveDisplayNodeID(volumeDisplayNode.GetID())

            vrLogic = slicer.vtkSlicerVolumeRenderingLogic()
            vrLogic.SetMRMLScene(slicer.mrmlScene)
            #vrLogic.CopyScalarDisplayToVolumeRenderingDisplayNode(vrDisplayNode,volumeDisplayNode)
            vtkvp=volumePropertyNode.GetVolumeProperty()
            vrLogic.SetThresholdToVolumeProp([0,250],[30,230],vtkvp,True,True)
         #if self.liveReconstruction==True:
         #   self.logic.getVolumeReconstructionSnapshot(self.igtlRemoteLogic, self.igtlConnectorNode)