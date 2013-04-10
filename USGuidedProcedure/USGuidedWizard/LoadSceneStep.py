from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *

class LoadSceneStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '0. Load a scene' )
    self.setDescription( 'Load a previously saved scene...' )    
    self.__parent = super( LoadSceneStep, self )
    
  def createUserInterface( self ):
    '''
    '''
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()
    
    # Status of the connection
    self.statusFrame = qt.QFrame()
    self.statusFrame.setLayout( qt.QHBoxLayout() )
    

    # Button to connect
    self.loadSceneButton = qt.QPushButton("Load a scene")
    
    # Add to the widget
    self.__layout.addWidget(self.loadSceneButton)
    
    # Connections
    self.loadSceneButton.connect("clicked()",self.onLoadSceneButtonClicked)

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
    print("We are in the validate function of LoadSceneStep")
           

  def onEntry(self, comingFrom, transitionType):

    super(LoadSceneStep, self).onEntry(comingFrom, transitionType)
    #self.updateWidgetFromParameters(self.parameterNode())
        
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of LoadSceneStep")
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    print("We are in the onExit function of LoadSceneStep")
    super(LoadSceneStep, self).onExit(goingTo, transitionType) 

  def updateWidgetFromParameters(self, parameterNode):
    return


  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()
    
  def onLoadSceneButtonClicked(self):
    self.loadSceneButton.connect("clicked()",slicer.app.ioManager().openLoadSceneDialog)