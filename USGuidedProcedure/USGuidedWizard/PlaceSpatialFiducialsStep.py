from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *

class PlaceSpatialFiducialsStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '3. Place spatial Fiducials' )
    self.setDescription( 'Place fiducials using the tracker' )

    self.__parent = super( PlaceSpatialFiducialsStep, self )

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

    # UI   from QtDesigner  -----------------------------------------------------------------------------
    f = qt.QFile('C:/Program Files/Slicer 4.2.0-2013-02-13/bin/Python/USGuidedWizard/fiducials.ui')
    f.open(qt.QFile.ReadOnly)
    loader = qt.QUiLoader()
    self.fiducialsWidget = loader.load(f)
    f.close()
    self.__layout.addWidget(self.fiducialsWidget)

    #customize the UI
    self.fiducialsWidget.placeSpatialButton.setVisible(True)
    self.fiducialsWidget.placeFiducialButton.setVisible(False)
    self.fiducialsWidget.fiducialsList.setColumnHidden(2, True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(4, True)

    #connect signals and slots
    self.fiducialsWidget.placeSpatialButton.connect('clicked(bool)', self.onPlaceTrackerPositionButtonClicked)


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
    print("We are in the validate function of PlaceSpatialFiducialsStep")

  def onEntry(self, comingFrom, transitionType):

    super(PlaceSpatialFiducialsStep, self).onEntry(comingFrom, transitionType)
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    
    
    print("We are in the onEntry function of PlaceSpatialFiducialsStep coming from:" )
    print comingFrom.name()
    qt.QTimer.singleShot(0, self.killButton)

    #After the connection is necessary to add models and transforms that will be used during navigation
    referenceToRASNode=slicer.vtkMRMLLinearTransformNode()
    slicer.mrmlScene.AddNode(referenceToRASNode)
    referenceToRASNode.SetName("ReferenceToRAS")
    imageReferenceNode=slicer.util.getNode("Image_Reference")
    imageReferenceNode.SetAndObserveTransformNodeID(referenceToRASNode.GetID())
    #Add the stylus model
    modelsModule=slicer.modules.models
    modelsModuleLogic=modelsModule.logic()
    modelsModuleLogic.SetMRMLScene(slicer.mrmlScene)
    modelsModuleLogic.AddModel("C:/Program Files/Slicer 4.2.0-2013-02-13/bin/Python/USGuidedWizard/Stylus_Example.stl")
    stylusModelNode=slicer.util.getNode("Stylus_Example")
    matrix=vtk.vtkMatrix4x4()
    matrix.SetElement(0,3,-210)
    stylusTipToStylusTipModel=slicer.vtkMRMLLinearTransformNode()
    slicer.mrmlScene.AddNode(stylusTipToStylusTipModel)
    stylusTipToStylusTipModel.SetAndObserveMatrixTransformToParent(matrix)
    stylusTipToStylusTipModel.SetName("StylusTipToStylusTipModel")
    stylusModelNode.SetAndObserveTransformNodeID(stylusTipToStylusTipModel.GetID())
    ## Associate the model of the stylus with the stylus tip transforms
    stylusTipToReferenceNode=slicer.util.getNode("StylusTipToReference")
    stylusTipToStylusTipModel.SetAndObserveTransformNodeID(stylusTipToReferenceNode.GetID())
    ## Associate the stylus to reference tranform with the reference to RAS
    stylusTipToReferenceNode.SetAndObserveTransformNodeID(referenceToRASNode.GetID())

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    super(PlaceSpatialFiducialsStep, self).onExit(goingTo, transitionType) 
    print("We are in the onExit function of PlaceSpatialFiducialsStep")

  def updateWidgetFromParameters(self, parameterNode):
    print("We are in the place fiducials step")
    self.updateFiducialsList()
    



  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()
    
    self.updateListNodesForRegistration()

#  def onPlaceTrackerPositionButtonClicked(self):   
#    self.logic.recordTrackerPosition()
#    

  def onLoadSpatialPointsListClicked(self):  
    self.logic.addFiducialsToTrackerList()   


  def onPlaceTrackerPositionButtonClicked(self):   

    if self.fiducialsWidget.fiducialsList.rowCount ==0:
      ret=qt.QMessageBox.warning(self.fiducialsWidget, 'Fiducials List', 'You must have image fiducials to match with tracker positions.', qt.QMessageBox.Ok , qt.QMessageBox.Ok )
      return

    currentRow = self.fiducialsWidget.fiducialsList.currentRow()
    print currentRow

    # TODO uncomment this line and comment all the following TODO
    self.logic.recordTrackerPosition()
    
    ## TODO  get the tracker position
    ## We must have here a node or a nodeID from the tracker points list
    ## For the moment we have a node that has the same position as the fiducial 
    fiducialListNode=slicer.util.getNode("Fiducials List")
    #trackerListNode=slicer.util.getNode("Tracker Points List")
    #saml = slicer.modules.annotations.logic() 
    #saml.SetActiveHierarchyNodeID(trackerListNode.GetID())
    
    fidHierarchyNode=fiducialListNode.GetNthChildNode(currentRow)
    fidNode=fidHierarchyNode.GetAssociatedNode()        
    #fidPos=[0,0,0]
    #dummy=fidNode.GetFiducialCoordinates(fidPos)
    fidName = fidNode.GetName()
    fidID = fidNode.GetID()

    #trackerNode=slicer.vtkMRMLAnnotationFiducialNode()
    #trackerNode.SetFiducialWorldCoordinates(fidPos)
    #trackerNode.SetName(fidName + '-Tracker')	
    #slicer.mrmlScene.AddNode(trackerNode)
    # TODO  get the tracker position (end)
    
    #get the most recent node (the last) in the Tracker Points List
    trackerNode = self.logic.getFiducialNode('Tracker Points List', -1)
    trackerNode.SetName(fidName + '-Tracker')
    
    
    # Associate the fiducial and the tracker position
    # We remove the previous (if exist) tracker node 
    # and we put the new tracker node ID in the table and check the row
    previousTrackerID = self.fiducialsWidget.fiducialsList.item(currentRow, 4).text()
    previousTrackerNode = slicer.mrmlScene.GetNodeByID(previousTrackerID)
    if  previousTrackerNode:
      logic = slicer.modules.annotations.logic()
      logic.RemoveAnnotationNode(previousTrackerNode)
    
    self.fiducialsWidget.fiducialsList.item(currentRow, 3).setText(trackerNode.GetName())
    self.fiducialsWidget.fiducialsList.item(currentRow, 4).setText(trackerNode.GetID())
    self.fiducialsWidget.fiducialsList.item(currentRow, 0).setCheckState(2)



  def updateFiducialsList(self):
    #clear list
    #self.fiducialsWidget.fiducialsList.clear()

    #raise this flag to ignore change events in the table, the flag is lowered at the end of this method
    self.updatingList = True

    # populate the list
    fiducialListNode=slicer.util.getNode("Fiducials List")
    print 'updateFiducialsList'
    print fiducialListNode.GetNumberOfChildrenNodes()
    self.fiducialsWidget.fiducialsList.setRowCount(fiducialListNode.GetNumberOfChildrenNodes())

    item = qt.QTableWidgetItem('dummy')
    for childrenIndex in xrange(fiducialListNode.GetNumberOfChildrenNodes()):
        fidHierarchyNode=fiducialListNode.GetNthChildNode(childrenIndex)
        fidNode=fidHierarchyNode.GetAssociatedNode()
        if not fidNode:
          print 'Fid node nulo'
          continue

        fidPos=[0,0,0]
        dummy=fidNode.GetFiducialCoordinates(fidPos)
        fidName = fidNode.GetName()
        fidID = fidNode.GetID()
  #          print childrenIndex
  #          print fidID , "  -  ",  fidName,  "  ------>  " ,  fidPos[0], ",", fidPos[1], ",", fidPos[2]

        #create the items for the cells
        self.fiducialsWidget.fiducialsList.setItem(childrenIndex,0,item.clone())
        self.fiducialsWidget.fiducialsList.setItem(childrenIndex,1,item.clone())
        self.fiducialsWidget.fiducialsList.setItem(childrenIndex,2,item.clone())
        self.fiducialsWidget.fiducialsList.setItem(childrenIndex,3,item.clone())
        self.fiducialsWidget.fiducialsList.setItem(childrenIndex,4,item.clone())

        # put the values in the items          
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setText(fidName)
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setText(fidPos)
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setText(fidID)
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setText('')
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setText('')

        #restrict edition to the names (AG: no encontr los textos de los flags en el qt module
        # flags of the cells
        #Qt::NoItemFlags	0	It does not have any properties set.
        #Qt::ItemIsSelectable	1	It can be selected.
        #Qt::ItemIsEditable	2	It can be edited.
        #Qt::ItemIsDragEnabled	4	It can be dragged.
        #Qt::ItemIsDropEnabled	8	It can be used as a drop target.
        #Qt::ItemIsUserCheckable	16	It can be checked or unchecked by the user.
        #Qt::ItemIsEnabled	32	The user can interact with the item.
        #Qt::ItemIsTristate	64	The item is checkable with three separate states.
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setFlags( 1 | 16 | 32)  # name is selectable and  not editable and user checkable
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setFlags(32)  #position is not selectable and not editable 
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setFlags(0)  #ID is disabled (final version should hide this column)
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setFlags(32)  #ID is disabled (final version should hide this column)
        self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setFlags(0)  #ID is disabled (final version should hide this column)


    self.updatingList = False


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
      print row
      print fidID
      print trackerID
      
      fidNode = slicer.mrmlScene.GetNodeByID(fidID)
      trackerNode = slicer.mrmlScene.GetNodeByID(trackerID)
      print fidNode
      print trackerNode
      
      #if the row is selected to be used in the registration
      if self.fiducialsWidget.fiducialsList.item(row, 0).checkState()==2:
        print 'Checked row'
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
