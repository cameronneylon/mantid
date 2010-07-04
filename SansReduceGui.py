# SansReduce: A GUI utility for Reducing SANS data in the Mantid
# Neutron Scattering Analysis framework
#
# Copyright (C) 2010 Cameron Neylon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#
# Global Variables the user may wish to set
#
DEFAULT_IN_PATH = '/Users/Cameron/Documents/AA - ISIS Docs/Experiments/'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import logging
import sys
import os
import shutil
import SansReduce

# Importing the Mantid Framework
try:
    from mantidsimple import *
except ImportError:
    def LoadRaw(filename, outws):
        pass
    def LoadSampleDetailsFromFaw(ws, filename):
        pass

try:
    import SANSReduction
except ImportError: 
    import SANSReduction_for_testing_only as SANSReduction

# Import the UI
from sansReduceUI import Ui_Form




#
# Document Class for the Sans Reduction GUI
#
class SansReduceDoc(SansReduce.Standard1DReductionSANS2DRearDetector):
    """The document for handling the SANS Reduce GUI

    The document is a subclass of the standard 1D SANS2d
    reduction class from the SansReduce library. A few 
    extra options are stored and the finalised object 
    can then be stored in the queue or reduced as is. 
    """

    def __init__(self):
        SansReduce.Standard1DReductionSANS2DRearDetector.__init__(self)

        self.inPath = DEFAULT_IN_PATH
        self.showRawInMenus = True
        self.showNexusInMenus = False

        self.outputLOQ = False
        self.outputCanSAS = True
        self.useRunnumberForOutput = False
        self.blog = False
        self.queue = False
        self.reductionQueue = []
        self.outPath = ''

        self._inPathFileList = ''

    def initForNewDocAfterQueuing(self):
        self.setSansRun()
        self.setBackgroundRun()

    ###########################################
    # Additional getters and setters required #
    ###########################################

    def setInPath(self, string):
        if type(string) != str and type(string) != QString:
            raise TypeError("Path must be a str or QString")
        self.inPath = str(string)

    def getInPath(self):
        return self.inPath

    def setShowRawInMenus(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.showRawInMenus = boolean

    def getShowRawInMenus(self):
        return self.getShowRawInMenus

    def setShowNexusInMenus(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.showNexusInMenus = boolean

    def getShowNexusInMenus(self):
        return self.showNexusInMenus

    def setOutputLOQ(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.outputLOQ = bool

    def getOutputLOQ(self):
        return self.outputLOQ

    def setOutputCanSAS(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.outputCanSAS = bool

    def getOutputCanSAS(self):
        return self.outputCanSAS

    def setUseRunnumberForOutput(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.useRunnumberForOutput = boolean

    def getUseRunnumberForOutput(self):
        return self.useRunnumberForOutput

    def setBlogReduction(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.blog = bool

    def getBlogReduction(self):
        return self.blog

    def setQueue(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.queue = bool

    def getQueue(self):
        return self.queue

    def setOutPath(self, string):
        """Set the output path

        The output path can be either a filename or a directory.
        If it is not set then system will default to the input
        directory.
        """

        if type(string) != string and type(string) != QString:
            raise TypeError("Path must be a string or QString")
            return
        self.outPath = str(string)

    def getOutPath(self):
        """If the outpath is set, return it, if not then return inPath
        
        OutPath can be either a filename or a directory depending on
        how it has been set.
        """

        if self.outPath:
            return self.outPath
        else:
            return self.inPath

    ################################
    # Utility Methods for Document #
    ################################

    def includeRun(self, string):
        if string.endswith('.raw') and self.getShowRawInMenus():
            return True
        elif string.endswith('.nxs') and self.getShowNexusInMenus():
            return True
        elif string.endswith('.nx5') and self.getShotNexusInMenus():
            return True
        else:
            return False

    def getRunListForMenu(self):
        """Method for returning a list of runs for the menus"""

        filesindir = os.listdir(self.getInPath())
        files = filter(self.includeRun, filesindir)

        files.sort()
        filesformenu = []
        for file in files:
            file = file.lstrip('SANS2D0')
            filesformenu.append(file)
        return filesformenu

    ############################
    # Reduce and Queue Methods #
    ############################

    def doReduceOrQueue(self):
        if self.queue:
            self.queueReduction

        else:
            self.doSingleReduction

    def queueReduction(self):
        reductionToQueue = deepcopy(self)
        self.reductionQueue.append(reductionToQueue)
        self.initForNewDocAfterQueuing


    def doSingleReduction(self):
        """Method for doing a single reduction
        """

        # Do the actual reduction
        reduced = self.doReduction()
        targetdirectory, filename = os.path.split(self.getOutPath())
        
        # Construct a filename from run number if required
        if self.useRunnumberForOutput:
            filename = self.getSansRun().getRunnumber().rstrip('-add')

        # Check the target directory and filename make sense
        if not os.path.isdir(targetdirectory):
            raise IOError("Target directory does not exist")
        if not filename:
            raise IOError("I don't have a filename to save to")

        # Set up the path and write out the files, then clear workspaces
        targetpath = os.path.join(targetdirectory, filename)
        if self.outputLOQ:
            SaveRKH(reduced, targetpath + '.LOQ')
        if self.outputCanSAS:
            SaveCanSAS1D(reduced, targetpath + '.xml')
        mantid.clear()

            
class SansReduceView(QWidget):
    """The view for the SANS Reduce GUI

    The view was built in QtDesigner and is imported from
    sansReduceUI above. The view simply initialises, 
    connects up signal and implements some convenience
    methods for handling population of menus and UI changes.
    """

    def __init__(self, doc):
        """Initialisation method for the View
        """
        
        QWidget.__init__(self)
        self.doc = doc
        # The ui from designer is setup as self.ui
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Init GUI elements
        self.initMenus()

        #######################################
        # Initialise connections from the view#
        #######################################

        # Incoming file path
        self.connect(self.ui.inPathPushButton, 
                     SIGNAL("clicked()"),
                     self.selectDirectoryDialog)

        self.connect(self.ui.inPathLineEdit,
                     SIGNAL("editingFinished()"),
                     self.setIncomingDirectory)

        # Run, bgd, trans selection menus
        self.connect(self.ui.sansRunMenu,
                     SIGNAL("activated()"),
                     self.setSansRun)

        self.connect(self.ui.sansTransMenu,
                     SIGNAL("activated()"),
                     self.setSansTrans)

        self.connect(self.ui.bgdRunMenu,
                     SIGNAL("activated()"),
                     self.setBgdRun)

        self.connect(self.ui.bgdTransMenu,
                     SIGNAL("activated()"),
                     self.setBgdTrans)

        # Options for the run selection
        self.connect(self.ui.showRawCheckbox,
                     SIGNAL("stateChanged(int)"),
                     self.showRawCheckStateChanged)

        self.connect(self.ui.showNexusCheckbox,
                     SIGNAL("stateChanged(int)"),
                     self.showNexusCheckStateChanged)

        self.connect(self.ui.maskFilePushButton,
                     SIGNAL("clicked()"),
                     self.selectMaskFileDialog)

        self.connect(self.ui.directBeamRunMenu,
                     SIGNAL("activated()"),
                     self.setDirectBeam)

        # Options for the reduction output
        self.connect(self.ui.outputLOQCheckbox,
                     SIGNAL("stateChanged(int)"),
                     self.outputLOQCheckStateChanged)

        self.connect(self.ui.outputCanSASCheckbox,
                     SIGNAL("stateChanged(int)"),
                     self.outputCanSASCheckStateChanged)

        self.connect(self.ui.useRunnumberCheckbox,
                     SIGNAL("stateChanged(int)"),
                     self.useRunnumberCheckStateChanged)

        self.connect(self.ui.blogReductionCheckbox,
                     SIGNAL("stateChanged(int)"),
                     self.blogReductionCheckStateChanged)

        self.connect(self.ui.outPathPushButton,
                     SIGNAL("clicked()"),
                     self.setOutPathDialog)

        # Final selections, Queue vs Reduce and Reduce button
        self.connect(self.ui.queueReductionsCheckbox,
                     SIGNAL("stateChanged(int)"),
                     self.queueReductionsCheckStateChanged)

        self.connect(self.ui.reducePushButton,
                     SIGNAL("clicked()"),
                     self.doReduceOrQueue)

        self.connect(self.ui.cancelPushButton,
                     SIGNAL("clicked()"),
                     self.exitWidget)

        
        ###########################################
        # Initialise connections from the document#
        ###########################################

        # TODO Catch state changes that might be caused by
        # scripts running against the document

    ##############################
    # GUI initialisation Methods #
    ##############################

    def initMenus(self):
        runlist = self.doc.getRunListForMenu()
        menulist = [self.ui.sansRunMenu,
                    self.ui.sansTransMenu,
                    self.ui.bgdRunMenu,
                    self.ui.bgdTransMenu,
                    self.ui.directBeamRunMenu]

        for menu in menulist:
            menu.clear()

        self.ui.directBeamRunMenu.addItem("Direct Beam Run")
        self.ui.directBeamRunMenu.setCurrentIndex(0)
        for run in runlist:
            for menu in menulist:
                menu.addItem(run)

    ####################################
    #Method definitions for GUI actions#
    ####################################

    def selectDirectoryDialog(self):
        """Select the input file directory"""

        directory = QFileDialog.getExistingDirectory(self, 
                    'Open Directory',
                    self.doc.getInPath())
        self.setIncomingDirectory(directory)

    def setIncomingDirectory(self, qstring):
        """Method for setting the input file directory"""

        self.doc.setInPath(qstring)
        self.doc.setPathForAllRuns(self.doc.getInPath())
        self.ui.inPathLineEdit.setText(qstring)
        self.initMenus()

    def setSansRun(self):
        """Set the run from the current menu selection"""
        self.doc.setSansRun(self.ui.sansRunMenu.currentText())

    def setSansTrans(self):
        """Set the run from the current menu selection"""
        self.doc.setSansTrans(self.ui.sansTransMenu.currentText())

    def setBgdRun(self):
        """Set the run from the current menu selection"""
        self.doc.setBackgroundRun(self.ui.bgdRunMenu.currentText())
    
    def setBgdTrans(self):
        """Set the run from the current menu selection"""
        self.doc.setBackgroundTrans(self.ui.bgdTransMenu.currentText())

    def showRawCheckStateChanged(self, integer):
        """Reset the menus to show required input files"""
        logging.debug('SRGui: Show Raw Checkbox activated: ' + str(integer))
        if integer == 0:
            self.doc.setShowRawInMenus(False)
        elif integer == 2:
            self.doc.setShowRawInMenus(True)
        else:
            raise TypeError('Checkbox should be sending 0 or 2')
        
        self.initMenus()
        
    def showNexusCheckStateChanged(self, integer):
        """Reset the menus to show required input files"""
        logging.debug('SRGui: Show Nexus Checkbox activated: ' + str(integer))
        if integer == 0:
            self.doc.setShowNexusInMenus(False)
        elif integer == 2:
            self.doc.setShowNexusInMenus(True)
        else:
            raise TypeError('Checkbox should be sending 0 or 2')

        self.initMenus()

    def selectMaskFileDialog(self):
        """Select and set the mask file"""

        maskfilepath = QFileDialog.getOpenFileName(self, 
                    'Open Directory',
                    self.doc.getInPath())
        self.doc.setMaskfile(maskfilepath)


    def setDirectBeam(self):
        """Set the direct beam from the menu selection"""
        self.doc.setDirectBeam(self.ui.directBeamRunMenu.currentText())

    def outputLOQCheckStateChanged(self, integer):
        """Set whether a LOQ file will be output"""
        logging.debug('SRGui: Output LOQ Checkbox activated: ' + str(integer))
        if integer == 0:
            self.doc.setOutputLOQ(False)
        elif integer == 2:
            self.doc.setOutputLOQ(True)
        else:
            raise TypeError('Checkbox should be sending 0 or 2')

    def outputCanSASCheckStateChanged(self, integer):
        """Set whether a CanSAS file will be output"""
        logging.debug('SRGui: Output CanSAS Checkbox activated: ' 
                        + str(integer))
        if integer == 0:
            self.doc.setOutputCanSAS(False)
        elif integer == 2:
            self.doc.setOutputCanSAS(True)
        else:
            raise TypeError('Checkbox should be sending 0 or 2')

    def useRunnumberCheckStateChanged(self, integer):
        """Set whether the Runnumber will be used as filename"""
        logging.debug('SRGui: Use runno Checkbox activated: ' + str(integer))
        if integer == 0:
            self.doc.setUseRunnumberForOutput(False)
            self.ui.outPathPushButton.setText("Output filename...")
        elif integer == 2:
            self.doc.setUseRunnumberForOutput(True)
            self.ui.outPathPushButton.setText("Output directory...")

        else:
            raise TypeError('Checkbox should be sending 0 or 2')

    def blogReductionCheckStateChanged(self, integer):
        """Set whether the output will be blogged

        This checkbox will need to open a new widget window for
        setting various blog settings"""
        logging.debug('SRGui: Blog Checkbox activated: ' + str(integer))
        if integer == 0:
            self.doc.setBlogReduction(False)
        elif integer == 2:
            self.doc.setBlogReduction(True)
        else:
            raise TypeError('Checkbox should be sending 0 or 2')

    def setOutPathDialog(self):
        """Trigger a dialog for setting the output path

        If the filename is set to be taken from the runnumber then
        a directory selection dialog is presented. Otherwise a save
        file dialog is given. The path is given the same in both 
        cases and we will clean up when we are ready to write the
        file out. Extensions will be cleaned up at that point as 
        well.
        """
  
        if self.doc.getUseRunnumberForOutput():
            outfilepath = QFileDialog.getExistingDirectory(self, 
                    'Select Directory',
                    self.doc.getInPath())

        else:
            outfilepath = QFileDialog.getSaveFileName(self,
                    'Choose path and set filename',
                    self.doc.getInPath())
        # Then set that as the path
        self.doc.setOutPath(outfilepath)                                                      

    def queueReductionsCheckStateChanged(self, integer):
        """Set whether reductions will be run or queued"""
        logging.debug('SRGui: Blog Checkbox activated: ' + str(integer))
        if integer == 0:
            self.doc.setQueue(False)
            self.ui.reducePushButton.setText("Reduce!")
        elif integer == 2:
            self.doc.setQueue(True)
            self.ui.reducePushButton.setText("Queue...")
        else:
            raise TypeError('Checkbox should be sending 0 or 2')

    def doReduceOrQueue(self):
        """Do the reduction or add it to the queue"""
        self.doc.doReduceOrQueue

    def exitWidget(self):
        """Close the window"""
        self.close()
        self.destroy()


app = QApplication.instance()
if app == None:
   app = QApplication(sys.argv) 
   LOG_FILENAME = '/logging.out'
   logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
  
   doc = SansReduceDoc()
   docview = SansReduceView(doc)
   docview.show()  
   app.exec_()

else:
   doc = SansReduceDoc()
   docview = SansReduceView(doc)
   docview.show()  

