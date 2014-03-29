import os
import unittest
import math
from __main__ import vtk, qt, ctk, slicer

from ToolsViewer import *
#
# StylusBasedUSProbeCalibration
#

import StylusBasedUSProbeCalibrationWizard

class StylusBasedUSProbeCalibration:
  def __init__(self, parent):
    parent.title = "StylusBasedUSProbeCalibration"  # TODO make this more human readable by adding spaces
    parent.categories = ["Testing"]
    parent.dependencies = []
    parent.contributors = ["""Guillermo Carbajal and Alvaro Gomez (Facultad de Ingenieria,Udelar , Montevideo, Uruguay). 
                              Andras Lasso and Tamas Ungi (Queen's University, Kingston, Ontario, Canada)."""] 
    parent.helpText = """
    Module to test StylusBasedUSProbeCalibration.
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
    slicer.selfTests['StylusBasedUSProbeCalibration'] = self.runTest

  def runTest(self):
    tester = StylusBasedUSProbeCalibrationTest()
    tester.runTest()

#
# qStylusBasedUSProbeCalibrationWidget
#

class StylusBasedUSProbeCalibrationWidget:
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
  
    self.logic = StylusBasedUSProbeCalibrationLogic()
    # Instantiate and connect widgets ...

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "StylusBasedUSProbeCalibration Reload"
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

    # Add vertical spacer
    self.layout.addStretch(1)


    
  def onHelloWorldButtonClicked(self):
    print "Hello World !"
    # cn=slicer.vtkMRMLIGTLConnectorNode()
    # slicer.mrmlScene.AddNode(cn)
    # cn.SetTypeClient("127.0.0.1",124)
    
  def onShowSliceletButtonClicked(self):   
    slicelet = StylusBasedUSProbeCalibrationSliceletTestSlicelet() 
    
  def onSliceletConnectToTrackerClicked(self):
    self.logic.createAndAssociateConectorNodeWithScene()  
    self.logic.connectWithTracker()

  def onShowRedSliceButtonClicked(self):
    self.logic.showRedSliceIn3D()
    
  def onReload(self, moduleName="StylusBasedUSProbeCalibration"):
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

  def onReloadAndTest(self, moduleName="StylusBasedUSProbeCalibration"):
    self.onReload()
    evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
    tester = eval(evalString)
    tester.runTest()

#
# StylusBasedUSProbeCalibrationLogic
#

class StylusBasedUSProbeCalibrationLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    # self.createRegistrationLists()
    self.connectorNode = None 
    vrd = slicer.modules.volumereslicedriver
    self.vrdl = vrd.logic()
    self.vrdl.SetMRMLScene(slicer.mrmlScene)
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

    # # The nodes StylusTipToReference and ProbeToReference are added 
    stylusTipToReferenceNode = slicer.util.getNode("StylusTipToTracker")
    if stylusTipToReferenceNode == None:
      stylusTipToReferenceNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(stylusTipToReferenceNode)
      stylusTipToReferenceNode.SetName("StylusTipToTracker")
    
    probeToReferenceNode = slicer.util.getNode("ProbeToTracker")
    if probeToReferenceNode == None:
      probeToReferenceNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(probeToReferenceNode)
      probeToReferenceNode.SetName("ProbeToTracker")
      
    stylusTipToProbeNode = slicer.util.getNode("StylusTipToProbe")
    if stylusTipToProbeNode == None:
      stylusTipToProbeNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(stylusTipToProbeNode)
      stylusTipToProbeNode.SetName("StylusTipToProbe")  
      
    imageToProbeNode = slicer.util.getNode("ImageToProbe")
    if imageToProbeNode == None:
      imageToProbeNode = slicer.vtkMRMLLinearTransformNode()
      slicer.mrmlScene.AddNode(imageToProbeNode)
      stylusTipToProbeNode.SetName("ImageToProbe")   
      
    #imageNode = slicer.util.getNode("Image_Image")          
      
        
    # referenceToRASNode=slicer.util.getNode("ReferenceToRAS")           
         
    # imageReferenceNode=slicer.util.getNode("Image_Reference")
    #imageNode.SetAndObserveTransformNodeID(imageToProbeNode.GetID()) 
    stylusTipToProbeNode.SetAndObserveTransformNodeID(probeToReferenceNode.GetID())   
     
    self.stylusModelNode = slicer.util.getNode("Stylus_Example")    
    if self.stylusModelNode == None:    
        # Add the stylus model
        modelsModule = slicer.modules.models
        modelsModuleLogic = modelsModule.logic()
        modelsModuleLogic.SetMRMLScene(slicer.mrmlScene)
        path = slicer.modules.stylusbasedusprobecalibration.path
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
      listNode = slicer.util.getNode(listName)   
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
    
    
  def hideAllTheFiducialsNode(self,listName):
    listNode = slicer.util.getNode(listName)
    for childrenIndex in xrange(listNode.GetNumberOfChildrenNodes()):              
      fidHierarchyNode=listNode.GetNthChildNode(childrenIndex)
      fidNode=fidHierarchyNode.GetAssociatedNode()   
      fidNode.SetDisplayVisibility(False)   
    
  def printFids(self):
    fiducialListNode = slicer.util.getNode("Fiducials List")
    for childrenIndex in xrange(fiducialListNode.GetNumberOfChildrenNodes()):
      fidHierarchyNode = fiducialListNode.GetNthChildNode(childrenIndex)
      fidNode = fidHierarchyNode.GetAssociatedNode()
      fidPos = [0, 0, 0]
      dummy = fidNode.GetFiducialCoordinates(fidPos)
      print fidPos[0], ",", fidPos[1], ",", fidPos[2]
      
    
  def register(self):
    print("registration started")  
    fidPointsNode = slicer.util.getNode("Fiducials List (for registration)")
    spaPointsNode = slicer.util.getNode("Tracker Points List (for registration)")
    # referenceToRASNode=slicer.vtkMRMLLinearTransformNode()
    # referenceToRASNode.SetName("ReferenceToRAS")
    # slicer.mrmlScene.AddNode(referenceToRASNode)
    referenceToRASNode = slicer.util.getNode("ImageToProbe")
    parameters = {}
    parameters["fixedLandmarks"] = fidPointsNode.GetID()
    parameters["movingLandmarks"] = spaPointsNode.GetID()
    parameters["saveTransform"] = referenceToRASNode.GetID()
    parameters["transformType"] = "Similarity"
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
 
  def getVolumeResliceDriverLogic(self):
    return self.vrdl 
    
  def showRedSliceIn3D(self, isShown):  
    image_RAS = slicer.util.getNode("Image_Image")  
    redNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    self.vrdl.SetDriverForSlice(image_RAS.GetID(), redNode)
    self.vrdl.SetModeForSlice(self.vrdl.MODE_TRANSVERSE180, redNode)
      
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
    
  def listenToImageSentToTheScene(self):
    self.sceneObserver = slicer.mrmlScene.AddObserver('ModifiedEvent', self.onImageSentToTheScene)
    

  def doNotListenToImageSentToTheScene(self):
    slicer.mrmlScene.RemoveObserver(self.sceneObserver)

  def onImageSentToTheScene(self, caller, event):
    image_Reference = slicer.util.getNode("Image_Image")   
    if image_Reference is not None: 
      self.doNotListenToImageSentToTheScene()
      self.showRedSliceIn3D(True)      

    
  def disconnectDriverForSlice(self):
    redNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    vrd = slicer.modules.volumereslicedriver
    vrdl = vrd.logic()
    vrdl.SetMRMLScene(slicer.mrmlScene)
    vrdl.SetDriverForSlice("None", redNode)    
    
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
    
  def takeUSSnapshot2(self,name):
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
    
    snapshotModel = slicer.vtkMRMLModelNode()
    snapshotModel.SetName(name)
    snapshotModel.SetDescription("Live Ultrasound Snapshot")
    snapshotModel.SetScene(slicer.mrmlScene)
    snapshotModel.SetAndObserveDisplayNodeID(snapshotDisp.GetID())
    snapshotModel.SetHideFromEditors(0)
    snapshotModel.SetSaveWithScene(0)
    slicer.mrmlScene.AddNode(snapshotModel)
    
    image_RAS = slicer.util.getNode("Image_Image")
    
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
    
    snapshotTexture = slicer.vtkMRMLScalarVolumeNode()
    snapshotTexture.SetAndObserveImageData(image)
    snapshotTexture.SetName(name + "_Texture")
    slicer.mrmlScene.AddNode(snapshotTexture)
    snapshotTexture.CopyOrientation( image_RAS )
    
    snapshotTextureDisplayNode = slicer.vtkMRMLScalarVolumeDisplayNode()
    snapshotTextureDisplayNode.SetName(name + "_TextureDisplay")
    snapshotTextureDisplayNode.SetAutoWindowLevel(0);
    snapshotTextureDisplayNode.SetWindow(256);
    snapshotTextureDisplayNode.SetLevel(128);
    snapshotTextureDisplayNode.SetDefaultColorMap();
    slicer.mrmlScene.AddNode(snapshotTextureDisplayNode)
    
    snapshotTexture.AddAndObserveDisplayNodeID( snapshotTextureDisplayNode.GetID() )
    
    snapshotModel.SetAttribute( "TextureNodeID", snapshotTexture.GetID() )
    snapshotModelDisplayNode= snapshotModel.GetModelDisplayNode()
    snapshotModelDisplayNode.SetAndObserveTextureImageData( snapshotTexture.GetImageData() )
    
    
  def captureSpatialsPositions(self,fidName ):
    saml = slicer.modules.annotations.logic() 
    listNode = slicer.util.getNode("Tracker Points List")
    saml.SetActiveHierarchyNodeID(listNode.GetID())  
    StylusTipToReferenceNode = slicer.util.getNode("StylusTipToProbe")
    validTransformation = self.isValidTransformation("StylusTipToProbe") 
    
    if validTransformation == True: 
      #cfl = slicer.modules.collectfiducials.logic()
      #cfl.SetProbeTransformNode(StylusTipToReferenceNode)
      #cfl.AddFiducial()
      transformation = StylusTipToReferenceNode.GetMatrixTransformToParent()
      fidPos=[transformation.GetElement(0,3),transformation.GetElement(1,3),transformation.GetElement(2,3)]
      trackerNode=slicer.vtkMRMLAnnotationFiducialNode()
      trackerNode.SetFiducialWorldCoordinates(fidPos)
      trackerNode.SetName(fidName + '-Tracker')    
      self.setActiveAnnotationsList("Tracker Points List")
      slicer.mrmlScene.AddNode(trackerNode)
      self.setActiveAnnotationsList("Fiducials List")
      fidPos=[0,0,0]
      fidNode=slicer.vtkMRMLAnnotationFiducialNode()
      fidNode.SetFiducialWorldCoordinates(fidPos)
      fidNode.SetName(fidName + '-Tracker')   
      self.takeUSSnapshot2(fidName + '-Snapshot')
      print("Tracker position recorded")   
    else:
      print("Tracker position is invalid")  
    return validTransformation

  
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
         
           
class StylusBasedUSProbeCalibrationTest(unittest.TestCase):
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
    self.test_StylusBasedUSProbeCalibration1()

  def test_StylusBasedUSProbeCalibration1(self):
    """ Testing StylusBasedUSProbeCalibration
    """

    self.delayDisplay("Starting the test")
  

  
  
  
  
  
  
  
  
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

#
# qSlicerPythonModuleExampleWidget
#

class StylusBasedUSProbeCalibrationSliceletTestWidget:
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
    
    self.moduleLogic = StylusBasedUSProbeCalibrationLogic()
    

    # TODO: should have way to pop up python interactor
    self.leftFrame = qt.QFrame(self.parent)
    self.leftFrame.setLayout(qt.QVBoxLayout())
    
    
    self.parent.layout().addWidget(self.leftFrame, 1)
    
    
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
    

    self.toolsViewer = ToolsViewer()
    self.toolsViewer.setModuleLogic(self.moduleLogic)
    # self.toolsViewer.listenToScene()
    
    
    # item=qt.QListWidgetItem("unItem")
    # self.modelsViewer.addItem(item)
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
    self.connectToTrackerStep = StylusBasedUSProbeCalibrationWizard.ConnectToTrackerStep('ConnectToTracker')
    self.connectToTrackerStep.setModuleLogic(self.moduleLogic)
    self.connectToTrackerStep.setButtonBoxWidget(bw)
    self.connectToTrackerStep.setToolsViewer(self.toolsViewer)
    self.placeStylusTipInTheImageStep = StylusBasedUSProbeCalibrationWizard.PlaceStylusTipInTheImageStep('PlaceStylusTipInTheImage')
    self.placeStylusTipInTheImageStep.setModuleLogic(self.moduleLogic)
    self.placeStylusTipInTheImageStep.setButtonBoxWidget(bw)
    self.captureSpatialPositionsStep = StylusBasedUSProbeCalibrationWizard.CaptureSpatialPositionsStep('CaptureSpatialPositions')
    self.captureSpatialPositionsStep.setModuleLogic(self.moduleLogic)
    self.captureSpatialPositionsStep.setButtonBoxWidget(bw)
    self.registrationStep = StylusBasedUSProbeCalibrationWizard.RegistrationStep('Registration')
    self.registrationStep.setModuleLogic(self.moduleLogic)
    self.registrationStep.setButtonBoxWidget(bw)


    # add the wizard steps to an array for convenience
    allSteps = []



    allSteps.append(self.connectToTrackerStep)
    allSteps.append(self.captureSpatialPositionsStep)
    allSteps.append(self.placeStylusTipInTheImageStep)
    allSteps.append(self.registrationStep)

    # Add transition for the first step which let's the user choose between simple and advanced mode
    self.workflow.addTransition(self.connectToTrackerStep, self.captureSpatialPositionsStep)
    self.workflow.addTransition(self.captureSpatialPositionsStep, self.placeStylusTipInTheImageStep)
    self.workflow.addTransition(self.placeStylusTipInTheImageStep, self.registrationStep)
 
    nNodes = slicer.mrmlScene.GetNumberOfNodesByClass('vtkMRMLScriptedModuleNode')

    self.parameterNode = None
    for n in xrange(nNodes):
      compNode = slicer.mrmlScene.GetNthNodeByClass(n, 'vtkMRMLScriptedModuleNode')
      nodeid = None
      if compNode.GetModuleName() == 'StylusBasedUSProbeCalibration':
        self.parameterNode = compNode
        print 'Found existing StylusBasedUSProbeCalibration parameter node'
        break
    if self.parameterNode == None:
      self.parameterNode = slicer.vtkMRMLScriptedModuleNode()
      self.parameterNode.SetModuleName('StylusBasedUSProbeCalibration')
      slicer.mrmlScene.AddNode(self.parameterNode)
 
    for s in allSteps:
        s.setParameterNode (self.parameterNode)

    # restore workflow step
    currentStep = self.parameterNode.GetParameter('currentStep')
    if currentStep != '':
      print 'Restoring workflow step to ', currentStep
      if currentStep == 'ConnectToTracker':
        self.workflow.setInitialStep(self.connectToTrackerStep)
      if currentStep == 'PlaceStylusInTheImage':
        self.workflow.setInitialStep(self.placeStylusInTheImageStep)
      if currentStep == 'CaptureSpatialPositions':
        self.workflow.setInitialStep(self.captureSpatialPositionsStep)
      if currentStep == 'Registration':
        self.workflow.setInitialStep(self.registrationStep)
    else:
      print 'currentStep in parameter node is empty!'
        
    # start the workflow and show the widget
    self.workflow.start()
    self.workflowWidget.visible = True
    
    
    if widgetClass:
      self.widget = widgetClass(self.parent)
    self.parent.show()
    
    # self.moduleLogic = slicer.modules.StylusBasedUSProbeCalibration.logic()
    
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
   
      
 
 
class StylusBasedUSProbeCalibrationSliceletTestSlicelet(Slicelet):
  """ Creates the interface when module is run as a stand alone gui app.
  """

  def __init__(self):
    super(StylusBasedUSProbeCalibrationSliceletTestSlicelet, self).__init__(StylusBasedUSProbeCalibrationSliceletTestWidget)


if __name__ == "__main__":
  # TODO: need a way to access and parse command line arguments
  # TODO: ideally command line args should handle --xml

  import sys
  print(sys.argv)

  slicelet = StylusBasedUSProbeCalibrationSliceletTestSlicelet() 
  
