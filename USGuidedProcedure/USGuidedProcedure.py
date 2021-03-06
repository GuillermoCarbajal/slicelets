import os
import unittest
import math
from __main__ import vtk, qt, ctk, slicer
from ModelsViewer import *
from VolumesViewer import *
from VolumeRenderingViewer import *
from ToolsViewer import *
#
# USGuidedProcedure
#

import USGuidedWizard

class USGuidedProcedure:
  def __init__(self, parent):
    parent.title = "USGuidedProcedure"  # TODO make this more human readable by adding spaces
    parent.categories = ["Testing"]
    parent.dependencies = []
    parent.contributors = ["""Guillermo Carbajal and Alvaro Gomez (Facultad de Ingenieria,Udelar , Montevideo, Uruguay). 
                              Andras Lasso and Tamas Ungi (Queen's University, Kingston, Ontario, Canada)."""] 
    parent.helpText = """
    Module to test USGuidedProcedure.
    """
    parent.acknowledgementText = """
    This file was partially developed by Guillermo Carbajal, Facultad de Ingenieria (Udelar), Montevideo, Uruguay
     and was partially funded by ANII grant BE_POS_2010_2236.
    """  # replace with organization, grant and thanks.
    self.parent = parent
    
    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['USGuidedProcedure'] = self.runTest

  def runTest(self):
    tester = USGuidedProcedureTest()
    tester.runTest()

#
# qUSGuidedProcedureWidget
#

class USGuidedProcedureWidget:
  def __init__(self, parent=None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()
      
  def setup(self):
  
    self.logic = USGuidedProcedureLogic()
    # Instantiate and connect widgets ...

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "USGuidedProcedure Reload"
    self.layout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    self.layout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    # Collapsible button
    dummyCollapsibleButton = ctk.ctkCollapsibleButton()
    dummyCollapsibleButton.text = "A collapsible button"
    self.layout.addWidget(dummyCollapsibleButton)

    # Layout within the dummy collapsible button
    dummyFormLayout = qt.QFormLayout(dummyCollapsibleButton)

    # HelloWorld button
    helloWorldButton = qt.QPushButton("Hello world")
    helloWorldButton.toolTip = "Print 'Hello world' in standard ouput."
    dummyFormLayout.addWidget(helloWorldButton)
    helloWorldButton.connect('clicked(bool)', self.onHelloWorldButtonClicked)

    # Show slicelet button
    sliceletStartButton = qt.QPushButton("Show slicelet")
    sliceletStartButton.toolTip = "Start the slicelet"
    dummyFormLayout.addWidget(sliceletStartButton)
    sliceletStartButton.connect('clicked(bool)', self.onShowSliceletButtonClicked)
    
    # Connect to Tracker
    sliceletConnectToTracker = qt.QPushButton("Connect to Tracker")
    sliceletConnectToTracker.toolTip = "Connect to tracker through OpenIGTLink"
    # dummyFormLayout.addWidget(sliceletConnectToTracker)
    sliceletConnectToTracker.connect('clicked(bool)', self.onSliceletConnectToTrackerClicked)
    
    # Set up fiducials lists 
    testAnnotationsButton = qt.QPushButton("Test Fiducials lists creation")
    testAnnotationsButton.toolTip = "Test the creation of both lists of fiducials"
    # dummyFormLayout.addWidget(testAnnotationsButton)
    testAnnotationsButton.connect('clicked(bool)', self.onTestAnnotationsButtonClicked)
    # Load a fiducials lists 
    loadFiducialsListButton = qt.QPushButton("Test image points lists creation")
    loadFiducialsListButton.toolTip = "Load a fiducials list to test registration"
    # dummyFormLayout.addWidget(loadFiducialsListButton)
    loadFiducialsListButton.connect('clicked(bool)', self.onLoadFiducialListClicked)
    # Load a tracker list 
    loadTrackerListButton = qt.QPushButton("Test spatial points lists creation")
    loadTrackerListButton.toolTip = "Load spatial points to test registration"
    # dummyFormLayout.addWidget(loadTrackerListButton)
    loadTrackerListButton.connect('clicked(bool)', self.onLoadSpatialPointsListClicked)
    
    # Place fiducial
    placeFiducialButtom = qt.QPushButton("Place fiducial")
    placeFiducialButtom.toolTip = "Add a fiducial to the list"
    # dummyFormLayout.addWidget(placeFiducialButtom)
    placeFiducialButtom.connect('clicked(bool)', self.onPlaceFiducialButtomClicked)
    
    # Place Tracker Position
    placeTrackerPositionButton = qt.QPushButton("Add tracker position")
    placeTrackerPositionButton.toolTip = "Add a tracker position to the list"
    # dummyFormLayout.addWidget(placeTrackerPositionButton)
    placeTrackerPositionButton.connect('clicked(bool)', self.onPlaceTrackerPositionButtonClicked)
    
    # Perform registration
    registrationButton = qt.QPushButton("Register")
    registrationButton.toolTip = "Perform registration using the points in the list"
    # dummyFormLayout.addWidget(registrationButton)
    registrationButton.connect('clicked(bool)', self.onRegistrationButtonClicked)

    # Show the image in 3D
    showImageButton = qt.QPushButton("Show image in 3D")
    showImageButton.toolTip = "Shows the image in 3D"
    # dummyFormLayout.addWidget(showImageButton)
    showImageButton.connect('clicked(bool)', self.onShowRedSliceButtonClicked)
    
    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.helloWorldButton = helloWorldButton
    self.sliceletStartButton = sliceletStartButton
    
  def onHelloWorldButtonClicked(self):
    print "Hello World !"
    # cn=slicer.vtkMRMLIGTLConnectorNode()
    # slicer.mrmlScene.AddNode(cn)
    # cn.SetTypeClient("127.0.0.1",124)
    
  def onShowSliceletButtonClicked(self):   
    slicelet = USGuidedSliceletTestSlicelet() 
    
  def onSliceletConnectToTrackerClicked(self):
    self.logic.createAndAssociateConectorNodeWithScene()  
    self.logic.connectWithTracker()
    
  def onPlaceFiducialButtomClicked(self):   
    self.logic.addFiducialToList("Fiducials List")
    
  def onPlaceTrackerPositionButtonClicked(self):   
    self.logic.recordTrackerPosition()   
  
  def onTestAnnotationsButtonClicked(self):  
    self.logic.createRegistrationLists()  
    
  def onLoadFiducialListClicked(self):  
    self.logic.addFiducialsToImageList() 
    
  def onLoadSpatialPointsListClicked(self):  
    self.logic.addFiducialsToTrackerList() 
    
  def onRegistrationButtonClicked(self):
    self.logic.register()
    
  def onShowRedSliceButtonClicked(self):
    self.logic.showRedSliceIn3D()
    
  def onReload(self, moduleName="USGuidedProcedure"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0, p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)
    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()

  def onReloadAndTest(self, moduleName="USGuidedProcedure"):
    self.onReload()
    evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
    tester = eval(evalString)
    tester.runTest()

#
# USGuidedProcedureLogic
#

class USGuidedProcedureLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    # self.createRegistrationLists()
    self.connectorNode = None 
    self.USImageName = "Image_Reference"
    self.numberOfUltrasoundSnapshotsTaken = 0
    self.scalarRange = [0., 255.]
    self.windowLevelMinMax = [20, 30]
    pass

  def hasImageData(self, volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  
  def createAndAssociateConectorNodeWithScene(self):
    cn = slicer.util.getNode('Plus Server Connection')  
    if cn == None:
       cn = slicer.vtkMRMLIGTLConnectorNode()
       slicer.mrmlScene.AddNode(cn)
       cn.SetName('Plus Server Connection')
       print("IGTL Connector node was created!")
    self.connectorNode = cn
       
  def connectWithTracker(self):
    self.connectorNode.SetTypeClient("localhost", 18944)
    print("Status before start(): " + str(self.connectorNode.GetState()))
    self.startTracking()
    print("Connected with Plus Server in Slicelet Class ")
    print("Status after start(): " + str(self.connectorNode.GetState()))  
      
    # self.associateTransformations()  
    
  def associateTransformations(self):
      
    referenceToRASNode = slicer.util.getNode("ReferenceToRAS")
    if referenceToRASNode == None:
      referenceToRASNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(referenceToRASNode)
      referenceToRASNode.SetName("ReferenceToRAS")  
    
    # # The nodes StylusTipToReference and ProbeToReference are added 
    stylusTipToReferenceNode = slicer.util.getNode("StylusTipToReference")
    if stylusTipToReferenceNode == None:
      stylusTipToReferenceNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(stylusTipToReferenceNode)
      stylusTipToReferenceNode.SetName("StylusTipToReference")
    
    probeToReferenceNode = slicer.util.getNode("ProbeToReference")
    if probeToReferenceNode == None:
      probeToReferenceNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(probeToReferenceNode)
      probeToReferenceNode.SetName("ProbeToReference")
      
    referenceToTrackerNode = slicer.util.getNode("ReferenceToTracker")
    if referenceToTrackerNode == None:
      referenceToTrackerNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(referenceToTrackerNode)
      referenceToTrackerNode.SetName("ReferenceToTracker")  
      
    imageToReferenceNode = slicer.util.getNode("ImageToReference")
    if imageToReferenceNode == None:
      imageToReferenceNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(imageToReferenceNode)
      imageToReferenceNode.SetName("ImageToReference")  
    
    imageReferenceNode = slicer.util.getNode("Image_Reference")
    if imageReferenceNode == None:
      imageReferenceNode = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(imageReferenceNode)
      imageReferenceNode.SetName("Image_Reference")  
      
        
    # referenceToRASNode=slicer.util.getNode("ReferenceToRAS")           
         
    # imageReferenceNode=slicer.util.getNode("Image_Reference")
    imageReferenceNode.SetAndObserveTransformNodeID(referenceToRASNode.GetID())
    
    # imageToReferenceNode=slicer.util.getNode("ImageToReference")
    imageToReferenceNode.SetAndObserveTransformNodeID(referenceToRASNode.GetID())
    
    # probeToReferenceNode=slicer.util.getNode("ProbeToReference")
    probeToReferenceNode.SetAndObserveTransformNodeID(referenceToRASNode.GetID())   
    
    # # Associate the stylus to reference transform with the reference to RAS
    stylusTipToReferenceNode.SetAndObserveTransformNodeID(referenceToRASNode.GetID())     
     
    self.stylusModelNode = slicer.util.getNode("Stylus_Example")    
    if self.stylusModelNode == None:    
        # Add the stylus model
        modelsModule = slicer.modules.models
        modelsModuleLogic = modelsModule.logic()
        modelsModuleLogic.SetMRMLScene(slicer.mrmlScene)
        path = slicer.modules.usguidedprocedure.path
        modulePath = os.path.dirname(path)
        stylusModelFile = os.path.join(modulePath, "models/Stylus_Example.stl")
        modelsModuleLogic.AddModel(stylusModelFile)
        self.stylusModelNode = slicer.util.getNode("Stylus_Example")
    
    self.stylusModelNode.RemoveAllNodeReferenceIDs("transform")
  
    # # Associate the model of the stylus with the stylus tip transforms
    stylusTipModelToStylusTipTransform = slicer.util.getNode("StylusTipModelToStylusTip")
    if stylusTipModelToStylusTipTransform == None:
        stylusTipModelToStylusTipTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(stylusTipModelToStylusTipTransform) 
        stylusTipModelToStylusTipTransform.SetName("StylusTipModelToStylusTip") 
        
    matrix = vtk.vtkMatrix4x4()
    matrix.SetElement(0, 3, -210)
    stylusTipModelToStylusTipTransform.SetAndObserveMatrixTransformToParent(matrix)
    stylusTipModelToStylusTipTransform.SetAndObserveTransformNodeID(stylusTipToReferenceNode.GetID())
    
    self.stylusModelNode.SetAndObserveTransformNodeID(stylusTipModelToStylusTipTransform.GetID())
    

    
    
    
   
    
    
        
        
  def getStylusModel(self):
      return self.stylusModelNode
        
  def startTracking(self):
      self.connectorNode.Start()
      
  def stopTracking(self):
    self.connectorNode.Stop()  
    
  def getConnectorNode(self): 
      return self.connectorNode
       
  def getConnectionStatus(self):
      return self.connectionStatus
    
  def addFiducialToList(self, listName):
    print("Place fiducial pressed")
    saml = slicer.modules.annotations.logic() 
    listNode = slicer.util.getNode(listName)
    if listNode is not None:
      saml.SetActiveHierarchyNodeID(listNode.GetID())
      snode = slicer.vtkMRMLSelectionNode.SafeDownCast(slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton"))
      inode = slicer.vtkMRMLInteractionNode.SafeDownCast(slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton"))
      snode.SetReferenceActivePlaceNodeClassName("vtkMRMLAnnotationFiducialNode")
      inode.SwitchToSinglePlaceMode()
    else:
      print listName + "list does not exit!" 
      
  def setActiveAnnotationsList(self, listName):
      saml = slicer.modules.annotations.logic()   
      listNode = slicer.util.getNode("All Annotations")   
      if listNode is not None:
        saml.SetActiveHierarchyNodeID(listNode.GetID())
  
  def createRegistrationLists(self): 
      saml = slicer.modules.annotations.logic()
      # saml.RegisterNodes() 
      parentNode = saml.GetActiveHierarchyNode()
      # parentNode = slicer.util.getNode("All Annotations")
      # Create the Fiducials List
      self.createAnnotationList("Fiducials List", parentNode)
      # Create the Tracker Points List
      self.createAnnotationList("Tracker Points List", parentNode)
      # Create the Fiducials List used for Registration
      self.createAnnotationList("Fiducials List (for registration)", parentNode)
      # Create the Tracker Points List used for Registration
      self.createAnnotationList("Tracker Points List (for registration)", parentNode)
      
  def createTargetList(self): 
      # The target list is created in the same level that the registration list   
      # saml=slicer.modules.annotations.logic()
      # saml.RegisterNodes() 
      
      # activeNode=saml.GetActiveHierarchyNode()
      parentNode = slicer.util.getNode("All Annotations")
      # parentNode=saml.GetActiveHierarchyNode()
      self.createAnnotationList("Target List", parentNode)
      
  def createPlusCommandsList(self): 
      # The target list is created in the same level that the registration list   
      # saml=slicer.modules.annotations.logic()
      # saml.RegisterNodes() 
      
      # activeNode=saml.GetActiveHierarchyNode()
      parentNode = slicer.util.getNode("All Annotations")
      # parentNode=saml.GetActiveHierarchyNode()
      self.createAnnotationList("Plus Commands List", parentNode)    
      
  def createAnnotationList(self, listName, parentNode):
     # check if we already have the annotation list
    if  slicer.mrmlScene.GetNodesByName(listName).GetNumberOfItems() > 0:
        return
    
    saml = slicer.modules.annotations.logic()
    # Set the parent node as the active node
    saml.SetActiveHierarchyNodeID(parentNode.GetID())
    # A new Annotation node id added to the scene.
    # When a Annotation node is added, this  recently created node turns into the active node 
    saml.AddHierarchy()
    createdNode = saml.GetActiveHierarchyNode()
    createdNode.SetName(listName) 
    
    
  def printFids(self):
    fiducialListNode = slicer.util.getNode("Fiducials List")
    for childrenIndex in xrange(fiducialListNode.GetNumberOfChildrenNodes()):
      fidHierarchyNode = fiducialListNode.GetNthChildNode(childrenIndex)
      fidNode = fidHierarchyNode.GetAssociatedNode()
      fidPos = [0, 0, 0]
      dummy = fidNode.GetFiducialCoordinates(fidPos)
      print fidPos[0], ",", fidPos[1], ",", fidPos[2]
      
  def addFiducialsToImageList(self):
    saml = slicer.modules.annotations.logic() 
    fnode = slicer.util.getNode("Fiducials List")
    saml.SetActiveHierarchyNodeID(fnode.GetID())
    f1 = slicer.vtkMRMLAnnotationFiducialNode()
    f1.SetFiducialWorldCoordinates((0, 0, 5))
    f1.SetName('Fiducial 1')	
    slicer.mrmlScene.AddNode(f1)
    f2 = slicer.vtkMRMLAnnotationFiducialNode()
    f2.SetFiducialWorldCoordinates((0, 10, 5))
    f2.SetName('Fiducial 2')	
    slicer.mrmlScene.AddNode(f2)
    f3 = slicer.vtkMRMLAnnotationFiducialNode()
    f3.SetFiducialWorldCoordinates((10, 10, 5))
    f3.SetName('Fiducial 3')	
    slicer.mrmlScene.AddNode(f3)
    f4 = slicer.vtkMRMLAnnotationFiducialNode()
    f4.SetFiducialWorldCoordinates((10, 10, 15))
    f4.SetName('Fiducial 4')	
    slicer.mrmlScene.AddNode(f4)
    print("Fiducials added to Image List")
    
  def addFiducialsToTrackerList(self):
    saml = slicer.modules.annotations.logic() 
    fnode = slicer.util.getNode("Tracker Points List")
    saml.SetActiveHierarchyNodeID(fnode.GetID())
    f1 = slicer.vtkMRMLAnnotationFiducialNode()
    f1.SetFiducialWorldCoordinates((10, 0, 5))
    f1.SetName('Stylus Tip 1')	
    slicer.mrmlScene.AddNode(f1)
    f2 = slicer.vtkMRMLAnnotationFiducialNode()
    f2.SetFiducialWorldCoordinates((10, 10, 5))
    f2.SetName('Stylus Tip 2')	
    slicer.mrmlScene.AddNode(f2)
    f3 = slicer.vtkMRMLAnnotationFiducialNode()
    f3.SetFiducialWorldCoordinates((20, 10, 5))
    f3.SetName('Stylus Tip 3')	
    slicer.mrmlScene.AddNode(f3)
    f4 = slicer.vtkMRMLAnnotationFiducialNode()
    f4.SetFiducialWorldCoordinates((20, 10, 15))
    f4.SetName('Stylus Tip 4')	
    slicer.mrmlScene.AddNode(f4)
    print("Fiducials added to Tracker List")
    
  def register(self):
    print("registration started")  
    fidPointsNode = slicer.util.getNode("Fiducials List (for registration)")
    spaPointsNode = slicer.util.getNode("Tracker Points List (for registration)")
    # referenceToRASNode=slicer.vtkMRMLLinearTransformNode()
    # referenceToRASNode.SetName("ReferenceToRAS")
    # slicer.mrmlScene.AddNode(referenceToRASNode)
    referenceToRASNode = slicer.util.getNode("ReferenceToRAS")
    parameters = {}
    parameters["fixedLandmarks"] = fidPointsNode.GetID()
    parameters["movingLandmarks"] = spaPointsNode.GetID()
    parameters["saveTransform"] = referenceToRASNode.GetID()
    parameters["transformType"] = "Rigid"
    fr = slicer.modules.fiducialregistration
    frLogic = fr.cliModuleLogic()
    node = frLogic.CreateNode()
    print node.GetParameterName(0, 0)
    print node.GetParameterName(0, 1)
    print node.GetParameterName(0, 2)
    print node.GetParameterName(0, 3)
    slicer.cli.run(fr, None, parameters)
    
 
  def getFiducialNode(self, listName, index):
    listNode = slicer.util.getNode(listName)
    if listNode:
      listNodeCount = listNode.GetNumberOfChildrenNodes()
    else:
      return None
      
    if index >= 0 and index < listNodeCount:
      hierarchyNode = listNode.GetNthChildNode(index)
      node = hierarchyNode.GetAssociatedNode()
    elif index < 0 and abs(index) <= listNodeCount:
      hierarchyNode = listNode.GetNthChildNode(listNodeCount + index)
      node = hierarchyNode.GetAssociatedNode()
    else:
      node = None
      
    return node
  
    
  def showRedSliceIn3D(self, isShown):  
    image_RAS = slicer.util.getNode("Image_Reference")  
    redNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    vrd = slicer.modules.volumereslicedriver
    vrdl = vrd.logic()
    vrdl.SetMRMLScene(slicer.mrmlScene)
    vrdl.SetDriverForSlice(image_RAS.GetID(), redNode)
    vrdl.SetModeForSlice(vrdl.MODE_TRANSVERSE180, redNode)
      
    # Set the background volume 
    redWidgetCompNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceCompositeNodeRed")
    redWidgetCompNode.SetBackgroundVolumeID(image_RAS.GetID())
    # Show the volume in 3D
    redNode.SetSliceVisible(isShown)
    # Adjust the size of the US image in the Axial view
    sliceLogic = slicer.vtkMRMLSliceLogic()
    sliceLogic.SetName("Red")
    sliceLogic.SetMRMLScene(slicer.mrmlScene)
    # sliceLogic.FitSliceToAll()
    greenNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    yellowNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    greenNode.SetSliceVisible(False)
    yellowNode.SetSliceVisible(False)
    
    
  def resliceVolumeWithDriver(self,node):
    image_RAS = slicer.util.getNode("Image_Reference") 
    vrd = slicer.modules.volumereslicedriver
    vrdl = vrd.logic()
    vrdl.SetMRMLScene(slicer.mrmlScene)
    
    
    greenNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    vrdl.SetDriverForSlice(image_RAS.GetID(), greenNode)
    vrdl.SetModeForSlice(vrdl.MODE_TRANSVERSE180, greenNode)   
    # Set the background volume 
    greenWidgetCompNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceCompositeNodeGreen")
    greenWidgetCompNode.SetBackgroundVolumeID(node.GetID()) 
    
  def disconnectDriverForSlice(self):
    redNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    vrd = slicer.modules.volumereslicedriver
    vrdl = vrd.logic()
    vrdl.SetMRMLScene(slicer.mrmlScene)
    vrdl.SetDriverForSlice("None", redNode)    
    
  def showReconstructedVolume(self, name):  
    recvol_Reference = slicer.util.getNode(name) 
    
    redNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    redNode.SetSliceVisible(True)  
    redWidgetCompNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceCompositeNodeRed")
    redWidgetCompNode.SetBackgroundVolumeID(recvol_Reference.GetID())
    redNode.SetOrientation("Axial")
    sliceLogicRed = slicer.vtkMRMLSliceLogic()
    sliceLogicRed.SetName("Red")
    sliceLogicRed.SetMRMLScene(slicer.mrmlScene)
    sliceLogicRed.FitSliceToAll()
    
    greenNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeGreen")
    greenNode.SetSliceVisible(True)  
    greenWidgetCompNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceCompositeNodeGreen")
    greenWidgetCompNode.SetBackgroundVolumeID(recvol_Reference.GetID())
    greenNode.SetOrientation("Coronal")
    sliceLogicGreen = slicer.vtkMRMLSliceLogic()
    sliceLogicGreen.SetName("Green")
    sliceLogicGreen.SetMRMLScene(slicer.mrmlScene)
    sliceLogicGreen.FitSliceToAll()
    
    yellowNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeYellow")
    yellowNode.SetSliceVisible(True)  
    yellowWidgetCompNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceCompositeNodeYellow")
    yellowWidgetCompNode.SetBackgroundVolumeID(recvol_Reference.GetID())
    yellowNode.SetOrientation("Sagittal")
    sliceLogicYellow = slicer.vtkMRMLSliceLogic()
    sliceLogicYellow.SetName("Yellow")
    sliceLogicYellow.SetMRMLScene(slicer.mrmlScene)
    sliceLogicYellow.FitSliceToAll()
    
  def showStylusTipToRAS(self):
    stylusTipToRAS = slicer.util.getNode("StylusTipToRAS")
    igt = slicer.modules.openigtlinkif
    igtl = igt.logic()
    igtl.GetConverterByMRMLTag(stylusTipToRAS.GetNodeTagName())
    converter = igtl.GetConverterByMRMLTag(stylusTipToRAS.GetNodeTagName())
    converter.SetVisibility(1, slicer.mrmlScene, stylusTipToRAS)

  def takeUSSnapshot(self):
    image_RAS = slicer.util.getNode(self.USImageName)
    usn = slicer.modules.ultrasoundsnapshots
    usnl = usn.logic()
    usnl.AddSnapshot(image_RAS)
    
  def takeUSSnapshot2(self):
    snapshotDisp = slicer.vtkMRMLModelDisplayNode()
    slicer.mrmlScene.AddNode(snapshotDisp)
    snapshotDisp.SetScene(slicer.mrmlScene)
    snapshotDisp.SetDisableModifiedEvent(1)
    snapshotDisp.SetOpacity(1.0)
    snapshotDisp.SetColor(1.0, 1.0, 1.0)
    snapshotDisp.SetAmbient(1.0)
    snapshotDisp.SetBackfaceCulling(0)
    snapshotDisp.SetDiffuse(0)
    snapshotDisp.SetSaveWithScene(0)
    snapshotDisp.SetDisableModifiedEvent(0)
    name = "Snapshot" + str(self.numberOfUltrasoundSnapshotsTaken)  
    self.numberOfUltrasoundSnapshotsTaken = self.numberOfUltrasoundSnapshotsTaken + 1
    
    snapshotModel = slicer.vtkMRMLModelNode()
    snapshotModel.SetName(name)
    snapshotModel.SetDescription("Live Ultrasound Snapshot")
    snapshotModel.SetScene(slicer.mrmlScene)
    snapshotModel.SetAndObserveDisplayNodeID(snapshotDisp.GetID())
    snapshotModel.SetHideFromEditors(0)
    snapshotModel.SetSaveWithScene(0)
    slicer.mrmlScene.AddNode(snapshotModel)
    
    image_RAS = slicer.util.getNode("Image_Reference")
    
    dim = [0, 0, 0]
    imageData = image_RAS.GetImageData()
    imageData.GetDimensions(dim)
    
    plane = vtk.vtkPlaneSource()
    plane.Update()
    snapshotModel.SetAndObservePolyData(plane.GetOutput())
    
    slicePolyData = snapshotModel.GetPolyData()
    slicePoints = slicePolyData.GetPoints()
    
    # In parent transform is saved the ReferenceToRAS transform
    parentTransform = vtk.vtkTransform()
    parentTransform.Identity()
    if not image_RAS.GetParentTransformNode() == None:
      parentMatrix = vtk.vtkMatrix4x4()
      parentTransformNode = image_RAS.GetParentTransformNode()
      parentTransformNode.GetMatrixTransformToWorld(parentMatrix)
      # aux=parentTransform.GetMatrix()
      # aux.DeepCopy(parentMatrix)
      # parentTransform.Update()
      parentTransform.SetMatrix(parentMatrix)
      
    inImageTransform = vtk.vtkTransform()
    inImageTransform.Identity()
    image_RAS.GetIJKToRASMatrix(inImageTransform.GetMatrix())
    
    tImageToRAS = vtk.vtkTransform()
    tImageToRAS.Identity()
    tImageToRAS.PostMultiply()
    tImageToRAS.Concatenate(inImageTransform)
    tImageToRAS.Concatenate(parentTransform)
   
    tImageToRAS.Update()
    
    point1Image = [0.0, 0.0, 0.0, 1.0]
    point2Image = [dim[0], 0.0, 0.0, 1.0]
    point3Image = [0.0, dim[1], 0.0, 1.0]
    point4Image = [dim[0], dim[1], 0.0, 1.0]
    
    point1RAS = [0.0, 0.0, 0.0, 0.0]
    point2RAS = [0.0, 0.0, 0.0, 0.0]
    point3RAS = [0.0, 0.0, 0.0, 0.0]
    point4RAS = [0.0, 0.0, 0.0, 0.0]
    tImageToRAS.MultiplyPoint(point1Image, point1RAS)
    tImageToRAS.MultiplyPoint(point2Image, point2RAS)
    tImageToRAS.MultiplyPoint(point3Image, point3RAS)
    tImageToRAS.MultiplyPoint(point4Image, point4RAS)  
    
    p1RAS = [point1RAS[0], point1RAS[1], point1RAS[2]]
    p2RAS = [point2RAS[0], point2RAS[1], point2RAS[2]]
    p3RAS = [point3RAS[0], point3RAS[1], point3RAS[2]]
    p4RAS = [point4RAS[0], point4RAS[1], point4RAS[2]]
    slicePoints.SetPoint(0, p1RAS)
    slicePoints.SetPoint(1, p2RAS)
    slicePoints.SetPoint(2, p3RAS)
    slicePoints.SetPoint(3, p4RAS)
    # # Add image texture.
    image = vtk.vtkImageData()
    image.DeepCopy(imageData)
    modelDisplayNode = snapshotModel.GetModelDisplayNode()
    modelDisplayNode.SetAndObserveTextureImageData(image)
    
    
  def recordTrackerPosition(self):
    saml = slicer.modules.annotations.logic() 
    fnode = slicer.util.getNode("Tracker Points List")
    saml.SetActiveHierarchyNodeID(fnode.GetID())  
    StylusTipToReferenceNode = slicer.util.getNode("StylusTipToReference")
    validTransformation = self.isValidTransformation("StylusTipToReference") and self.isValidTransformation("ReferenceToTracker")
    
    if validTransformation == True: 
      cfl = slicer.modules.collectfiducials.logic()
      cfl.SetProbeTransformNode(StylusTipToReferenceNode)
      cfl.AddFiducial()
      print("Tracker position recorded")   
        
    else:
      print("Tracker position is invalid")  
    return validTransformation

    
  def startAcquisition(self, igtlRemoteLogic, igtlConnectorNode, OutputFilename):
    self.commandId=igtlRemoteLogic.SendCommand('<Command Name="StartRecording" OutputFilename="' + OutputFilename + '" CaptureDeviceId="CaptureDevice"></Command>', igtlConnectorNode.GetID())
    return self.commandId
 
    
  def stopAcquisition(self, igtlRemoteLogic, igtlConnectorNode): 
    self.commandId=igtlRemoteLogic.SendCommand('<Command Name="StopRecording"  CaptureDeviceId="CaptureDevice"></Command>', igtlConnectorNode.GetID())
    return self.commandId    
        
  def reconstructVolume(self, igtlRemoteLogic, igtlConnectorNode, PreAcquisitionFilename, OutputVolFilename, OutputVolDeviceName):
    self.commandId=igtlRemoteLogic.SendCommand('<Command Name="ReconstructVolume" InputSeqFilename="' + PreAcquisitionFilename + '" OutputVolFilename="' + OutputVolFilename + '" OutputVolDeviceName="' + OutputVolDeviceName + '"></Command>', igtlConnectorNode.GetID())       
    return self.commandId   
  
  def startVolumeReconstruction(self, igtlRemoteLogic, igtlConnectorNode, OutputVolFilename, OutputVolDeviceName):
    self.commandId = igtlRemoteLogic.SendCommand('<Command Name="StartVolumeReconstruction" OutputVolFilename="' + OutputVolFilename + '" OutputVolDeviceName="' + OutputVolDeviceName + '" ChannelId="TrackedVideoStream"></Command>', igtlConnectorNode.GetID()) 
    return self.commandId   

  def suspendVolumeReconstruction(self, igtlRemoteLogic, igtlConnectorNode): 
    self.commandId=igtlRemoteLogic.SendCommand('<Command Name="SuspendVolumeReconstruction"></Command>', igtlConnectorNode.GetID())  
    return self.commandId   
    
  def resumeVolumeReconstruction(self, igtlRemoteLogic, igtlConnectorNode): 
    self.commandId=igtlRemoteLogic.SendCommand('<Command Name="ResumeVolumeReconstruction"></Command>', igtlConnectorNode.GetID())   
    return self.commandId   
    
  def stopVolumeReconstruction(self, igtlRemoteLogic, igtlConnectorNode): 
    igtlRemoteLogic.SendCommand('<Command Name="StopVolumeReconstruction" ReferencedCommandId="' + str(self.commandId) + '"></Command>', igtlConnectorNode.GetID())   
    return self.commandId   
    
  def getVolumeReconstructionSnapshot(self, igtlRemoteLogic, igtlConnectorNode): 
    self.commandId=igtlRemoteLogic.SendCommand('<Command Name="GetVolumeReconstructionSnapshot"></Command>', igtlConnectorNode.GetID())           
    return self.commandId   
         

  def listenToVolumesAdded(self):
    vl = slicer.modules.volumes
    vl = vl.logic()  
    self.sceneObserver = vl.AddObserver('ModifiedEvent', self.onVolumeAdded)
    
  def isAnUltrasoundVolumeGeneratedWithPLUS(self, volumeNode):
    name = volumeNode.GetName()
    nameArray = name.split("_")
    returnValue = False
    if nameArray.count("Reference") > 0:
      returnValue = True
    return returnValue  
    
  def onVolumeAdded(self, volumeNode):     
    
    if self.isAnUltrasoundVolumeGeneratedWithPLUS(volumeNode) == True:
      print("A volume generated with PLUS was added!!")
      #volumeNode.AddObserver("ModifiedEvent", self.onVolumeModified)      
    
      '''
      It is assumed that the volume was created with respect to the Reference
      The matrix associated with the volume must have the following structure
      sx 0  0  ox
      0  sy 0  oy
      0  0  sz oz
      with sx, sy, and sz >0
      This is checked and if it is not true is modified.
      By default Slicer add a volume with a ijkToRas matrix of the form:
      -1    0    0
       0    -1    0
       0     0    1
      In this case we want a ijkToRAS matrix equal to identity because we want to place the
      volume with respect to the Reference.
      ReferenceToRAS matrix is calculated during registration
      '''
    
      matrix = vtk.vtkMatrix4x4()
      volumeNode.GetIJKToRASMatrix(matrix) 
      #print matrix
      sx = matrix.GetElement(0, 0)
      if (sx < 0):
        ox = matrix.GetElement(0, 3)
        matrix.SetElement(0, 0, -sx)
        matrix.SetElement(0, 3, -ox)
      sy = matrix.GetElement(1, 1)
      if (sy < 0):
        oy = matrix.GetElement(1, 3)
        matrix.SetElement(1, 1, -sy)
        matrix.SetElement(1, 3, -oy)    
      volumeNode.SetIJKToRASMatrix(matrix)
      #print matrix
    
      # Volumes are placed under the Reference coordinate system
      referenceToRASNode = slicer.util.getNode("ReferenceToRAS")
      if referenceToRASNode == None:
        referenceToRASNode = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(referenceToRASNode)
        referenceToRASNode.SetName("ReferenceToRAS")
    
      volumeNode.SetAndObserveTransformNodeID(referenceToRASNode.GetID()) 
      volumeNode.SetDisplayVisibility(True)
      
      colorTransfer= self.createColorTransfer()
      volumePropertyNode=self.createVolumePropertyNode(colorTransfer)
      self.createVolumeRendering(volumeNode, volumePropertyNode)
    
  
  def createColorTransfer(self):
    # the color function is configured
    # zero is associated to the scalar zero and 1 to the scalar 255
    colorTransfer = vtk.vtkColorTransferFunction()
    black = [0., 0., 1.]
    white = [1., 0., 0.]
    colorTransfer.AddRGBPoint(self.scalarRange[0], black[0], black[1], black[2])
    colorTransfer.AddRGBPoint(self.windowLevelMinMax[0], black[0], black[1], black[2])
    colorTransfer.AddRGBPoint(self.windowLevelMinMax[1], white[0], white[1], white[2]);
    colorTransfer.AddRGBPoint(self.scalarRange[1], white[0], white[1], white[2]);
    return colorTransfer
  
  def createVolumePropertyNode(self, colorTransfer):
    volumePropertyNode = slicer.vtkMRMLVolumePropertyNode()
    slicer.mrmlScene.RegisterNodeClass(volumePropertyNode);

    # the scalar opacity mapping function is configured
    # it is a ramp with opacity of 0 equal to zero and opacity of 1 equal to 1. 
    scalarOpacity = vtk.vtkPiecewiseFunction()
    scalarOpacity.AddPoint(self.scalarRange[0], 0.)
    scalarOpacity.AddPoint(self.windowLevelMinMax[0], 0.)
    scalarOpacity.AddPoint(self.windowLevelMinMax[1], 1.)
    scalarOpacity.AddPoint(self.scalarRange[1], 1.)
    volumePropertyNode.SetScalarOpacity(scalarOpacity);
    
    vtkVolumeProperty = volumePropertyNode.GetVolumeProperty()
    
    vtkVolumeProperty.SetInterpolationTypeToNearest();
    vtkVolumeProperty.ShadeOn();
    vtkVolumeProperty.SetAmbient(0.30);
    vtkVolumeProperty.SetDiffuse(0.60);
    vtkVolumeProperty.SetSpecular(0.50);
    vtkVolumeProperty.SetSpecularPower(40);
    
    volumePropertyNode.SetColor(colorTransfer)
   
    slicer.mrmlScene.AddNode(volumePropertyNode)
    
    return volumePropertyNode
  
  
  def createVolumeRendering(self, volumeNode, volumePropertyNode):    
    # The volume rendering display node is created
    vr = slicer.modules.volumerendering
    vrLogic = vr.logic()
    defaultRenderingMethod = vrLogic.GetDefaultRenderingMethod()
    print defaultRenderingMethod
    if defaultRenderingMethod == 'vtkMRMLGPURayCastVolumeRenderingDisplayNode':
      self.vrDisplayNode = slicer.vtkMRMLGPURayCastVolumeRenderingDisplayNode()
      self.vrDisplayNode.SetName(volumeNode.GetName()+"Rendering")
    elif defaultRenderingMethod == 'vtkMRMLCPURayCastVolumeRenderingDisplayNode':
      self.vrDisplayNode = slicer.vtkMRMLCPURayCastVolumeRenderingDisplayNode()
      self.vrDisplayNode.SetName(volumeNode.GetName()+"Rendering")  
      
    self.vrDisplayNode.SetAndObserveVolumeNodeID(volumeNode.GetID())
    #self.vrDisplayNode.SetFollowVolumeDisplayNode(True)
    self.vrDisplayNode.SetAndObserveVolumePropertyNodeID(volumePropertyNode.GetID())
    
    slicer.mrmlScene.AddNode(self.vrDisplayNode)
    self.vrDisplayNode.SetVisibility(False)
    #self.vrDisplayNode.AddObserver("ModifiedEvent", self.onVolumeRenderingModified)  
    
    #vrLogic.Modified()
    #self.vrDisplayNode.Modified()
    self.vrDisplayNode.UpdateScene(slicer.mrmlScene)                 
                        
                                  
  def showVolumeRendering(self, isShown):
    self.vrDisplayNode.SetVisibility(isShown)  
                                           
  def onVolumeModified(self, caller, event):
    print "Volume Modified"
  
  def onVolumeRenderingModified(self, caller, event):
    print "Volume Rendering Modified"      
  
  def isValidTransformation(self, transformationNodeName):
 
      transformationNode = slicer.util.getNode(transformationNodeName)
      # transformation=vtk.vtkMatrix4x4()
      # transformationNode.GetMatrixTransformToWorld(transformation)
      transformation = transformationNode.GetMatrixTransformToParent()
      # print "Transformation is: "  
      # print transformation 
      
      validTransformation = True
      a00 = transformation.GetElement(0, 0)     
      a01 = transformation.GetElement(0, 1) 
      a02 = transformation.GetElement(0, 2) 
      a03 = transformation.GetElement(0, 3)
      
      a10 = transformation.GetElement(1, 0)     
      a11 = transformation.GetElement(1, 1) 
      a12 = transformation.GetElement(1, 2) 
      a13 = transformation.GetElement(1, 3) 
      
      a20 = transformation.GetElement(2, 0)     
      a21 = transformation.GetElement(2, 1) 
      a22 = transformation.GetElement(2, 2) 
      a23 = transformation.GetElement(2, 3)    
      
      a30 = transformation.GetElement(3, 0)     
      a31 = transformation.GetElement(3, 1) 
      a32 = transformation.GetElement(3, 2) 
      a33 = transformation.GetElement(3, 3)   
      
      if(a00 == 1 and a01 == 0 and a02 == 0 and a03 == 0 and 
         a10 == 0 and a11 == 1 and a12 == 0 and a13 == 0 and
         a20 == 0 and a21 == 0 and a22 == 1 and a32 == 0 and
         a30 == 0 and a31 == 0 and a23 == 0 and a33 == 1):
         validTransformation = False   
      
      # print "Transformation is valid:" + str(validTransformation)  
      return validTransformation
                 
                         
  def onResetView(self):
      print "View should be reset!"  
      # lm=slicer.app.layoutManager()
      # renderer=lm.activeThreeDRenderer()  
      camera1 = slicer.mrmlScene.GetNodeByID("vtkMRMLCameraNode1")
      if not camera1 == None:
         # camera1.Reset(True,True,True,renderer)  
         glCamera1 = camera1.GetCamera()
         glCamera1.SetFocalPoint(0, 0, 0)
         glCamera1.SetPosition(-500, 0, 0)   
         glCamera1.SetViewAngle(30)
         glCamera1.SetViewUp(0, 0, 1)
      camera2 = slicer.mrmlScene.GetNodeByID("vtkMRMLCameraNode2")
      if not camera2 == None:
         # camera2.Reset(True,True,True,renderer)  
         glCamera2 = camera2.GetCamera()
         glCamera2.SetFocalPoint(0, 0, 0)
         glCamera2.SetPosition(0, 500, 0)   
         glCamera2.SetViewAngle(30)   
         glCamera2.SetViewUp(0, 0, 1)       
         
         
  def startPlusServer(self):
    self.PlusExecutable = "C:/Users/Usuario/devel/PlusExperimentalBin/bin/Debug/PlusServer.exe"
    self.ConfigFile = "D:/data/USGuidedProcedure/recordedData/BluePhantom_LAxis_PlusServerTrunk_config.xml"
    command = self.PlusExecutable
    command += " --config-file=" + self.ConfigFile
    command += " --running-time=12345"
    command += " --verbose=3"
    from subprocess import Popen
    p = Popen(command)     
    
  def crosshairDisable(self):   
      crosshairNode = slicer.util.getNode("Crosshair")
      crosshairNode.NavigationOff()
      crosshairNode.SetCrosshairMode(0)
      
  def crosshairEnable(self):   
      crosshairNode = slicer.util.getNode("Crosshair")
      crosshairNode.NavigationOff() 
      crosshairNode.SetCrosshairMode(1) 
        
           
class USGuidedProcedureTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def delayDisplay(self, message, msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message, self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_USGuidedProcedure1()

  def test_USGuidedProcedure1(self):
    """ Testing USGuidedProcedure
    """

    self.delayDisplay("Starting the test")
  

  
  
  
  
  
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

#
# qSlicerPythonModuleExampleWidget
#

class USGuidedSliceletTestWidget:
  def __init__(self, parent=None):
    self.chartOptions = ("Count", "Volume mm^3", "Volume cc", "Min", "Max", "Mean", "StdDev")
    if not parent:
      print("There is no parent!")
    else:
      self.parent = parent
      print("There is parent!")



      

class Slicelet(object):
  """A slicer slicelet is a module widget that comes up in stand alone mode
  implemented as a python class.
  This class provides common wrapper functionality used by all slicer modlets.
  """
  # TODO: put this in a SliceletLib 
  # TODO: parse command line arge


  def __init__(self, widgetClass=None):
    self.parent = qt.QFrame()
    self.parent.setLayout(qt.QHBoxLayout())
    
    self.moduleLogic = USGuidedProcedureLogic()
    

    # TODO: should have way to pop up python interactor
    self.leftFrame = qt.QFrame(self.parent)
    self.leftFrame.setLayout(qt.QVBoxLayout())
    # self.leftFrame.setSizePolicy(qt.QSizePolicy.Maximum,qt.QSizePolicy.Maximum)
    # self.leftFrame.setSizePolicy(qt.QSizePolicy.MinimumExpanding,qt.QSizePolicy.MinimumExpanding)
    
    # self.parent.setStyleSheet(
    # "QFrame{background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #ccf); background-color: qlineargradient(spread:pad, x1:0.989, y1:0.012, x2:0, y2:0, stop:0 rgba(223, 227, 255, 255), stop:0.494318 rgba(164, 157, 194, 255), stop:1 rgba(115, 115, 115, 255));}"
    # "QComboBox{color: white; background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88d, stop: 0.1 #99e, stop: 0.49 #77c, stop: 0.5 #66b, stop: 1 #77c); border-width: 1px; border-color: #339; border-style: solid; border-radius: 7; padding: 3px; font-size: 12px; font-weight: bold; padding-left: 5px; padding-right: 5px; /*min-width: 50px;*/ max-width: 150px; /*min-height: 13px;*/ max-height: 150px; }"     "QPushButton{color: white; background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88d, stop: 0.1 #99e, stop: 0.49 #77c, stop: 0.5 #66b, stop: 1 #77c); border-width: 1px; border-color: #339; border-style: solid; border-radius: 7; padding: 3px;  font-size: 12px; font-weight: bold; padding-left: 5px; padding-right: 5px; min-width: 20px; max-width: 150px; min-height: 20px; max-height: 40px;}"
    # "QLabel{color: white; background-color: rgba(255, 255, 255, 0);}"
    #    "QSlider::groove:horizontal{border: 1px solid #bbb;background: white;height: 10px;border-radius: 4px;}" 
    #    "QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,    stop: 0 #66e, stop: 1 #bbf);background:qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,    stop: 0 #bbf, stop: 1 #55f);border: 1px solid #777;height: 10px;border-radius:4px;}"
    #    "QSlider::add-page:horizontal {background: #fff;border: 1px solid #777;height: 10px;border-radius: 4px;}"
    #    "QSlider::handle:horizontal {background: qlineargradient(x1:0, y1:0, x2:1, y2:1,    stop:0 #eee, stop:1 #ccc);border: 1px solid #777;width: 13px;margin-top: -2px;margin-bottom: -2px;border-radius: 4px;}"
    #    "QSlider::handle:horizontal:hover {background: qlineargradient(x1:0, y1:0, x2:1, y2:1,    stop:0 #fff, stop:1 #ddd);border: 1px solid#444;border-radius: 4px;}"
    #    "QSlider::sub-page:horizontal:disabled {background: #bbb;border-color: #999;}"
    #    "QSlider::add-page:horizontal:disabled {background: #eee;border-color: #999;}"
    #    "QSlider::handle:horizontal:disabled {background: #eee;border: 1px solid #aaa;border-radius: 4px;}")
    
    self.parent.layout().addWidget(self.leftFrame, 1)
    
    
    # self.addDataButton = qt.QPushButton("Add Data")
    # self.leftFrame.layout().addWidget(self.addDataButton)
    # self.addDataButton.connect("clicked()",slicer.app.ioManager().openAddDataDialog)
    
    self.saveSceneButton = qt.QPushButton("Save Data")
    self.leftFrame.layout().addWidget(self.saveSceneButton)
    self.saveSceneButton.connect("clicked()", slicer.app.ioManager().openSaveDataDialog)
    # self.loadSceneButton = qt.QPushButton("Load Scene")
    # self.leftFrame.layout().addWidget(self.loadSceneButton)
    # self.loadSceneButton.connect("clicked()",slicer.app.ioManager().openLoadSceneDialog)
    
    
    self.layoutSelectorFrame2 = qt.QFrame(self.parent)
    self.layoutSelectorFrame2.setLayout(qt.QHBoxLayout())
    self.leftFrame.layout().addWidget(self.layoutSelectorFrame2)

    self.layoutSelectorLabel2 = qt.QLabel("Layout Selector: ", self.layoutSelectorFrame2)
    self.layoutSelectorLabel2.setToolTip("Select the layout ...")
    self.layoutSelectorFrame2.layout().addWidget(self.layoutSelectorLabel2)

    self.layoutSelector2 = qt.QComboBox(self.layoutSelectorFrame2)
    self.layoutSelector2.addItem("FourViews")
    self.layoutSelector2.addItem("3D View")
    self.layoutSelector2.addItem("One view")
    self.layoutSelector2.addItem("Double 3D View")
    self.layoutSelectorFrame2.layout().addWidget(self.layoutSelector2)
    self.layoutSelector2.connect('activated(int)', self.onLayoutSelect)
    
    self.resetViewButton = qt.QPushButton("Reset")
    self.layoutSelectorFrame2.layout().addWidget(self.resetViewButton)
    self.resetViewButton.connect('clicked()', self.moduleLogic.onResetView)
    
    self.layoutWidget = slicer.qMRMLLayoutWidget()
    self.layoutWidget.setMRMLScene(slicer.mrmlScene)
    
    # self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    # self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)   
    # self.layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutTabbedSliceView)
    #### Some of the possible layouts
    # SlicerLayout3DPlusLightboxView SlicerLayoutCompareGridView SlicerLayoutCompareWidescreenView SlicerLayoutConventionalQuantitativeView SlicerLayoutConventionalView SlicerLayoutConventionalWidescreenView
    # SlicerLayoutCustomView SlicerLayoutDefaultView SlicerLayoutOneUp3DView SlicerLayoutOneUpRedSliceView SlicerLayoutOneUpGreenSliceView SlicerLayoutOneUpYellowSliceView SlicerLayoutDual3DView 
    # SlicerLayoutFourOverFourView SlicerLayoutTabbedSliceView 
    self.layoutWidget.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)
    
    self.parent.layout().addWidget(self.layoutWidget, 2)
    
    
    print("Previous line of the Constructor of ModelsViewer")
    self.modelsViewer = ModelsViewer()
    self.modelsViewer.setModuleLogic(self.moduleLogic)
    self.modelsViewer.listenToScene()
    self.volumesViewer = VolumesViewer()
    self.volumesViewer.setModuleLogic(self.moduleLogic)
    self.volumesViewer.listenToScene()
    self.volumeRenderingViewer = VolumeRenderingViewer()
    self.volumeRenderingViewer.setModuleLogic(self.moduleLogic)
    self.volumeRenderingViewer.listenToScene()
    self.toolsViewer = ToolsViewer()
    self.toolsViewer.setModuleLogic(self.moduleLogic)
    # self.toolsViewer.listenToScene()
    
    
    # item=qt.QListWidgetItem("unItem")
    # self.modelsViewer.addItem(item)
    
    self.leftFrame.layout().addWidget(self.modelsViewer.getModelsViewerWidget(), 1)
    self.leftFrame.layout().addWidget(self.volumesViewer.getVolumesViewerWidget(), 1)
    self.leftFrame.layout().addWidget(self.volumeRenderingViewer.getVolumeRenderingViewerWidget(), 1)
    self.leftFrame.layout().addWidget(self.toolsViewer.getToolsWidget(), 1)
    '''
    Create and start the USGuided workflow.
    '''
    self.workflow = ctk.ctkWorkflow()

    self.workflowWidget = ctk.ctkWorkflowStackedWidget()
    self.workflowWidget.setWorkflow(self.workflow)
    
    bw = self.workflowWidget.buttonBoxWidget()
    bw.hideInvalidButtons = True
    
    
    groupBox = self.workflowWidget.workflowGroupBox()
    groupBox.errorTextEnabled = False

    #bw.nextButtonDefaultText = ""
    #bw.backButtonDefaultText = ""
    
    nextButton=bw.nextButton()
    backButton=bw.backButton()
    nextButton.text=""
    backButton.text=""
  
    self.leftFrame.layout().addWidget(self.workflowWidget, 8)
    

    # create all wizard steps
    self.loadSceneStep = USGuidedWizard.LoadSceneStep('LoadScene')
    self.loadSceneStep.setModuleLogic(self.moduleLogic)
    self.loadSceneStep.setButtonBoxWidget(bw)
    self.connectToTrackerStep = USGuidedWizard.ConnectToTrackerStep('ConnectToTracker')
    self.connectToTrackerStep.setModuleLogic(self.moduleLogic)
    self.connectToTrackerStep.setButtonBoxWidget(bw)
    self.connectToTrackerStep.setToolsViewer(self.toolsViewer)
    self.placeImageFiducialsStep = USGuidedWizard.PlaceImageFiducialsStep('PlaceImageFiducials')
    self.placeImageFiducialsStep.setModuleLogic(self.moduleLogic)
    self.placeImageFiducialsStep.setButtonBoxWidget(bw)
    self.placeSpatialFiducialsStep = USGuidedWizard.PlaceSpatialFiducialsStep('PlaceSpatialFiducials')
    self.placeSpatialFiducialsStep.setModuleLogic(self.moduleLogic)
    self.placeSpatialFiducialsStep.setButtonBoxWidget(bw)
    self.registrationStep = USGuidedWizard.RegistrationStep('Registration')
    self.registrationStep.setModuleLogic(self.moduleLogic)
    self.registrationStep.setButtonBoxWidget(bw)
    self.navigationStep = USGuidedWizard.NavigationStep('Navigation')
    self.navigationStep.setModuleLogic(self.moduleLogic)
    self.navigationStep.setButtonBoxWidget(bw)
    # self.selectScansStep = USGuidedWizard.ChangeTrackerSelectScansStep( 'SelectScans'  )
    # self.defineROIStep = USGuidedWizard.ChangeTrackerDefineROIStep( 'DefineROI'  )
    # self.segmentROIStep = USGuidedWizard.ChangeTrackerSegmentROIStep( 'SegmentROI'  )
    # self.analyzeROIStep = USGuidedWizard.ChangeTrackerAnalyzeROIStep( 'AnalyzeROI'  )
    # self.reportROIStep = USGuidedWizard.ChangeTrackerReportROIStep( 'ReportROI'  )
    

    # add the wizard steps to an array for convenience
    allSteps = []

    allSteps.append(self.loadSceneStep)
    allSteps.append(self.placeImageFiducialsStep)
    allSteps.append(self.connectToTrackerStep)
    allSteps.append(self.placeSpatialFiducialsStep)
    allSteps.append(self.registrationStep)
    allSteps.append(self.navigationStep)
    # allSteps.append( self.selectScansStep )
    # allSteps.append( self.defineROIStep )
    # allSteps.append( self.segmentROIStep )
    # allSteps.append( self.analyzeROIStep )
    # allSteps.append( self.reportROIStep )

    # Add transition for the first step which let's the user choose between simple and advanced mode
    self.workflow.addTransition(self.loadSceneStep, self.placeImageFiducialsStep)
    self.workflow.addTransition(self.placeImageFiducialsStep, self.connectToTrackerStep)
    self.workflow.addTransition(self.connectToTrackerStep, self.placeSpatialFiducialsStep)
    self.workflow.addTransition(self.placeSpatialFiducialsStep, self.registrationStep)
    self.workflow.addTransition(self.registrationStep, self.navigationStep)
    # self.workflow.addTransition( self.placeImageFiducials, self.selectScansStep )  
    # self.workflow.addTransition( self.selectScansStep, self.defineROIStep )
    # self.workflow.addTransition( self.defineROIStep, self.segmentROIStep )
    # self.workflow.addTransition( self.segmentROIStep, self.analyzeROIStep )
    # self.workflow.addTransition( self.analyzeROIStep, self.reportROIStep )

    nNodes = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLScriptedModuleNode')

    self.parameterNode = None
    for n in xrange(nNodes):
      compNode = slicer.mrmlScene.GetNthNodeByClass(n, 'vtkMRMLScriptedModuleNode')
      nodeid = None
      if compNode.GetModuleName() == 'USGuidedProcedure':
        self.parameterNode = compNode
        print 'Found existing USGuidedProcedure parameter node'
        break
    if self.parameterNode == None:
      self.parameterNode = slicer.vtkMRMLScriptedModuleNode()
      self.parameterNode.SetModuleName('USGuidedProcedure')
      slicer.mrmlScene.AddNode(self.parameterNode)
 
    for s in allSteps:
        s.setParameterNode (self.parameterNode)

    # restore workflow step
    currentStep = self.parameterNode.GetParameter('currentStep')
    if currentStep != '':
      print 'Restoring workflow step to ', currentStep
      if currentStep == 'LoadScene':
        self.workflow.setInitialStep(self.loadSceneStep)
      if currentStep == 'ConnectToTracker':
        self.workflow.setInitialStep(self.connectToTrackerStep)
      if currentStep == 'PlaceImageFiducials':
        self.workflow.setInitialStep(self.placeImageFiducialsStep)
      if currentStep == 'PlaceSpatialFiducials':
        self.workflow.setInitialStep(self.placeSpatialFiducialsStep)
      if currentStep == 'Registration':
        self.workflow.setInitialStep(self.registrationStep)
      if currentStep == 'Navigation':
        self.workflow.setInitialStep(self.navigationStep)
      # if currentStep == 'SelectScans':
      #  self.workflow.setInitialStep(self.selectScansStep)
      # if currentStep == 'DefineROI':
      #  self.workflow.setInitialStep(self.defineROIStep)
      # if currentStep == 'SegmentROI':
      #  self.workflow.setInitialStep(self.segmentROIStep)
      # if currentStep == 'AnalyzeROI':
      #  self.workflow.setInitialStep(self.analyzeROIStep)
      # if currentStep == 'ReportROI':
      #  self.workflow.setInitialStep(self.reportROIStep)
    else:
      print 'currentStep in parameter node is empty!'
        
    # start the workflow and show the widget
    self.workflow.start()
    self.workflowWidget.visible = True
    
    if widgetClass:
      self.widget = widgetClass(self.parent)
    self.parent.show()
    
    # self.moduleLogic = slicer.modules.USGuidedProcedure.logic()
    
  def onPlusServerConnection(self):
    print("Trying to connect...")
    self.moduleLogic.Connect()
    
  def onLayoutSelect(self, argin): 
    print("Layout changed") 
    print(argin)
    if argin == 0:
       self.layoutWidget.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalView)  
    elif argin == 1:  
       self.layoutWidget.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    elif argin == 2:
       self.layoutWidget.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutTabbedSliceView)
    elif argin == 3:
       self.layoutWidget.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutDual3DView)
   
      
 
 
class USGuidedSliceletTestSlicelet(Slicelet):
  """ Creates the interface when module is run as a stand alone gui app.
  """

  def __init__(self):
    super(USGuidedSliceletTestSlicelet, self).__init__(USGuidedSliceletTestWidget)


if __name__ == "__main__":
  # TODO: need a way to access and parse command line arguments
  # TODO: ideally command line args should handle --xml

  import sys
  print(sys.argv)

  slicelet = USGuidedSliceletTestSlicelet() 
  
