from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *
from FiducialsList import *

import os

class CaptureSpatialPositionsStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '2. Capture spatial positions step' )
    #self.setDescription( 'Place fiducials using the tracker' )

    self.__parent = super( CaptureSpatialPositionsStep, self )
    self.numberOfAcquiredSpatialPositions = 0

  def createUserInterface( self ):
    '''
    '''
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()

#    # Place Tracker Position
#    placeTrackerPositionButton = qt.QPushButton("Add tracker position")
#    placeTrackerPositionButton.toolTip = "Add a tracker position to the list"
#    self.__layout.addWidget(placeTrackerPositionButton)
#    placeTrackerPositionButton.connect('clicked(bool)', self.onPlaceTrackerPositionButtonClicked)
#    
#    # Load a tracker list 
#    loadTrackerListButton = qt.QPushButton("Test spatial points lists creation")
#    loadTrackerListButton.toolTip = "Load spatial points to test registration"
#    self.__layout.addWidget(loadTrackerListButton)
#    loadTrackerListButton.connect('clicked(bool)', self.onLoadSpatialPointsListClicked)


    self.fiducialsList = FiducialsList()
    self.fiducialsList.setModuleLogic(self.logic)
    self.__layout.addWidget(self.fiducialsList.getFiducialsWidget())
    self.fiducialsWidget = self.fiducialsList.getFiducialsWidget()
    
    #customize the UI
    self.fiducialsWidget.placeSpatialButton.setVisible(True)
    self.fiducialsWidget.placeFiducialButton.setVisible(False)
    self.fiducialsWidget.fiducialsList.setColumnHidden(2, True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(4, True)

    #connect signals and slots
    self.fiducialsWidget.placeSpatialButton.connect('clicked(bool)', self.onPlaceTrackerPositionButtonClicked)


    self.updateWidgetFromParameters(self.parameterNode())
    self.updateGeometry()

    qt.QTimer.singleShot(0, self.killButton)
    print("Fiducials Widget size Hint:")
    self.fiducialsWidget.sizeHint
    print("Fiducials Widget size :")
    self.fiducialsWidget.size
    print("Spatial fiducials step size Hint:")
    print self.sizeHint
    print("Spatial fiducials step size")
    print self.size

  def killButton(self):
    # hide useless button
    bl = slicer.util.findChildren(text='ReportROI')
    if len(bl):
      bl[0].hide()

  def validate( self, desiredBranchId ):
    '''
    '''
    self.__parent.validationSucceeded(desiredBranchId)
    print("We are in the validate function of CaptureSpatialPositionsStepStep")

  def onEntry(self, comingFrom, transitionType):

    super(CaptureSpatialPositionsStep, self).onEntry(comingFrom, transitionType)
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    
    
    print("We are in the onEntry function of CaptureSpatialPositionsStepStep coming from:" )
    print comingFrom.name()
    qt.QTimer.singleShot(0, self.killButton)
    

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    super(CaptureSpatialPositionsStep, self).onExit(goingTo, transitionType) 
    print("We are in the onExit function of CaptureSpatialPositionsStepStep")

  def updateWidgetFromParameters(self, parameterNode):
    print("We are in the place fiducials step")
    self.fiducialsList.updateSpatialFiducialsList()
    #self.updateTrackerPointsList()
    



  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()

#  def onPlaceTrackerPositionButtonClicked(self):   
#    self.logic.recordTrackerPosition()
#    

  def onLoadSpatialPointsListClicked(self):  
    self.logic.addFiducialsToTrackerList()   


  def onPlaceTrackerPositionButtonClicked(self):   
    
    fiducialName = "F" + str(self.numberOfAcquiredSpatialPositions)
    positionRecorded= self.logic.captureSpatialsPositions(fiducialName)
    
    path=slicer.modules.stylusbasedusprobecalibration.path
    modulePath=os.path.dirname(path)
    
    if positionRecorded==True:
        #get the most recent node (the last) in the Tracker Points List
        #trackerNode = slicer.util.getNode(fiducialName+"-Tracker")
#         trackerNode = self.logic.getFiducialNode('Tracker Points List', -1)
#     
#     
#         # Associate the fiducial and the tracker position
#         # We remove the previous (if exist) tracker node 
#         # and we put the new tracker node ID in the table and check the row
#         currentItem = self.fiducialsWidget.fiducialsList.item(self.numberOfAcquiredSpatialPositions , 4)
#         if currentItem is None:
#           self.fiducialsList.addNewEmptyRow(self.numberOfAcquiredSpatialPositions)        
#     
#         currentItem = self.fiducialsWidget.fiducialsList.item(self.numberOfAcquiredSpatialPositions , 4)
#         
#         self.fiducialsWidget.fiducialsList.item(self.numberOfAcquiredSpatialPositions , 3).setText(trackerNode.GetName())
#         self.fiducialsWidget.fiducialsList.item(self.numberOfAcquiredSpatialPositions , 4).setText(trackerNode.GetID())
#         self.fiducialsWidget.fiducialsList.item(self.numberOfAcquiredSpatialPositions , 0).setCheckState(2)
        
        self.fiducialsList.updateFiducialsList("Tracker Points List")
      
        soundFile=os.path.join(modulePath,"sounds/notify.wav")
        sound=qt.QSound(soundFile)
        sound.play()    
        self.numberOfAcquiredSpatialPositions += 1
    else:
        soundFile=os.path.join(modulePath,"sounds/critico.wav") 
        #sound=qt.QSound("C:\Users\Usuario\devel\slicelets\USGuidedProcedure\sounds\critico.wav")
        sound=qt.QSound(soundFile)
        sound.play()   

      
  def updateTrackerPointsList(self):
    #clear list
    #self.fiducialsWidget.fiducialsList.clear()

    #raise this flag to ignore change events in the table, the flag is lowered at the end of this method
    self.updatingList = True

    # get the nodes
    fiducialListNode=slicer.util.getNode("Fiducials List")
    trackerListNode=slicer.util.getNode("Tracker Points List")

    # clear the list of tracker points
    trackerListNode.RemoveChildrenNodes()

    # create as many tracker nodes as fiducials
    saml = slicer.modules.annotations.logic() 
    saml.SetActiveHierarchyNodeID(trackerListNode.GetID())
    for childrenIndex in xrange(fiducialListNode.GetNumberOfChildrenNodes()):
        fidHierarchyNode=fiducialListNode.GetNthChildNode(childrenIndex)
        fidNode=fidHierarchyNode.GetAssociatedNode()        
        fidPos=[0,0,0]
        dummy=fidNode.GetFiducialCoordinates(fidPos)
        fidName = fidNode.GetName()
        fidID = fidNode.GetID()

        trackerNode=slicer.vtkMRMLAnnotationFiducialNode()
        trackerNode.SetFiducialWorldCoordinates(fidPos)
        trackerNode.SetName(fidName + '-Tracker')	
        slicer.mrmlScene.AddNode(trackerNode)

    self.updatingList = False


        