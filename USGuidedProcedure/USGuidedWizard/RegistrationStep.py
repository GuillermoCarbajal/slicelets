from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *

class RegistrationStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '4. Registration' )
    self.setDescription( 'Registration step' )

    self.__parent = super( RegistrationStep, self )

  def createUserInterface( self ):
    '''
    '''
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()
       
    # Perform registration
    registrationButton = qt.QPushButton("Register")
    registrationButton.toolTip = "Perform registration using the points in the list"
    self.__layout.addWidget(registrationButton)
    registrationButton.connect('clicked(bool)', self.onRegistrationButtonClicked)

    
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
    print("We are in the validate function of RegistrationStep")

  def onEntry(self, comingFrom, transitionType):

    super(RegistrationStep, self).onEntry(comingFrom, transitionType)
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of RegistrationStep")
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    

    super(RegistrationStep, self).onExit(goingTo, transitionType) 
    print("We are in the onExit function of RegistrationStep")
  def updateWidgetFromParameters(self, parameterNode):
    print("We are in the place fiducials step")


  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()

  def onRegistrationButtonClicked(self):
    self.logic.register()
