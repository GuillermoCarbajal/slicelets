from __main__ import qt, ctk
import os

from USGuidedStep import *
from Helper import *
from FiducialsList import *

class PlaceStylusTipInTheImageStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '3. PlaceStylusTipInTheImage' )
    #self.setDescription( 'Place fiducials in the image' )
  
    self.__parent = super( PlaceStylusTipInTheImageStep, self )
    

  def createUserInterface( self ):
    '''
    '''
    
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()
    

    
#    # BUTTONS --------------------------------------------------------------------
#    This is commented out and the buttons are in the UI from the designer
#
#    #layout for the buttons
#    self.buttonsLayout = qt.QHBoxLayout()
#    self.__layout.addLayout(self.buttonsLayout, 1)
#    
#    # Place fiducial
#    placeFiducialButtom = qt.QPushButton("Place fiducial")
#    placeFiducialButtom.toolTip = "Add a fiducial to the list"
#    self.buttonsLayout.addWidget(placeFiducialButtom)
#    placeFiducialButtom.connect('clicked(bool)', self.onPlaceFiducialButtomClicked) 
#    
#    # Spacer
#    self.buttonsLayout.addStretch()
    
    self.fiducialsList = FiducialsList()
    self.fiducialsList.setModuleLogic(self.logic)
    self.__layout.addWidget(self.fiducialsList.getFiducialsWidget())
    
    self.fiducialsWidget = self.fiducialsList.getFiducialsWidget()
            #customize the UI
    self.fiducialsWidget.placeSpatialButton.setVisible(False)
    self.fiducialsWidget.placeFiducialButton.setVisible(True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(2, True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(4, True)
    qt.QTimer.singleShot(0, self.killButton)
    
    print("Fiducials Widget size Hint:")
    print self.fiducialsWidget.sizeHint
    print("Fiducials Widget size :")
    print self.fiducialsWidget.size
    print("Image fiducials step size Hint:")
    print self.sizeHint
    print("Image fiducials step size")
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
    print("We are in the validate function of PlaceStylusTipInTheImageStep")

  def onEntry(self, comingFrom, transitionType):

    super(PlaceStylusTipInTheImageStep, self).onEntry(comingFrom, transitionType)
     
    self.fiducialsList.listenToListModifications()  
    
    #self.logic.crosshairEnable()
    
    self.fiducialsList.setPlaceImageFiducialStep(True)
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    if self.fiducialsWidget.fiducialsList.rowCount > 0:
        item = self.fiducialsWidget.fiducialsList.item(0, 0)
        self.fiducialsWidget.fiducialsList.itemClicked(item)
    print("We are in the onEntry function of PlaceStylusTipInTheImageStep")
    

    
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    super(PlaceStylusTipInTheImageStep, self).onExit(goingTo, transitionType) 
    #crosshairNode=slicer.util.getNode("Crosshair")
    #crosshairNode.SetCrosshairMode(1) 
    #self.logic.crosshairDisable()
    self.fiducialsList.setPlaceImageFiducialStep(False)
    self.fiducialsList.doNotListenToListModifications()
    print("We are in the onExit function of PlaceStylusTipInTheImageStep")
    
    
  def updateWidgetFromParameters(self, parameterNode):
    self.fiducialsList.updateFiducialsList("Tracker Points List")    
    print("We are in the place fiducials step")

  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()
    self.updateListNodesForRegistration()
    
    
  def updateListNodesForRegistration(self):
    
  #raise this flag to ignore change events in the table, the flag is lowered at the end of this method
    self.updatingList = True

    # get the nodes
    fiducialListNode=slicer.util.getNode("Fiducials List")
    trackerListNode=slicer.util.getNode("Tracker Points List")

    fiducialListNodeForRegistration=slicer.util.getNode("Fiducials List (for registration)")
    trackerListNodeForRegistration=slicer.util.getNode("Tracker Points List (for registration)")


    
    # clear the lists (for registration)
    fiducialListNodeForRegistration.RemoveChildrenNodes()
    trackerListNodeForRegistration.RemoveChildrenNodes()
    
    saml=slicer.modules.annotations.logic()
    
   
    for row in range(self.fiducialsWidget.fiducialsList.rowCount):
      fidID = self.fiducialsWidget.fiducialsList.item(row, 2).text()
      trackerID = self.fiducialsWidget.fiducialsList.item(row, 4).text()
      #print row
      #print fidID
      #print trackerID
      
      fidNode = slicer.mrmlScene.GetNodeByID(fidID)
      trackerNode = slicer.mrmlScene.GetNodeByID(trackerID)
      #print fidNode
      #print trackerNode
      
      #if the row is selected to be used in the registration
      if self.fiducialsWidget.fiducialsList.item(row, 0).checkState()==2:
        #print 'Checked row'
     
        fidPos=[0,0,0]
        dummy=fidNode.GetFiducialCoordinates(fidPos)
        fidName = fidNode.GetName()
        trackerPos=[0,0,0]
        dummy=trackerNode.GetFiducialCoordinates(trackerPos)
        trackerName = trackerNode.GetName()
        
        #create the new nodes copying the data 
        fidNodeForRegistration=slicer.vtkMRMLAnnotationFiducialNode()
        fidNodeForRegistration.SetFiducialWorldCoordinates(fidPos)
        fidNodeForRegistration.SetName(fidName)    
        trackerNodeForRegistration=slicer.vtkMRMLAnnotationFiducialNode()
        trackerNodeForRegistration.SetFiducialWorldCoordinates(trackerPos)
        trackerNodeForRegistration.SetName(trackerName)    
        
        # add the nodes to the lists for registration
        saml.SetActiveHierarchyNodeID(fiducialListNodeForRegistration.GetID())
        slicer.mrmlScene.AddNode(fidNodeForRegistration)
        saml.SetActiveHierarchyNodeID(trackerListNodeForRegistration.GetID())
        slicer.mrmlScene.AddNode(trackerNodeForRegistration)
     
     
    self.logic.hideAllTheFiducialsNode("Fiducials List (for registration)")
    self.logic.hideAllTheFiducialsNode("Tracker Points List (for registration)")      