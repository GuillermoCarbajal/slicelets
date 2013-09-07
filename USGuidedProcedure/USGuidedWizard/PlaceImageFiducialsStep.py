from __main__ import qt, ctk
import os

from USGuidedStep import *
from Helper import *
from FiducialsList import *

class PlaceImageFiducialsStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '2. PlaceImageFiducials' )
    #self.setDescription( 'Place fiducials in the image' )
  
    self.__parent = super( PlaceImageFiducialsStep, self )
    

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
    self.fiducialsList.setPlaceImageFiducialStep(True)
    self.fiducialsList.setModuleLogic(self.logic)
    self.__layout.addWidget(self.fiducialsList.getFiducialsWidget())
    
    self.fiducialsWidget = self.fiducialsList.getFiducialsWidget()
            #customize the UI
    self.fiducialsWidget.placeSpatialButton.setVisible(False)
    self.fiducialsWidget.placeFiducialButton.setVisible(True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(2, True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(3, True)
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
    print("We are in the validate function of PlaceImageFiducialsStep")

  def onEntry(self, comingFrom, transitionType):

    super(PlaceImageFiducialsStep, self).onEntry(comingFrom, transitionType)
    
    self.logic.createRegistrationLists()
    self.logic.createTargetList()
     
    self.fiducialsList.listenToListModifications()  
    
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of PlaceImageFiducialsStep")
    
    """  # For debugging
    import sys
    sys.path.append('C:/Users/Usuario/devel/eclipse/plugins/org.python.pydev_2.7.1.2012100913/pysrc')
    
    import pydevd 
    pydevd.settrace()
    """
    
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    
    super(PlaceImageFiducialsStep, self).onExit(goingTo, transitionType) 
    print("We are in the onExit function of PlaceImageFiducialsStep")
    
  def updateWidgetFromParameters(self, parameterNode):
    self.fiducialsList.updateFiducialsList()    
    print("We are in the place fiducials step")

  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()