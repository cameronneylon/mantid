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
DEFAULT_IN_PATH = '/Users/Cameron/Documents/AA-ISIS-Docs/Experiments/'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import logging
import sys
import os
import shutil
from copy import deepcopy
import SansReduce
import lablogpost

# Import the UI
from sansReduceUI import Ui_sansReduceUI
from sansQueueUI import Ui_queuedReductionsUI

# Importing the Mantid Framework
try:
    from mantidsimple import *
    MANTID = True
except ImportError:
    def LoadRaw(filename, outws):
        pass
    def LoadSampleDetailsFromFaw(ws, filename):
        pass
    def SaveCanSAS1D(reduced, targetpath):
        print "Dummy reduced to CanSAS1D!"

    MANTID = False

try:
    import SANSReduction
except ImportError: 
    import SANSReduction_for_testing_only as SANSReduction

#
# Document Class for the Sans Reduction GUI
#
class SansReduceDoc(SansReduce.Standard1DReductionSANS2DRearDetector):
    """The document for handling the SANS Reduce GUI

    The document contains state variable for the GUI as well as
    an instance of 1D SANS2D reduction class as an internal 
    variable. Some GUI state variables need to persist outside
    the specific Reduction object instance such as the in path
    output path, maskfile, and direct beam. In addition there is 
    Reduction Queue, a list of Reduction objects ready for reduction.


    The document is a subclass of the standard 1D SANS2d
    reduction class from the SansReduce library. A few 
    extra options are stored and the finalised object 
    can then be stored in the queue or reduced as is. 
    """

    def __init__(self):
        self.inPath = DEFAULT_IN_PATH
        self.maskfile = ''
        self.directbeam = ''
        self.showRawInMenus = True
        self.showNexusInMenus = False
        self.outputLOQ = False
        self.outputCanSAS = True
        self.useRunnumberForOutput = True
        self.blog = False
        self.queue = False
        self.reductionQueue = []
        self.queueViewVisible = False
        self.outPath = ''
        self._inPathFileList = ''

        self.initCurrentReduction()

        # Blog variables
        self.blogurl = 'http://biolab.isis.rl.ac.uk'
        self.bloguid = ''
        self.blogusername = 'cameronneylon.net'
        self.blog_sname = 'testing_sandpit'
        self.blogreductionpost = None

    #########################################################
    # Map getters and setters onto internal Reduction object#
    #                                                       #
    # TODO: BUILD THE GETTERS AS WELL IF NECESSARY          #
    #########################################################

    def initCurrentReduction(self):
        """Initiate the reduction object for first or subsequent times

        The first time the object is initiated all internal variables will
        be set to null. These will then be built up as GUI elements are selected.
        After a reduction the object is re-initialised and in this case some 
        elements such as direct beam, maskfile, and path need to persist.
        """

        self.currentReduction = SansReduce.Standard1DReductionSANS2DRearDetector()
        self.currentReduction.setPathForAllRuns(self.inPath)

        # On the first initialisation directbeam and maskfile are None
        # so setting them will raise a ValueError in SansReduce.py
        if self.directbeam:
            self.currentReduction.setDirectBeam(self.directbeam)
        if self.maskfile:
            self.currentReduction.setMaskfile(self.maskfile)


    def setSansRun(self, qstring):
        self.currentReduction.setSansRun(qstring)

    def getSansRun(self):
        return self.currentReduction.getSansRun().getRunnumber()

    def setSansTrans(self, qstring):
        self.currentReduction.setSansTrans(qstring)

    def getSansTrans(self):
        return self.currentReduction.getSansTrans().getRunnumber()

    def setBackgroundRun(self, qstring):
        self.currentReduction.setBackgroundRun(qstring)

    def getBackgroundRun(self):
        return self.currentReduction.getBackgroundRun().getRunnumber()

    def setBackgroundTrans(self, qstring):
        self.currentReduction.setBackgroundTrans(qstring)

    def getBackgroundTrans(self):
        return self.currentReduction.getBackgroundTrans().getRunnumber()

    def setMaskfile(self, qstring):
        """Set the maskfile in reduction object and doc

        The maskfile needs to persist after a given reduction
        is performed. Here we set both a persistent variable
        outside the reduction object and one in the reduction
        object itself.
        """

        self.maskfile = qstring
        self.currentReduction.setMaskfile(qstring)

    def getMaskfile(self):
        """Getter for the document maskfile

        This method is required because we are persisting the
        record of the maskfile for the queue UI. This returns
        the value of maskfile held in the SansReduceGui Doc 
        and _not_ that held in the current reduction object.
        Currently self.maskfile is simply a string.
        """
        
        return self.maskfile

    def setDirectBeam(self, qstring):
        """Set the directbeam in reduction object and doc

        The direct beam needs to persists after a given 
        reduction is performed. Here we set both a persistent
        variable outside th reduction object and one in the
        reduction object itself.
        """
        try:
            assert type(qstring) == str or type(qstring) == QString
        except AssertionError:
            raise TypeError('Run identifier must be a string or QString')

        self.directbeam = qstring
        self.currentReduction.setDirectBeam(qstring)

    def getDirectBeam(self):
        """Getter for the document directbeam

        This method is required because we are persisting the
        record of the direct beam for the queue UI. This returns
        the value of directbeam held in the SansReduceGui Doc 
        and _not_ that held in the current reduction object.
        Currently self.directbeam is simply a string.
        """

        return self.directbeam

    def doReduction(self):
        """Map doReduction onto the Doc object for neatness"""

        self.currentReduction.doReduction()

    ###########################################################
    # Additional getters and setters required for doc methods #
    ###########################################################

    def setInPath(self, string):
        print str(string)
        if type(string) != str and type(string) != QString:
            raise TypeError("Path must be a str or QString")
        self.inPath = str(string)
        self.currentReduction.setPathForAllRuns(self.getInPath())

    def getInPath(self):
        return self.inPath

    def setShowRawInMenus(self, boolean):
        if type(boolean) != bool:
            raise TypeError('Value must be True or False')
            return
        self.showRawInMenus = boolean
        logging.debug("Doc:setShowRawInMenus: setto: " + 
                      str(self.showRawInMenus))

    def getShowRawInMenus(self):
        return self.showRawInMenus

    def setShowNexusInMenus(self, boolean):
        if type(boolean) != bool:
            raise TypeError('Value must be True or False')
            return
        self.showNexusInMenus = boolean

    def getShowNexusInMenus(self):
        return self.showNexusInMenus

    def setOutputLOQ(self, boolean):
        if type(boolean) != bool:
            raise TypeError('Value must be True or False')
            return
        self.outputLOQ = boolean

    def getOutputLOQ(self):
        return self.outputLOQ

    def setOutputCanSAS(self, boolean):
        if type(boolean) != bool:
            raise TypeError('Value must be True or False')
            return
        self.outputCanSAS = boolean

    def getOutputCanSAS(self):
        return self.outputCanSAS

    def setUseRunnumberForOutput(self, boolean):
        if type(boolean) != bool:
            raise TypeError('Value must be True or False')
            return
        self.useRunnumberForOutput = boolean

    def getUseRunnumberForOutput(self):
        return self.useRunnumberForOutput

    def setBlogReduction(self, boolean):
        if type(boolean) != bool:
            raise TypeError('Value must be True or False')
            return
        self.blog = boolean

    def getBlogReduction(self):
        return self.blog

    def setQueue(self, boolean):
        if type(boolean) != bool:
            raise TypeError('Value must be True or False')
            return
        self.queue = boolean

    def getQueue(self):
        return self.queue

    def setQueueViewVisible(self, boolean):
        if type(boolean) != bool:
            raise TypeError('Value must be True or False')
            return
        self.queueViewVisible = boolean

    def getQueueViewVisible(self):
        return self.queueViewVisible

    def setOutPath(self, string):
        """Set the output path

        The output path can be either a filename or a directory.
        If it is not set then system will default to the input
        directory.
        """

        if type(string) != str and type(string) != QString:
            raise TypeError("Path must be a string or QString")

        if not os.path.exists(string):
            raise ValueError('Outpath is incorrect or broken!')

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
        """A filter method for getting list of runs for menus

        This filter method is called from getRunListForMenu.
        """

        if type(string) != str:
            raise TypeError("Filter method includeRun requires a string")


        if string.endswith('.raw') and self.getShowRawInMenus():
            logging.debug("ends with raw and " + str(self.getShowRawInMenus()))
            return True
        elif string.endswith('.nxs') and self.getShowNexusInMenus():
            return True
        elif string.endswith('.nx5') and self.getShowNexusInMenus():
            return True
        else:
            return False

    def getRunListForMenu(self):
        """Method for returning a list of runs for the menus"""

        filesindir = os.listdir(self.getInPath())
        files = filter(self.includeRun, filesindir)

        filesformenu = []
        for file in files:
            file = file.lstrip('SANS2D0')
            filesformenu.append(file)

        # Sort the numbers into correct order
        filesformenu.sort()
        return filesformenu

    ############################
    # Reduce and Queue Methods #
    ############################

    def getReductionQueue(self):
        logging.debug("Doc:getReductionQueue: Queue has " + 
                      str(len(self.reductionQueue)) + " reductions")
        return self.reductionQueue

    def clearReductionQueue(self):
        self.reductionQueue = []

    def queueReduction(self):
        reductionToQueue = deepcopy(self)
        self.reductionQueue.append(reductionToQueue)
        # self.initForNewDocAfterQueuing

    def getReductionQueueLength(self):
        """Length method for the queue. Required for queue table."""
        return len(self.reductionQueue)

    def getQueueElement(self, index):
        """Will return a list for the indexth reduction in the queue

        The list is the runnumbers for the SANS, SANS transmission, 
        background and background transmission in that order. This
        method is required for building the queue table in the UI.
        """

        if index > len(self.reductionQueue):
            raise ValueError("Don't have that many reductions queued")

        list = []
        list.append(self.reductionQueue[index].getSansRun())
        list.append(self.reductionQueue[index].getSansTrans())
        list.append(self.reductionQueue[index].getBackgroundRun())
        list.append(self.reductionQueue[index].getBackgroundTrans())
        return list

    def writeOutputFiles(self, reduced, targetdirectory, filename):
        """Method for writing required output files after reduction

        This method takes a workspace and checks the document variables
        outPath, Runnumber, outputLOQ, and outputNexus to determine what
        needs to be written where. This means that this variables are 
        effectively global to a queued set of reductions. This should be
        fine in most circumstances.
        """
        # Check the target directory and filename make sense
        if not os.path.isdir(targetdirectory):
            raise IOError("Target directory does not exist")
        if not filename:
            raise IOError("I don't have a filename to save to")

        # Set up the path and write out the files
        targetpath = os.path.join(targetdirectory, filename)
        if self.outputLOQ:
            SaveRKH(reduced, targetpath + '.LOQ')
        if self.outputCanSAS:
            SaveCanSAS1D(reduced, targetpath + '.xml')
        

    def doSingleReduction(self):
        """Method for doing a single reduction
        """

        logging.debug("Doc:doSingleReduction: starting")
        # Do the actual reduction
        reduced = self.currentReduction.doReduction()
        targetdirectory, filename = os.path.split(self.getOutPath())
        
        # Construct a filename from run number if required
        if self.useRunnumberForOutput:
            filename = self.getSansRun().rstrip('-add')

        # Write out the required files
        self.writeOutputFiles(reduced, targetdirectory, filename)

        # If the reduction is to be blogged out
        if self.getBlogReduction():
            post_id =self.arrangeOutputPostsToBlog(os.path.join(
                                                      targetdirectory,
                                                      filename))
            self.appendReductionToReductionPost(post_id)
            self.closeAndPostReductionPost()
            self.blogreductionpost = None

        self.currentReduction = None
        self.initCurrentReduction()
        if MANTID:
            mantid.clear()

    def doQueuedReductions(self):
        """Method for carrying out the reductions in the queue"""

        if self.getBlogReduction():
            self.initialiseReductionPost()

        for reduction in self.getReductionQueue():
            reduced = reduction.currentReduction.doReduction()
            targetdirectory = self.getOutPath()
        
        # Construct a filename from run number if required
            if self.useRunnumberForOutput:
                filename = reduction.getSansRun().rstrip('-add')

        # Write out the required files
            self.writeOutputFiles(reduced, targetdirectory, filename)

        # If the reduction is to be blogged out
            if self.getBlogReduction():
                post_id = reduction.arrangeOutputPostsToBlog(os.path.join(
                                                      targetdirectory,
                                                      filename))
                self.blogreductionposttable.appendRow(
                        [reduction.getSansRun(), 
                         reduction.getSansTrans(),
                         reduction.getBackgroundRun(),
                         reduction.getBackgroundTrans(),
                         '[blog]' + post_id + '[/blog]'])

            # Clear the Mantid workspace before doing further reductions
            if MANTID:
                mantid.clear()

        #Close up the blog post when done if required
        if self.getBlogReduction():
            self.closeAndPostReductionPost()
            self.blogreductionpost = None



            # TODO - some monitoring and error catching here in case
            # some reductions don't proceed properly

    ################################
    # Blogging convenience methods #
    ################################

    def doOutputDataUploadToBlog(self, filepath):
        datapost = lablogpost.LaBLogData()
        datapost.set_type('inline')
        datapost.set_data(filepath)
        data_id = datapost.doPost(self.blogurl, self.bloguid)
        if data_id:
            return data_id
        else:
            raise Warning("Failed to upload %s to blog" % filepath)
            return False
 
    def arrangeOutputPostsToBlog(self, targetpath):
        """Method to set up the output post in the blog

        First the data is posted to the appropriate blog and
        the data numbers appended to a list. The actual post
        that will contain the data is then created and the 
        post_id returned.
        """

        datapostlist = []
        # Need to create a data post for each output object
        if self.outputLOQ:
            datapostlist.append(self.doOutputDataUploadToBlog(
                                     targetpath + '.LOQ'))
        if self.outputCanSAS:
            datapostlist.append(self.doOutputDataUploadToBlog(
                                     targetpath + '.xml'))

        # Set up the blog post that holds the output data
        outputblogpost = lablogpost.LaBLogPost()
        outputblogpost.set_username(self.blogusername)
        if self.getUseRunnumberForOutput():
            outputblogpost.set_title(self.getSansRun() + 
                                     ' - reduced SANS data')
        else:
            outputblog.post.set_title(os.path.basename(targetpath) +
                                      ' - reduced SANS data')
        outputblogpost.set_section('Data')
        outputblogpost.set_blog_sname(self.blog_sname)
        outputblogpost.set_metadata({'Data_type'  : 'SANS',
                              'Instrument' : self.currentReduction.getInstrument()})
        outputblogpost.set_attached_data(datapostlist)
        content = "Reduced SANS Data\n\n"
        for datapost in datapostlist:
            content += "[data]" + datapost + "[/data]\n\n"
        outputblogpost.set_content(content)
        outputpost_id = outputblogpost.doPost(self.blogurl, self.bloguid)
        if outputpost_id:
            return outputpost_id
        else:
            raise Warning("Failed to create the reduced data post")
            return False
            
    def initialiseReductionPost(self):
        if not self.blogreductionpost:
            self.blogreductionpost = lablogpost.LaBLogPost()
            self.blogreductionpost.set_title('SANS Data Reduction')
            self.blogreductionpost.set_username(self.blogusername)
            self.blogreductionpost.set_section('Procedure')
            self.blogreductionpost.set_blog_sname(self.blog_sname)
            self.blogreductionpost.set_metadata(
                      {'Procedure' : 'Data_reduction'})
            self.blogreductionpost.set_content = \
                """Reduction of SANS raw Data to 1D SANS Pattern"""
            self.blogreductionposttable = lablogpost.BlogTable(
                ['SANS Run', 'SANS Trans', 
                 'Bgd Run', 'Bgd Trans', 'Reduced data'])

    def appendReductionToReductionPost(self, datapost_id):
        """Append the new reduction entry to table"""

        self.blogreductionposttable.appendRow(
            [self.getSansRun(), 
             self.getSansTrans(),
             self.getBackgroundRun(),
             self.getBackgroundTrans(),
             '[blog]' + datapost_id + '[/blog]'])

    def closeAndPostReductionPost(self):
        """Finalise the reduction post and send to the blog"""

        table = self.blogreductionposttable.serialize()
        self.blogreductionpost.append_content(table)
        self.blogreductionpost.doPost(self.blogurl, self.bloguid)
        
            
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
        logging.debug("New Session------------------------------")
        self.doc = doc
        # The ui from designer is setup as self.ui
        self.ui = Ui_sansReduceUI()
        self.ui.setupUi(self)
        self.setGeometry(20, 100, 570, 420)

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
                     SIGNAL("activated(int)"),
                     self.setSansRun)

        self.connect(self.ui.sansTransMenu,
                     SIGNAL("activated(int)"),
                     self.setSansTrans)

        self.connect(self.ui.bgdRunMenu,
                     SIGNAL("activated(int)"),
                     self.setBgdRun)

        self.connect(self.ui.bgdTransMenu,
                     SIGNAL("activated(int)"),
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
                     SIGNAL("activated(int)"),
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

    def setIncomingDirectory(self, qstring = None):
        """Method for setting the input file directory"""

        if qstring:
            self.doc.setInPath(qstring)
            self.ui.inPathLineEdit.setText(qstring)
        else:
            if self.ui.inPathLineEdit.displayText() != self.doc.getInPath():
                self.doc.setInPath(self.ui.inPathLineEdit.displayText())
        self.initMenus()

    def setSansRun(self, int):
        """Set the run from the current menu selection"""

        logging.debug("Gui:setSansRun: settto " +
                        self.ui.sansRunMenu.currentText())
        self.doc.setSansRun(self.ui.sansRunMenu.currentText())

    def setSansTrans(self, int):
        """Set the run from the current menu selection"""
        logging.debug("Gui:setSansTrans: settto " +
                        self.ui.sansTransMenu.currentText())
        self.doc.setSansTrans(self.ui.sansTransMenu.currentText())

    def setBgdRun(self, int):
        """Set the run from the current menu selection"""
        logging.debug("Gui:setBgdRun: settto " +
                        self.ui.bgdRunMenu.currentText())
        self.doc.setBackgroundRun(self.ui.bgdRunMenu.currentText())
    
    def setBgdTrans(self, int):
        """Set the run from the current menu selection"""
        logging.debug("Gui:setBgdTrans: settto " +
                        self.ui.bgdTransMenu.currentText())
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


    def setDirectBeam(self, int):
        """Set the direct beam from the menu selection"""
        self.doc.setDirectBeam(self.ui.directBeamRunMenu.currentText())
        logging.debug("View:setDirectBeam: set to: " + 
                      self.ui.directBeamRunMenu.currentText())

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
        logging.debug('SRGui: Queue Checkbox activated: ' + str(integer))
        if integer == 0:
            self.doc.setQueue(False)
            self.ui.reducePushButton.setText("Reduce!")
        elif integer == 2:
            self.doc.setQueue(True)
            self.ui.reducePushButton.setText("Queue...")
        else:
            raise TypeError('Checkbox should be sending 0 or 2')

    def doReduceOrQueue(self):
        """Do the reduction or add it to the queue

        The menu selections are called just to be safe. The '1's are
        required because these are usually triggered via the 
        comboboxes activated(int) signal"""

        logging.debug("View:doReduceOrQueue")
        self.setSansRun(1); self.setSansTrans(1)
        self.setBgdRun(1); self.setBgdTrans(1)
        self.setDirectBeam(1)

        if not self.doc.getQueue():
            logging.debug("View:doReduceOrQueue: Starting single reduction")
            self.doc.doSingleReduction()

        else:
            logging.debug("View:doReduceOrQueue: Starting to queue reduction")
            self.doc.queueReduction()
            if self.doc.getQueueViewVisible():
                self.queueWindow.tablemodel = QueueTableModel(self.doc)
                self.queueWindow.ui.reductionQueueTableView.setModel(
                                          self.queueWindow.tablemodel)
                self.queueWindow.show()
                return
            else:
                self.queueWindow = QueueWindowView(self.doc)
                self.queueWindow.show()
                self.doc.setQueueViewVisible(True)

    def exitWidget(self):
        """Close the window"""
        self.close()
        self.destroy()

class QueueWindowView(QWidget):
    """A view for showing which reductions are currently queued

    First implementation is just to show them and provide a reduce
    button. More complex version should allow removal of items 
    from the queue.
    """

    def __init__(self, doc):
        """Initialisation method for the View
        """
        
        QWidget.__init__(self)
        self.doc = doc
        # The ui from designer is setup as self.ui
        self.ui = Ui_queuedReductionsUI()
        self.ui.setupUi(self)
        self.setGeometry(650, 100, 600, 400)

        # Add the relevant connections to populate UI elements
        self.ui.maskFileLineEdit.setText(self.doc.getMaskfile())
        self.ui.directBeamLineEdit.setText(
                     self.doc.getDirectBeam())
        self.connect(self.ui.maskFilePushButtonQueue,
                     SIGNAL("clicked()"),
                     self.changeMaskFileForQueue)
        self.connect(self.ui.directBeamPushButtonQueue,
                     SIGNAL("clicked()"),
                     self.changeDirectBeamForQueue)
        self.connect(self.ui.cancelQueuePushButton,
                     SIGNAL("clicked()"),
                     self.cancelReductionQueue)
        self.connect(self.ui.reduceQueuePushButton,
                     SIGNAL("clicked()"),
                     self.doQueuedReductions)
        self.tablemodel = QueueTableModel(self.doc)
        self.ui.reductionQueueTableView.setModel(self.tablemodel)

    def changeMaskFileForQueue(self):
        """Method for changing the maskfile for queue

        This method needs to change the mask file for
        each reduction in the queue. There is currently no
        means of changing them independently through the 
        GUI.
        """

        maskfilepath = QFileDialog.getOpenFileName(self, 
                    'Select Mask File',
                    self.doc.getInPath())
        self.ui.maskFileLineEdit.setText(maskfilepath)
        for reduction in self.doc.getReductionQueue():
            reduction.setMaskfile(maskfilepath)

    def changeDirectBeamForQueue(self):
        """Method for changing the direct beam run for queue

        This method needs to change the direct beam run for
        each reduction in the queue. There is currently no
        means of changing them independently through the 
        GUI.
        """
        directbeampath = QFileDialog.getOpenFileName(self,
                                                         'Select Direct Beam',
                                                         self.doc.getInPath())
        directbeamrun = os.path.basename(str(directbeampath)).lstrip('SANS2D0')
        self.ui.directBeamLineEdit.setText(directbeamrun)
        for reduction in self.doc.getReductionQueue():
            reduction.setDirectBeam(directbeamrun)
           
    def cancelReductionQueue(self):
        """Method for cancelling the queue

        This method will both close the queue window and
        clear the queue, allowing the user to start again
        with a new queue.
        """
            
        self.doc.clearReductionQueue()
        self.close()
        self.destroy()

    def doQueuedReductions(self):
        """UI Calling method for doing the full set of reductions

        Calls the document method for doing the queued reductions and
        then kills the queue and closes the queue window.
        """

        self.doc.doQueuedReductions()
        self.cancelReductionQueue()

class QueueTableModel(QAbstractTableModel):
    """A class to provide the model for the queue table"""

    def __init__(self, doc, parent = None):
        QAbstractTableModel.__init__(self, parent)
        self.doc = doc
        self.headerdata = ['SANS Run #', 'SANS Transmission',
                           'Bgd Run #', 'Bgd Transmission', '']

    def rowCount(self, parent):
        return self.doc.getReductionQueueLength()

    def columnCount(self, parent):
        return 5

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        elif index.column() == 4:
            return QVariant()
        else:
            return QVariant(self.doc.getQueueElement(index.row())[index.column()])

    def headerData(self, col, orientation, role):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()
    

app = QApplication.instance()
# If running outside of Mantid need a QApp
if app == None:
 # But if running tests we don't want that...
 if sys.argv[0] != 'tests.py':
   app = QApplication(sys.argv) 
   LOG_FILENAME = '/logging.out'
   logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
  
   doc = SansReduceDoc()
   docview = SansReduceView(doc)
   docview.show()  
   app.exec_()

else:
   #LOG_FILENAME = '/logging.out'
   #logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
 
   doc = SansReduceDoc()
   docview = SansReduceView(doc)
   docview.show()  

