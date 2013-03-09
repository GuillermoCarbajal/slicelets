from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *

class NavigationStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '5. Navigation' )
    self.setDescription( 'Navigation step' )

    self.__parent = super( NavigationStep, self )

  def createUserInterface( self ):
    '''
    '''
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()
    
    # Show the image in 3D
    showImageButton = qt.QPushButton("Show image in 3D")
    showImageButton.toolTip = "Shows the image in 3D"
    self.__layout.addWidget(showImageButton)
    showImageButton.connect('clicked(bool)', self.onShowRedSliceButtonClicked)

    # Show the image in 3D
    showStylusButton = qt.QPushButton("Show stylus in 3D")
    showStylusButton.toolTip = "Shows stylus in 3D"
    self.__layout.addWidget(showStylusButton)
    showStylusButton.connect('clicked(bool)', self.onShowStylusButtonClicked)

    # Add Ultrasound Snapshot
    snapshotButton = qt.QPushButton("US snapshot")
    snapshotButton.toolTip = "Take an ultrasound snapshot"
    self.__layout.addWidget(snapshotButton)
    snapshotButton.connect('clicked(bool)', self.onSnapshotButtonClicked)

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

    super(NavigationStep, self).onEntry(comingFrom, transitionType)
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of NavigationStep")
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
    self.logic.takeUSSnapshot()  

