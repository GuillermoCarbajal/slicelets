from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *

class ConnectToTrackerStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '1. Connect to Tracker' )
    #self.setDescription( 'Connect to the tracker...' )    
    self.__parent = super( ConnectToTrackerStep, self )
    
    self.estado = "Disconnected"
    self.connectorCreated=False
    #self.PlusServerBin = "C:\Users\Usuario\devel\PlusExperimentalBin\bin\Debug"
    #self.ConfigFile = "D:\data\USGuidedProcedure\recordedData\BluePhantom_LAxis_PlusServerTrunk_config.xml"
    #import subprocess
    #params=[r"C:\Users\Usuario\devel\PlusExperimentalBin\bin\Debug/PlusServer.exe",]
    #print subprocess.list2cmdline(r"C:")
    #print subprocess.list2cmdline(r"pause")
    
    #from subprocess import Popen
    #p = Popen("runPlusServerOpenIGTLinkRemote.bat", cwd=r"D:\data\USGuidedProcedure\recordedData")
    #stdout, stderr = p.communicate()

    #cimport os
    #os.startfile("D:/data/USGuidedProcedure/recordedData/runPlusServerOpenIGTLinkRemote.bat")
    #os.system("C:")
    #os.system("cd "+self.PlusServerBin)
    #os.system("PlusServer.exe --config-file="+self.ConfigFile+" --running-time=12345 --verbose=3")
    
  def createUserInterface( self ):
    '''
    '''
    # TODO: might make sense to hide the button for the last step at this
    # point, but the widget does not have such option
    self.__layout = self.__parent.createUserInterface()
    # Status of the connection
    self.statusFrame = qt.QFrame()
    self.statusFrame.setLayout( qt.QHBoxLayout() )
    
    self.statusLabel = qt.QLabel("Status: ")
    self.statusLabel.setToolTip( "Status of the connection ...")
    
    self.statusBar = qt.QStatusBar()
    self.statusBar.showMessage("Disconnected")

    # Button to connect
    self.PlusServerConnection = qt.QPushButton("Connect to Tracker")
    # Add to the widget
    self.statusFrame.layout().addWidget(self.statusLabel)
    self.statusFrame.layout().addWidget(self.statusBar)
    
    self.__layout.addWidget(self.statusFrame)
    self.__layout.addWidget(self.PlusServerConnection)
    
    # Connections
    self.PlusServerConnection.connect("clicked()",self.onPlusServerConnection)

    self.updateWidgetFromParameters(self.parameterNode())

    self.ConnectedState=False
    self.DisconnectedState=False

    qt.QTimer.singleShot(0, self.killButton)

  def killButton(self):
    # hide useless button
    bl = slicer.util.findChildren(text='ReportROI')
    if len(bl):
      bl[0].hide()


  def validate( self, desiredBranchId ):
    '''
    '''
      
    print("We are in the validate function of ConnectToTrackerStep")
          
    if self.estado == "Connected":
       self.__parent.validationSucceeded(desiredBranchId)
    else:
       self.__parent.validationFailed(desiredBranchId, 'Error','Please connect to the tracker before continuing')  

  def onEntry(self, comingFrom, transitionType):

    super(ConnectToTrackerStep, self).onEntry(comingFrom, transitionType)
    #self.updateWidgetFromParameters(self.parameterNode())
    if not self.connectorCreated:
        self.logic.createAndAssociateConectorNodeWithScene()
        self.connectorNode = self.logic.getConnectorNode()
        self.connectorNode.AddObserver(self.connectorNode.ConnectedEvent,self.onConnectedEventCaptured)
        self.connectorNode.AddObserver(self.connectorNode.DisconnectedEvent,self.onDisconnectedEventCaptured)
        self.connectorCreated = True    
    
    status = self.connectorNode.GetState()
      #print("Status: " + str(status))
    if status==2:
        self.estado = "Connected"
        self.PlusServerConnection.setText("Disconnect")
    elif status==1:
        self.estado = "Waiting"
    elif status==0:
        self.estado=="Disconnected"
        self.PlusServerConnection.setText("Connect")
    
    self.statusBar.showMessage(self.estado)#print(self.estado)
          
              
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of ConnectToTrackerStep")
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    self.logic.associateTransformations()   
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
    if self.estado=="Disconnected":
       print("Trying to connect...")
       print("Status before Connect(): " + str(self.connectorNode.GetState()))
       self.logic.connectWithTracker()
       self.estado = "Waiting"
       self.statusBar.showMessage(self.estado)
       print("Status After Connect(): " + str(self.connectorNode.GetState()))
    elif (self.estado=="Connected") or (self.estado=="Waiting"):
       self.logic.stopTracking() 
 
  def onConnectedEventCaptured(self, caller,  event):
      #print("Connected event captured!")
      status = self.connectorNode.GetState()
      #print("Status: " + str(status))
      if status==2:
          self.estado = "Connected"
          self.PlusServerConnection.setText("Disconnect")
          self.statusBar.showMessage(self.estado)#print(self.estado)
          self.ConnectedState=True
      else:
          self.ConnectedState=False
          
      if((not self.ConnectedState) and (not self.DisconnectedState)):
          self.estado = "Waiting"
          self.statusBar.showMessage(self.estado)   
          
      
  def onDisconnectedEventCaptured(self, caller,  event):
      #print("Disconnected event captured!")
      status = self.connectorNode.GetState()
      if status==0:
          self.estado = "Disconnected"
          self.statusBar.showMessage(self.estado)
          self.PlusServerConnection.setText("Connect to Tracker")  
          self.DisconnectedState=True
      else:
          self.DisconnectedState=False
          