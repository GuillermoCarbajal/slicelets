'''
Created on 28/03/2013

@author: Usuario
'''
import os
from PropertiesMenu import *

from __main__ import vtk, qt, ctk, slicer

class VolumeRenderingViewer():
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
        self.listWidget = qt.QListWidget() 
        print("Constructor of VolumeRenderingViewer executed")
        self.listWidget.show()
        self.currentItem=None
        
        self.listWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)  
        self.propertiesMenu = PropertiesMenu()
        
        #qt.QObject.connect(self.propertiesMenu,qt.SIGNAL("colorButtonClicked"),self.onColorButtonClicked)
        #TODO: should be a way to emit a signal from the PropertiesMenu class but I do not how
        self.propertiesMenu.colourButton.connect("clicked()",self.onColorButtonClicked) 
        self.propertiesMenu.meshOpacitySlider.connect('valueChanged(int)', self.onSliderMoved)
        self.propertiesMenu.checkBoxVisible3D.connect("stateChanged(int)",self.onVisible3DChanged)
        
        
    def getListWidget(self):
        return self.listWidget
           
    def setModuleLogic(self,logic):   
        self.logic=logic
           
    def listenToScene(self):
        vl=slicer.modules.volumes
        vl=vl.logic()  
        vl.SetMRMLScene(slicer.mrmlScene)
        self.sceneObserver = vl.AddObserver('ModifiedEvent', self.onVolumeAdded)
        #self.sceneObserver = slicer.mrmlScene.AddObserver('ModifiedEvent', self.onVolumeAdded)
        
    def onVolumeAdded(self, caller,  event):
        print("Volumes module was modified")
        
        numVolumes=slicer.mrmlScene.GetNumberOfNodesByClass("vtkMRMLScalarVolumeNode") 
        print "Number of volumes: " + str(numVolumes)
        #print('A model was added to the scene !')
        if numVolumes>0:
            for i in xrange(0,numVolumes):
                node = slicer.mrmlScene.GetNthNodeByClass(i, "vtkMRMLScalarVolumeNode")
                if not (node==None): 
                    if (not (node.GetName() == "Image_Reference")):     
                        print(node.GetName())  
                        isAlreadyInList=False 
                        j=0
                        while ((j < self.listWidget.count) and (not isAlreadyInList)):
                            isAlreadyInList=node.GetName()==self.listWidget.item(j).text()
                            j=j+1
                        if not isAlreadyInList:
                            print('A volume was added to the scene !')
                            self.listWidget.addItem(node.GetName())
                            node=slicer.util.getNode(node.GetName())
                            node=slicer.vtkMRMLScalarVolumeNode.SafeDownCast(node)
                            self.logic.onVolumeAdded(node)
                            #print("Info of added node:")
    
    
        
    def addItem(self,item):
        self.listWidget.addItem(item)
        
    def onItemDoubleClicked(self,item):
        vrNode=slicer.util.getNode("CPURayCastVolumeRendering")
        slicer.mrmlScene.AddNode(vrNode)
        self.currentItem=item;
        # Get the current display node
        node=slicer.util.getNode(self.currentItem.text())
        node=slicer.vtkMRMLScalarVolumeNode.SafeDownCast(node)
        
        self.currentDisplayNode=node.GetDisplayNode()
        currentOpacity= self.currentDisplayNode.GetOpacity()
        self.propertiesMenu.meshOpacitySlider.setValue(currentOpacity*100)
        isVisible=self.currentDisplayNode.GetVisibility()
        self.propertiesMenu.checkBoxVisible3D.setCheckState(isVisible)
        
        #print item.text()
        self.propertiesMenu.show()
        
    def onColorButtonClicked(self):
        print("Color button clicked SIGNAL captured!!")    
        # Set the current color to the dialog
        colorDialog=qt.QColorDialog()
        currentColor=self.currentDisplayNode.GetColor()
        qtCurrentColor=qt.QColor(currentColor[0]*255,currentColor[1]*255,currentColor[2]*255)
        color=colorDialog.getColor(qtCurrentColor)
        if color.isValid():
            b=float(color.blue())/255
            r=float(color.red())/255
            g=float(color.green())/255
            self.currentDisplayNode.SetColor(r,g,b)
           
    def onSliderMoved(self,opacity):
        # Get the current display node
        print("Slider movement captured!")
        #print opacity
        self.currentDisplayNode.SetOpacity(float(opacity)/100)
        
    def onVisible3DChanged(self,isVisible):
        #print isVisible
        self.currentDisplayNode.SetVisibility(isVisible)