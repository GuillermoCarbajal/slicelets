from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *

class ConnectToTrackerStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '1. Connect to Tracker' )
    self.setDescription( 'Connect to the tracker.' )
    
    
    self.__parent = super( ConnectToTrackerStep, self )

  def createUserInterface( self ):
    '''
    '''
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()
   
    self.PlusServerConnection = qt.QPushButton("Connect to Tracker")
    self.__layout.addWidget(self.PlusServerConnection)
    self.PlusServerConnection.connect("clicked()",self.onPlusServerConnection)

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
    print("We are in the validate function of ConnectToTrackerStep")

  def onEntry(self, comingFrom, transitionType):

    super(ConnectToTrackerStep, self).onEntry(comingFrom, transitionType)
    #self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of ConnectToTrackerStep")
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    print("We are in the onExit function of ConnectToTrackerStep")
    super(ConnectToTrackerStep, self).onExit(goingTo, transitionType) 

  def updateWidgetFromParameters(self, parameterNode):
    baselineVolumeID = parameterNode.GetParameter('baselineVolumeID')
    followupVolumeID = parameterNode.GetParameter('followupVolumeID')


  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()
    
  def onPlusServerConnection(self):
    print("Trying to connect...")
    self.logic.Connect()


