'''
Created on 28/03/2013

@author: Usuario
'''
import os
from PropertiesMenu import *

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
        path=slicer.modules.usguidedprocedure.path
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
        
        
        #add the annotations widget   (just to see also the annotations)
        #the annotations widgets is refreshed in self.updateWidgetFromParameters
    #    self.annotationLayout = qt.QVBoxLayout()
    #    self.__layout.addLayout(self.annotationLayout, 1)
        
    #    # Load a fiducials list 
    #    loadFiducialsListButton = qt.QPushButton("Test image points lists creation")
    #    loadFiducialsListButton.toolTip = "Load a fiducials list to test registration"
    #    self.__layout.addWidget(loadFiducialsListButton)
    #    loadFiducialsListButton.connect('clicked(bool)', self.onLoadFiducialListClicked)
    
        #listeners
        #self.listenToAnnotations()
        self.updatingList = False
        self.placeImageFiducialStep=False
        
    def setPlaceImageFiducialStep(self,isPlaceImageFiducialStep):
        self.placeImageFiducialStep = isPlaceImageFiducialStep
            
    def getFiducialsWidget(self):
        return self.fiducialsWidget
           
    def setModuleLogic(self,logic):   
        self.logic=logic
        
    def onPlaceFiducialButtomClicked(self):   
        self.logic.addFiducialToList("Fiducials List") 
        qt.QApplication.setOverrideCursor(self.placeFiducialCursor)  

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
        
    def onFiducialsListModified(self, caller,  event):
        if self.updatingList:
          return
        #print('Scene changed !')
        #print(event)
        if self.placeImageFiducialStep:
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
          crosshairNode=slicer.util.getNode("Crosshair")
          crosshairNode.SetCrosshairMode(0)
          # populate the list
          fiducialListNode=slicer.util.getNode("Fiducials List")
          
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
              #Qt::NoItemFlags    0    It does not have any properties set.
              #Qt::ItemIsSelectable    1    It can be selected.
              #Qt::ItemIsEditable    2    It can be edited.
              #Qt::ItemIsDragEnabled    4    It can be dragged.
              #Qt::ItemIsDropEnabled    8    It can be used as a drop target.
              #Qt::ItemIsUserCheckable    16    It can be checked or unchecked by the user.
              #Qt::ItemIsEnabled    32    The user can interact with the item.
              #Qt::ItemIsTristate    64    The item is checkable with three separate states.
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 0).setFlags( 1 | 2 | 32)  # name is selectable and  not editable and user checkable
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 1).setFlags(32)  # position is not selectable and not editable 
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 2).setFlags(0)  #ID is disabled (final version should hide this column)
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 3).setFlags(32)  #ID is disabled (final version should hide this column)
              self.fiducialsWidget.fiducialsList.item(childrenIndex, 4).setFlags(0)  #ID is disabled (final version should hide this column)
              
          
          self.updatingList = False     
          
    def updateSpatialFiducialsList(self):
          #clear list
          #self.fiducialsWidget.fiducialsList.clear()
          
          #raise this flag to ignore change events in the table, the flag is lowered at the end of this method
          self.updatingList = True
          
          # populate the list
          fiducialListNode=slicer.util.getNode("Fiducials List")
          
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
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,0,item.clone())
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,1,item.clone())
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,2,item.clone())
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,3,item.clone())
              self.fiducialsWidget.fiducialsList.setItem(childrenIndex,4,item.clone())
    
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
        