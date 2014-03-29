'''
Created on 28/03/2013

@author: Usuario
'''
import os

from __main__ import vtk, qt, ctk, slicer

class FiducialsList():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        """
        path=slicer.modules.usguidedprocedure.path
        modulePath=os.path.dirname(path)
        loadedDataGUIfile=os.path.join(modulePath,"USGuidedWizard/loadedData.ui")
        f = qt.QFile(loadedDataGUIfile)
        #f = qt.QFile('C:/Users/Usuario/devel/slicelets/USGuidedProcedure/USGuidedWizard/fiducials.ui')
        f.open(qt.QFile.ReadOnly)
        loader = qt.QUiLoader()
        self.loadedDataWidget = loader.load(f)
        f.close()
        """
        
        # UI   from QtDesigner  -----------------------------------------------------------------------------
        path=slicer.modules.stylusbasedusprobecalibration.path
        modulePath=os.path.dirname(path)
        fiducialsStepGUIfile=os.path.join(modulePath,"GUI/fiducials.ui")
        f = qt.QFile(fiducialsStepGUIfile)
        #f = qt.QFile('C:/Users/Usuario/devel/slicelets/USGuidedProcedure/USGuidedWizard/fiducials.ui')
        f.open(qt.QFile.ReadOnly)
        loader = qt.QUiLoader()
        self.fiducialsWidget = loader.load(f)
        f.close()
        
        # connect signals and slots
        self.fiducialsWidget.fiducialsList.connect('cellChanged(int ,int )', self.onFiducialNameChanged) 
        self.fiducialsWidget.placeFiducialButton.connect('clicked(bool)', self.onPlaceFiducialButtomClicked) 
        self.fiducialsWidget.removeFiducialButton.connect('clicked(bool)', self.onRemoveFiducialButtonClicked)
        self.fiducialsWidget.clearFiducialsListButton.connect('clicked(bool)', self.onClearFiducialsListButtonClicked)
        self.fiducialsWidget.fiducialsList.itemClicked.connect(self.onFiducialsListClicked)
    
        #listeners
        #self.listenToAnnotations()
        self.updatingList = False
        self.placeImageFiducialStep=False
        pixmap=qt.QPixmap("Resources/Icons/AnnotationPointWithArrow.png")
        self.placeFiducialCursor= qt.QCursor(pixmap)
        
    def setPlaceImageFiducialStep(self,isPlaceImageFiducialStep):
        self.placeImageFiducialStep = isPlaceImageFiducialStep
            
    def getFiducialsWidget(self):
        return self.fiducialsWidget
           
    def setModuleLogic(self,logic):   
        self.logic=logic
        
    def onPlaceFiducialButtomClicked(self):    
        
        if self.fiducialsWidget.fiducialsList.rowCount ==0:
          ret=qt.QMessageBox.warning(self.fiducialsWidget, 'Fiducials List', 'You must have image fiducials to match with tracker positions.', qt.QMessageBox.Ok , qt.QMessageBox.Ok )
          return

        currentRow = self.fiducialsWidget.fiducialsList.currentRow()
        print("Current row is: " + str(currentRow))
    
        if currentRow==-1:
          ret=qt.QMessageBox.warning(self.fiducialsWidget, 'Fiducials List', 'You must select an image fiducials to match with the tracker position.', qt.QMessageBox.Ok , qt.QMessageBox.Ok )
          return
    
        self.currentFiducialName =self.fiducialsWidget.fiducialsList.item(currentRow, 0).text()
        qt.QApplication.setOverrideCursor(self.placeFiducialCursor) 
        self.listenToFiducialNodeAdded()
        self.logic.addFiducialToList("Fiducials List") 
        
        
            
    def listenToFiducialNodeAdded(self):
      print "Listening to Fiducials List modifications"   
      listNode = slicer.util.getNode("Fiducials List")   
      self.fiducialsListObserver = listNode.AddObserver('ModifiedEvent', self.onFiducialNodeAdded)
   
#---------------------------------------------------------------------------------------------------------------

   
    def doNotListenToFiducialNodeAdded(self): 
      listNode = slicer.util.getNode("Fiducials List") 
      listNode.RemoveObserver(self.fiducialsListObserver)  
      

    def onFiducialsListModified(self,caller,event):
      if self.updatingList:
        return
      self.updateFiducialsList("Tracker Points List") 
       
       
    def onFiducialNodeAdded(self,caller,event):
      
        #print('Scene changed !')
        #print(event) 
      print "Fiducials List Modified"  
      self.doNotListenToFiducialNodeAdded()
      currentRow = self.fiducialsWidget.fiducialsList.currentRow()
      
      listNode = slicer.util.getNode("Fiducials List")
      numberOfChildrenNodes=listNode.GetNumberOfChildrenNodes()
      childrenNode=listNode.GetNthChildNode(numberOfChildrenNodes-1)
      if childrenNode is not None:
        fidNode = childrenNode.GetAssociatedNode() 
        fidNode.SetName(self.currentFiducialName) 
            
      qt.QApplication.restoreOverrideCursor()        
      
    
    def onFiducialsListClicked(self, item):
      if self.placeImageFiducialStep == True:  
        print "Fiducials list clicked"  
        self.currentRow = self.fiducialsWidget.fiducialsList.currentRow()
        self.currentColumn = self.fiducialsWidget.fiducialsList.currentColumn() 
        if self.currentRow >= 0 :
          snapshotImageName = self.fiducialsWidget.fiducialsList.item(self.currentRow, 0).text() + "-Snapshot_Texture" 
          fiducialName = self.fiducialsWidget.fiducialsList.item(self.currentRow, 0).text()  
          imageNode = slicer.util.getNode(snapshotImageName)  
          if imageNode is not None:
            # Set the background volume 
            redWidgetCompNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceCompositeNodeRed")
            redWidgetCompNode.SetBackgroundVolumeID(imageNode.GetID())  
            vrdl=self.logic.getVolumeResliceDriverLogic()    
            redNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
            vrdl.SetDriverForSlice(imageNode.GetID(), redNode)
            vrdl.SetModeForSlice(vrdl.MODE_TRANSVERSE180, redNode)   
            redNode.SetSliceVisible(False)
            slicer.util.resetSliceViews()
            self.logic.hideAllTheFiducialsNode("Fiducials List")
            fiducialNode = slicer.util.getNode(fiducialName)
            if fiducialNode is not None:
              fiducialNode.SetDisplayVisibility(True)    

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
        crosshairNode=slicer.util.getNode("Crosshair")
        crosshairNode.SetCrosshairMode(1) 
        self.logic.addFiducialsToImageList()   
           
    def listenToListModifications(self):
        self.sceneObserver = slicer.mrmlScene.AddObserver('ModifiedEvent', self.onFiducialsListModified)
        
    def doNotListenToListModifications(self):    
        slicer.mrmlScene.RemoveObserver(self.sceneObserver)
        
        
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
      
    def updateFiducialsList(self,listName):
          #clear list
          #self.fiducialsWidget.fiducialsList.clear()
          
          #raise this flag to ignore change events in the table, the flag is lowered at the end of this method
          self.updatingList = True
          # populate the list
          trackerListNode=slicer.util.getNode(listName)
          
          if not trackerListNode:
              return
          
          print 'updateFiducialsList'
          print trackerListNode.GetNumberOfChildrenNodes()
          self.fiducialsWidget.fiducialsList.setRowCount(trackerListNode.GetNumberOfChildrenNodes())
          
          item = qt.QTableWidgetItem('dummy')
          for childrenIndex in xrange(trackerListNode.GetNumberOfChildrenNodes()):              
    #          print childrenIndex
    #          print fidID , "  -  ",  fidName,  "  ------>  " ,  fidPos[0], ",", fidPos[1], ",", fidPos[2]
              
              #create the items for the cells
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,0,item.clone())
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,1,item.clone())
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,2,item.clone())
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,3,item.clone())
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,4,item.clone())
    
              # put the values in the items  
              fidHierarchyNode=trackerListNode.GetNthChildNode(childrenIndex)
              trackerNode=fidHierarchyNode.GetAssociatedNode()
              if trackerNode is not None:      
                trackerNodeName = trackerNode.GetName()
                trackerNodeId = trackerNode.GetID()
                spatialPos=[0,0,0]
                trackerNode.GetFiducialCoordinates(spatialPos)
              fidName = trackerNodeName.split("-")  
              fidName = fidName[0]
              fidNode=slicer.util.getNode(fidName)  
              if fidNode is not None:
                  fidPos=[0,0,0]
                  dummy=fidNode.GetFiducialCoordinates(fidPos)
                  fidID=fidNode.GetID()
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setText(fidName)
              if fidNode is not None:   
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setText(fidPos)
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setText(fidID)
                self.fiducialsWidget.fiducialsList.item(childrenIndex , 0).setCheckState(2)
              else:
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setText('')
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setText('')
              if trackerNode is not None:
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setText(spatialPos)
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setText(trackerNodeId)
              else:
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setText('')
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setText('')
    
              #restrict edition to the names (AG: no encontr los textos de los flags en el qt module
              # flags of the cells
              #Qt::NoItemFlags    0    It does not have any properties set.
              #Qt::ItemIsSelectable    1    It can be selected.
              #Qt::ItemIsEditable    2    It can be edited.
              #Qt::ItemIsDragEnabled    4    It can be dragged.
              #Qt::ItemIsDropEnabled    8    It can be used as a drop target.
              #Qt::ItemIsUserCheckable    16    It can be checked or unchecked by the user.
              #Qt::ItemIsEnabled    32    The user can interact with the item.
              #Qt::ItemIsTristate    64    The item is checkable with three separate states.
              if self.placeImageFiducialStep == True:
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setFlags( 1 | 16 | 32)  # name is selectable and  not editable and user checkable
              else:      
                self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setFlags( 1 | 2 | 32)  # name is selectable and  not editable and user checkable     
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setFlags(32)  # position is not selectable and not editable 
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setFlags(0)  #ID is disabled (final version should hide this column)
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setFlags(32)  #ID is disabled (final version should hide this column)
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setFlags(0)  #ID is disabled (final version should hide this column)
              
          
          self.updatingList = False     
          
    def addNewEmptyRow(self, rowIndex):   
      item = qt.QTableWidgetItem("dummy") 
      self.fiducialsWidget.fiducialsList.setItem(rowIndex,0,item.clone())
      self.fiducialsWidget.fiducialsList.setItem(rowIndex,1,item.clone())
      self.fiducialsWidget.fiducialsList.setItem(rowIndex,2,item.clone())
      self.fiducialsWidget.fiducialsList.setItem(rowIndex,3,item.clone())
      self.fiducialsWidget.fiducialsList.setItem(rowIndex,4,item.clone())  
          
    def updateSpatialFiducialsList(self):
          #clear list
          #self.fiducialsWidget.fiducialsList.clear()
          
          #raise this flag to ignore change events in the table, the flag is lowered at the end of this method
          self.updatingList = True
          
          # populate the list
          fiducialListNode=slicer.util.getNode("Tracker Points List")
          
          if not fiducialListNode:
              return
          
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
              
              trackerNode=slicer.util.getNode(fidName + '-Tracker')  
              if trackerNode is not None:
                  spatialPos=[0,0,0]
                  dummy=trackerNode.GetFiducialCoordinates(spatialPos)
                  trackerNodeName = trackerNode.GetName()
                  trackerNodeId=trackerNode.GetID()
    #          print childrenIndex
    #          print fidID , "  -  ",  fidName,  "  ------>  " ,  fidPos[0], ",", fidPos[1], ",", fidPos[2]
              
              #create the items for the cells
#               self.fiducialsWidget.fiducialsList.setItem(childrenIndex,0,item.clone())
#               self.fiducialsWidget.fiducialsList.setItem(childrenIndex,1,item.clone())
#               self.fiducialsWidget.fiducialsList.setItem(childrenIndex,2,item.clone())
#               self.fiducialsWidget.fiducialsList.setItem(childrenIndex,3,item.clone())
#               self.fiducialsWidget.fiducialsList.setItem(childrenIndex,4,item.clone())
              self.addNewEmptyRow(childrenIndex)
    
              # put the values in the items          
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setText(fidName)
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setText(fidPos)
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setText(fidID)
              if trackerNode is not None:
                  self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setText(spatialPos)
                  self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setText(trackerNodeId)
              else:
                  self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setText('')
                  self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setText('')
    
              #restrict edition to the names (AG: no encontr los textos de los flags en el qt module
              # flags of the cells
              #Qt::NoItemFlags    0    It does not have any properties set.
              #Qt::ItemIsSelectable    1    It can be selected.
              #Qt::ItemIsEditable    2    It can be edited.
              #Qt::ItemIsDragEnabled    4    It can be dragged.
              #Qt::ItemIsDropEnabled    8    It can be used as a drop target.
              #Qt::ItemIsUserCheckable    16    It can be checked or unchecked by the user.
              #Qt::ItemIsEnabled    32    The user can interact with the item.
              #Qt::ItemIsTristate    64    The item is checkable with three separate states.
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setFlags( 1 | 16 | 32)  # name is selectable and  not editable and user checkable
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setFlags(32)  # position is not selectable and not editable 
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setFlags(0)  #ID is disabled (final version should hide this column)
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setFlags(32)  #ID is disabled (final version should hide this column)
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setFlags(0)  #ID is disabled (final version should hide this column)
              
          
          self.updatingList = False              
        