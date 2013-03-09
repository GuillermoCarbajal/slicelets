from __main__ import qt, ctk

from USGuidedStep import *
from Helper import *

class PlaceImageFiducialsStep( USGuidedStep ) :

  def __init__( self, stepid ):
    self.initialize( stepid )
    self.setName( '2. PlaceImageFiducials' )
    self.setDescription( 'Place fiducials in the image' )
    
    self.updatingList = False
    
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
    
    # UI   from QtDesigner  -----------------------------------------------------------------------------
    f = qt.QFile('C:/Program Files/Slicer 4.2.0-2013-02-13/bin/Python/USGuidedWizard/fiducials.ui')
    f.open(qt.QFile.ReadOnly)
    loader = qt.QUiLoader()
    self.fiducialsWidget = loader.load(f)
    f.close()
    self.__layout.addWidget(self.fiducialsWidget)
    
    # connect signals and slots
    self.fiducialsWidget.fiducialsList.connect('cellChanged(int ,int )', self.onFiducialNameChanged) 
    self.fiducialsWidget.placeFiducialButton.connect('clicked(bool)', self.onPlaceFiducialButtomClicked) 
    self.fiducialsWidget.removeFiducialButton.connect('clicked(bool)', self.onRemoveFiducialButtonClicked)
    self.fiducialsWidget.clearFiducialsListButton.connect('clicked(bool)', self.onClearFiducialsListButtonClicked)

    #customize the UI
    self.fiducialsWidget.placeSpatialButton.setVisible(False)
    self.fiducialsWidget.placeFiducialButton.setVisible(True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(2, True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(3, True)
    self.fiducialsWidget.fiducialsList.setColumnHidden(4, True)
    
    
    #add the annotations widget   (just to see also the annotations)
    #the annotations widgets is refreshed in self.updateWidgetFromParameters
#    self.annotationLayout = qt.QVBoxLayout()
#    self.__layout.addLayout(self.annotationLayout, 1)
    
#    # Load a fiducials list 
#    loadFiducialsListButton = qt.QPushButton("Test image points lists creation")
#    loadFiducialsListButton.toolTip = "Load a fiducials list to test registration"
#    self.__layout.addWidget(loadFiducialsListButton)
#    loadFiducialsListButton.connect('clicked(bool)', self.onLoadFiducialListClicked)

    self.updateWidgetFromParameters(self.parameterNode())

    #listeners
    #self.listenToAnnotations()
    self.listenToScene()
    
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
    print("We are in the validate function of PlaceImageFiducialsStep")

  def onEntry(self, comingFrom, transitionType):

    super(PlaceImageFiducialsStep, self).onEntry(comingFrom, transitionType)
    self.updateWidgetFromParameters(self.parameterNode())
    pNode = self.parameterNode()
    pNode.SetParameter('currentStep', self.stepid)
    print("We are in the onEntry function of PlaceImageFiducialsStep")
    qt.QTimer.singleShot(0, self.killButton)

  def onExit(self, goingTo, transitionType):
    self.doStepProcessing()
    
    super(PlaceImageFiducialsStep, self).onExit(goingTo, transitionType) 
    print("We are in the onExit function of PlaceImageFiducialsStep")
  
  
  def updateWidgetFromParameters(self, parameterNode):
    print("We are in the place fiducials step")
#    self.annotationLayout.removeWidget(slicer.modules.annotations.widgetRepresentation())
#    self.annotationLayout.addWidget(slicer.modules.annotations.widgetRepresentation())
    
    # update the fiducials list
    


  def doStepProcessing(self):
    # calculate the transform to align the ROI in the next step with the
    # baseline volume
    pNode = self.parameterNode()
    

  def onPlaceFiducialButtomClicked(self):   
    self.logic.changeMousePlacingState()  

  def onRemoveFiducialButtonClicked(self):   
      
    if self.fiducialsWidget.fiducialsList.rowCount ==0:
      return
    
    
    ret=qt.QMessageBox.question(self.fiducialsWidget, 'Fiducials List', 'The selected fiducial will be deleted. This action cannot be undone. \n Confirm?', qt.QMessageBox.Ok | qt.QMessageBox.Cancel, qt.QMessageBox.Cancel )
        
    if ret==qt.QMessageBox.Cancel:
      return
    
    currentRow = self.fiducialsWidget.fiducialsList.currentRow()
    print currentRow
    if currentRow>=0:
        fidID = self.fiducialsWidget.fiducialsList.item(currentRow, 2).text()
        fidNode = slicer.mrmlScene.GetNodeByID(fidID)
        logic = slicer.modules.annotations.logic()
        logic.RemoveAnnotationNode(fidNode)
        # slicer.mrmlScene.RemoveNode(fidNode)
    
    fiducialListNode=slicer.util.getNode("Fiducials List")
    print 'RemoveFiducial'
    print fiducialListNode.GetNumberOfChildrenNodes()
    
    
  def onClearFiducialsListButtonClicked(self):   
        
    if self.fiducialsWidget.fiducialsList.rowCount ==0:
      return
    
    ret=qt.QMessageBox.question(self.fiducialsWidget, 'Fiducials List', 'The list will be cleared. This action cannot be undone. \n Confirm?', qt.QMessageBox.Ok | qt.QMessageBox.Cancel, qt.QMessageBox.Cancel )
    
    if ret==qt.QMessageBox.Cancel:
      return
    
    fiducialListNode=slicer.util.getNode("Fiducials List")
    fiducialListNode.RemoveChildrenNodes()
    
#    for row in range(self.fiducialsWidget.fiducialsList.rowCount):
#      fidID = self.fiducialsWidget.fiducialsList.item(row, 2).text()
#      fidNode = slicer.mrmlScene.GetNodeByID(fidID)
#      #slicer.mrmlScene.RemoveNode(fidNode)    #Esto no anda porque no mantiene bien la jerarquia y la FiducialList se cree que sigue teniendo los nodos
#      logic = slicer.modules.annotations.logic()
#      logic.RemoveAnnotationNode(fidNode)

    self.updateFiducialsList()
    

  def onLoadFiducialListClicked(self):  
    self.logic.addFiducialsToImageList()   

  def listenToAnnotations(self):
    annotationsLogic = slicer.modules.annotations.logic()
    annotationsLogic.AddObserver('AnyEvent', self.onAnnotationsChanged)
    
  def listenToScene(self):
    self.sceneObserver = slicer.mrmlScene.AddObserver('ModifiedEvent', self.onSceneChanged)  
        
  def onAnnotationsChanged(self, caller,  event):
      if self.updatingList:
          return
      
      print('Annotations changed !')
      print(event)
      self.updateFiducialsList()
  
  def onSceneChanged(self, caller,  event):
      if self.updatingList:
        return
      print('Scene changed !')
      print(event)
      self.updateFiducialsList()
      
  def onFiducialNameChanged(self, row,  col) :
      # this is called when a name is changed in the list to change the underlying fiducial name
      
      #ignore events while updating the list
      if self.updatingList:
        return
        
      fidID = self.fiducialsWidget.fiducialsList.item(row, 2).text()
      fidName=self.fiducialsWidget.fiducialsList.item(row, 0).text()
      
      fidNode=slicer.mrmlScene.GetNodeByID(fidID)
      
      if fidNode:
          fidNode.SetName(fidName)
      
      
        
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
          
          # put the values in the items          
          self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setText(fidName)
          self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setText(fidPos)
          self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setText(fidID)
          
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
          self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setFlags(1 | 2 | 32)  # name is selectable and editable 
          self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setFlags(32)  #position is not selectable and not editable 
          self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setFlags(0)  #ID is disabled (final version should hide this column)
          
          
      self.updatingList = False


