from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *
from WorkInProgress import *

class NavigationStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '5. Navigation' )
    #self.setDescription( 'Navigation step' )
   
    self.__parent = super( NavigationStep, self )
    #self.igtlConnectorNode = None
    self.igtlRemoteLogic = None
    self.reconstructionSuspended = False
    self.reconstructionStarted = False
    self.exploreVolume = False
    self.reconstructedVolumePrefix="recvol"
    #self.outputVolFilename="recvol_Reference.mha"
    self.numberOfGeneratedVolumes=0;
    self.volumeReferenceFrame="Reference"
    self.outputVolFilename=self.reconstructedVolumePrefix+str(self.numberOfGeneratedVolumes)+"_"+self.volumeReferenceFrame+".mha"
    #self.outputVolDeviceName= "recvol_Reference"
    self.outputVolDeviceName= self.reconstructedVolumePrefix+str(self.numberOfGeneratedVolumes)+"_"+self.volumeReferenceFrame
    self.liveReconstruction=True
    self.volumesAddedToTheScene=[] #contains the unique ID of the volumes added to the scene 
    self.scalarRange=[0.,255.]
    self.windowLevelMinMax=[0.1,254.99]
    self.preAcquireVolumeReconstructionSequence=True
    self.preAcquisitionFilename="acquiredFramesForVolumeReconstruction"+str(self.numberOfGeneratedVolumes)+".mha"
    
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
      
    self.isTrackingFrame = qt.QFrame()
    self.isTrackingFrame.setLayout(qt.QHBoxLayout())
    self.__layout.addWidget(self.isTrackingFrame)

    self.isTrackingLabel = qt.QLabel("Tracking enabled: ", self.isTrackingFrame)
    self.isTrackingLabel.setToolTip( "Enable/Disable the tracking")
    self.isTrackingFrame.layout().addWidget(self.isTrackingLabel)

    self.isTrackingCheckBox = qt.QCheckBox(self.isTrackingFrame)
    self.isTrackingCheckBox.setCheckState(2)
    self.isTrackingFrame.layout().addWidget(self.isTrackingCheckBox)
    self.isTrackingCheckBox.connect("stateChanged(int)",self.onTrackingStateChanged)
      
    # Add Ultrasound Snapshot
    snapshotButton = qt.QPushButton("US snapshot")
    snapshotButton.toolTip = "Take an ultrasound snapshot"
    self.__layout.addWidget(snapshotButton)
    snapshotButton.connect('clicked(bool)', self.onSnapshotButtonClicked)
    
    # Add target button
    addTargetButton = qt.QPushButton("Add target")
    addTargetButton.toolTip = "Add a target to the scene"
    self.__layout.addWidget(addTargetButton)
    addTargetButton.connect('clicked(bool)', self.onAddTargetButtonClicked)
    
    # Volume reconstruction
    
    volumeReconstructionFrame=qt.QFrame()
    volumeReconstructionFrame.setLayout(qt.QVBoxLayout())
    volumeReconstructionLayout=volumeReconstructionFrame.layout()
    
    self.volumeReconstructionLabel = qt.QLabel("Volume reconstruction: ", self.isTrackingFrame)
    self.volumeReconstructionLabel.setToolTip( "Perform volume reconstruction")
    volumeReconstructionFrame.layout().addWidget(self.volumeReconstructionLabel)
    
    
    self.preAcquisitionFrame=qt.QFrame()
    self.preAcquisitionFrame.setLayout(qt.QHBoxLayout())
    self.preAcquisitionLayout=self.preAcquisitionFrame.layout()
    
    self.isPreAcquisitionLabel = qt.QLabel("Pre Adquisition: ", volumeReconstructionFrame)
    self.isPreAcquisitionLabel.setToolTip( "Enable/Disable the pre adquisition. It is important to pre adquire a sequence to determine the extent of the volume")
    self.preAcquisitionLayout.addWidget(self.isPreAcquisitionLabel)

    self.isPreAcquisitionCheckBox = qt.QCheckBox(self.isTrackingFrame)
    self.isPreAcquisitionCheckBox.setCheckState(0)
    self.preAcquisitionLayout.addWidget(self.isPreAcquisitionCheckBox)
    self.isPreAcquisitionCheckBox.connect("stateChanged(int)",self.onPreAcquisitionStateChanged)
    
    self.volumeReconstructionButtonsFrame=qt.QFrame()
    self.volumeReconstructionButtonsFrame.setLayout(qt.QHBoxLayout())
    self.volumeReconstructionButtonsLayout=self.volumeReconstructionButtonsFrame.layout()
    
     
    self.startReconstructionButton = qt.QPushButton("Start")
    self.startReconstructionButton.toolTip = "Start/Stop the volume reconstruction"
    self.volumeReconstructionButtonsLayout.addWidget(self.startReconstructionButton)
    self.startReconstructionButton.connect('clicked(bool)', self.onStartReconstructionButtonClicked)
    
    self.suspendReconstructionButton = qt.QPushButton("Suspend")
    self.suspendReconstructionButton.toolTip = "Suspend/Resume the volume reconstruction"
    self.suspendReconstructionButton.setEnabled(False)
    self.volumeReconstructionButtonsLayout.addWidget(self.suspendReconstructionButton)
    self.suspendReconstructionButton.connect('clicked(bool)', self.onSuspendReconstructionButtonClicked)
    
    #volumeReconstructionFrame.layout().addWidget(self.preAcquisitionFrame)
    volumeReconstructionFrame.layout().addWidget(self.volumeReconstructionButtonsFrame)
    
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
    
    self.logic.showRedSliceIn3D(1)
      
    # If the Target list does not exit, it is created.
    self.listenToTargetListModification()
      
    igtlRemote=slicer.modules.openigtlinkremote
    self.igtlRemoteLogic=igtlRemote.logic() 
    self.igtlRemoteLogic.SetMRMLScene(slicer.mrmlScene)
    self.igtlConnectorNode = self.logic.getConnectorNode() #slicer.util.getNode("Plus Server Connection")  
    
    super(NavigationStep, self).onEntry(comingFrom, transitionType)
    
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of NavigationStep")
    
    
    # listen to volumes added
    self.listenToVolumesAdded()
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
    self.logic.showRedSliceIn3D(True)

  def onShowStylusButtonClicked(self):
    self.logic.showStylusTipToRAS()
    
  def onSnapshotButtonClicked(self):
    self.logic.takeUSSnapshot2()  
         
      
  def onStartReconstructionButtonClicked(self):
    if not self.preAcquireVolumeReconstructionSequence:  
      self.reconstructionStarted = not self.reconstructionStarted
      if self.reconstructionStarted == True:
         self.logic.startVolumeReconstruction(self.igtlRemoteLogic, self.igtlConnectorNode,self.outputVolFilename,self.outputVolDeviceName)
         print("volume reconstruction started!")
         self.startReconstructionButton.setText("Stop")
         self.suspendReconstructionButton.setEnabled(True)
         #self.logic.getVolumeReconstructionSnapshot(self.igtlRemoteLogic, self.igtlConnectorNode)
      else:
         self.logic.stopVolumeReconstruction(self.igtlRemoteLogic, self.igtlConnectorNode)
         print("volume reconstruction stopped!")
         self.startReconstructionButton.setText("Start")   
         self.suspendReconstructionButton.setEnabled(False)
    else:
      self.reconstructionStarted = not self.reconstructionStarted
      if self.reconstructionStarted == True:
         self.logic.startAcquisition(self.igtlRemoteLogic, self.igtlConnectorNode,self.preAcquisitionFilename)
         print("pre acquisition started!")
         self.startReconstructionButton.setText("Stop")
         #self.suspendReconstructionButton.setEnabled(True)
         #self.logic.getVolumeReconstructionSnapshot(self.igtlRemoteLogic, self.igtlConnectorNode)
      else:
         self.logic.stopAcquisition(self.igtlRemoteLogic, self.igtlConnectorNode)
         print("pre acquisition stopped!")
         self.startReconstructionButton.setText("Start")   
         self.logic.reconstructVolume(self.igtlRemoteLogic, self.igtlConnectorNode,self.preAcquisitionFilename,self.outputVolFilename,self.outputVolDeviceName)
         self.numberOfGeneratedVolumes+=1
         self.pbarwin = AddProgresWin()
         self.pbarwin.show()
         #self.suspendReconstructionButton.setEnabled(False) 
         #node=slicer.vtkMRMLScalarVolumeNode()
         #node.SetName(self.outputVolDeviceName)
         #slicer.mrmlScene.AddNode(node)

      #while(not self.reconstructionSuspended):
      #print("Start sleeping")
      #time.sleep(5)
      #print("Finish sleeping")
      #self.logic.getVolumeReconstructionSnapshot(self.igtlRemoteLogic, self.igtlConnectorNode)
        
    
  def onSuspendReconstructionButtonClicked(self):
    if not self.preAcquireVolumeReconstructionSequence:   
      self.reconstructionSuspended = not self.reconstructionSuspended
      if self.reconstructionSuspended == True:
         self.logic.suspendVolumeReconstruction(self.igtlRemoteLogic, self.igtlConnectorNode)
         self.suspendReconstructionButton.setText("Resume")
      else:
         self.logic.resumeVolumeReconstruction(self.igtlRemoteLogic, self.igtlConnectorNode)
         self.suspendReconstructionButton.setText("Suspend") 
        
            
  def listenToVolumesAdded(self):
    self.sceneObserver = slicer.mrmlScene.AddObserver('ModifiedEvent', self.onVolumeAdded)

  def listenToTargetListModification(self):
    fiducialListNode=slicer.util.getNode("Target List")
    fiducialListNode.AddObserver('ModifiedEvent', self.onTargetListModification)
    
  def onVolumeAdded(self, caller,  event):  
      node = slicer.util.getNode(self.outputVolDeviceName)
      if not node==None:
         vl=slicer.modules.volumes
         vl=vl.logic()
         vl.Modified()
         self.pbarwin.hide()
         self.outputVolFilename=self.reconstructedVolumePrefix+str(self.numberOfGeneratedVolumes)+"_"+self.volumeReferenceFrame+".mha"
         self.outputVolDeviceName=self.reconstructedVolumePrefix+str(self.numberOfGeneratedVolumes)+"_"+self.volumeReferenceFrame
         self.preAcquisitionFilename="acquiredFramesForVolumeReconstruction"+str(self.numberOfGeneratedVolumes)+".mha"
         
         
  def onAddTargetButtonClicked(self):   
      self.logic.addFiducialToList("Target List")   
      
  def onTargetListModification(self, caller, event):
      print ("Target List was modified")
      # populate the list
      targetListNode=slicer.util.getNode("Target List")
          
      print "Number of target: " + str(targetListNode.GetNumberOfChildrenNodes())
      for childrenIndex in xrange(targetListNode.GetNumberOfChildrenNodes()):
          fidHierarchyNode=targetListNode.GetNthChildNode(childrenIndex)
          fidNode=fidHierarchyNode.GetAssociatedNode()
          fidNode.SetName("T"+str(childrenIndex))
          fidDisplayNode=fidNode.GetAnnotationPointDisplayNode()
          fidTextDisplay=fidNode.GetAnnotationTextDisplayNode()
          fidDisplayNode.SetColor([0,0,1])
          fidTextDisplay.SetColor([0,0,1])
          if not fidNode:
            print 'Fid node nulo'
            continue       
  def onTrackingStateChanged(self,status):     
        if status==2:
            self.logic.startTracking()
            self.logic.showRedSliceIn3D(True)
        else:
            self.logic.stopTracking()
            self.logic.showRedSliceIn3D(False)
            
  def onPreAcquisitionStateChanged(self,status):     
        if status==2:
            self.preAcquireVolumeReconstructionSequence=True
        else:
            self.preAcquireVolumeReconstructionSequence=False         
        