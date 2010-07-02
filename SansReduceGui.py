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
class SansReduceDoc(QObject):
    """The document for handling the SANS Reduce GUI

    The document is a subclass of the standard 1D SANS2d
    reduction class from the SansReduce library. A few 
    extra options are stored and the finalised object 
    can then be stored in the queue or reduced as is. 
    """

    def __init__(self):
        SansReduce.Standard1DReductionSANS2DRearDetector.__init__(self)

        self.showRawInMenus = True
        self.showNexusInMenus = False

        self.outputLOQ = False
        self.outputCanSAS = True
        self.useRunnumberForOutput = False
        self.blogoutput = False
        self.queue = False
        self.outPath = ''

    def setShowRawInMenus(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.showRawInMenus = bool

    def getShowRawInMenus(self):
        return self.getShowRawInMenus

    def setShowNexusInMenus(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.showNexusInMenus = bool

    def getShowCanSASInMenus(self):
        return self.showNexusInMenus

    def setOutputLOQ(self, boolean):
        if type(boolean) != bool:
            raise ValueError('Value must be True or False')
            return
        self.outputLOQ = bool

    def getOutputLOQ(self):
        return self.outputLOQ

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
        # The ui from designer is setup as self.ui
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Init GUI elements
        self.initDefaultDir()
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
                     signal("activated()"),
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
                     signal("clicked()"),
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
        # scripting of the document

    ####################################
    #Method definitions for GUI actions#
    ####################################

    def selectDirectoryDialog(self):
        """Select the input file directory"""

    def setIncomingDirectory(self):
        """Method for setting the input file directory"""

    def setSansRun(self):
        """Set the run from the current menu selection"""

    def setSansTrans(self):
        """Set the run from the current menu selection"""

    def setBgdRun(self):
        """Set the run from the current menu selection"""
    
    def setBgdTrans(self):
        """Set the run from the current menu selection"""

    def showRawCheckStateChanged(self):
        """Reset the menus to show required input files"""

    def showNexusCheckStateChanged(self):
        """Reset the menus to show required input files"""

    def selectMaskFileDialog(self):
        """Select and set the mask file"""

    def setDirectBeam(self):
        """Set the direct beam from the menu selection"""

    def outputLOQCheckStateChanged(self, state):
        """Set whether a LOQ file will be output"""

    def outputCanSASCheckStateChanged(self, state):
        """Set whether a CanSAS file will be output"""

    def outputRunnumberCheckStateChanged(self, state):
        """Set whether the Runnumber will be used as filename"""

    def outputblogReductionCheckStateChanged(self, state):
        """Set whether the output will be blogged

        This checkbox will need to open a new widget window for
        setting various blog settings"""

    def setOutPathDialog(self):
        """Trigger a dialog for setting the output path"""

    def queueReductionsCheckStateChanged(self, state):
        """Set whether reductions will be run or queued"""

    def doReduceOrQueue(self):
        """Do the reduction or add it to the queue"""

    def exitWidget(self):
        """Close the window"""

