# AddRaw: A GUI utility for adding RAW files together in the Mantid
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

#from mantidsimple import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import logging
import sys
import os

DEFAULT_PATH = '/Users/Cameron/Documents/AA - ISIS Docs/Experiments/'

class addRawDoc(QObject):
    """Document for RAW file addition process
    """

    def __init__(self, *args):
        apply(QObject.__init__, (self,) + args)
        
        logging.debug('addRawDoc: Initialising new Document')
        self.path = DEFAULT_PATH
        self.runlist = []
        self.outname = ''
        self.outpath = ''
        self.filelist = []
        self.useincomingfilename = False

    def checkType(self, check, testtype):

        try:
            if  testtype == str:
                assert (type(check) == QString or 
                        type(check) == str or
                        type(check) == unicode)

            elif testtype == list:
                assert type(check) == list

            elif testtype == bool:
                assert type(check) == bool
        
        except AssertionError:
            # raise TypeError('Must be set with a string or similar')
            return False

        return True        

# Getters and Setters

    def setPath(self, string):
        if self.checkType(string, str):
            self.path = string
            self.initFilelist()
            self.emit(SIGNAL('sigDocPathSet'))
            logging.debug('addRawDoc: Path set to ' + self.path)

    def getPath(self):
        return self.path

    def setRunlist(self, listofruns):
        """Method to set runlist from the view

        The runlist can be a list of shortened file names at this
        point so requires cleanup and conversion to proper filenames
        before doing addition.
        """

        if self.checkType(listofruns, list):
            self.runlist = listofruns
            logging.debug('addRawDoc: Runlist set to: ' + str(self.runlist))

    def appendToRunlist(self, run):
        if self.checkType(run, str):
            self.runlist.append(run)
        
        elif self.checkType(run, int):
            self.runlist.append(str(run))

    def getRunlist(self):
        return self.runlist

    def setOutname(self, string):
        if self.checkType(string, str):
            self.outname = string

    def getOutname(self):
        if self.useincomingfilename:
            l = self.getRunlist()[:]
            l.sort()
            return l[-1]
        elif self.outname:
            return self.outname
        else:
            return 'temp_add_workspace'

    def setUseIncomingFilename(self, boolean):
        if self.checkType(boolean, bool):
            self.useincomingfilename = boolean
            self.emit(SIGNAL('sigDocUseIncomingChanged'))

    def getUseIncomingFilename(self):
        return self.useincomingfilename

    def setOutpath(self, string):
        if self.checkType(string, str):
            self.outpath = string

    def getOutpath(self):
        if self.outpath:
            return self.outpath
        elif self.path:
            return self.path
        else:
            return False

    def initFilelist(self):
        self.filelist = []
        if self.getPath():
            for file in os.listdir(self.getPath()):
                self.filelist.append(file)

    def getFilelist(self):
        return self.filelist
      

##############################
#
# Business end methods for Document                         
#
##############################

    def addRuns(self):
        """Method for doing the actual raw file adding
        
        Due to some vagaries in the Mantid framework it is important
        firstly to load the initial run separately rather than add
        to an empty workspace and then to clean up afterwards to save
        memory. If this isn't done then currently Mantid will crash 
        out after loading up around six workspaces.
        """

        filenamelist = self.runlistToFilenames()
        inpath = str(self.getPath())
        outpath = str(self.getOutpath())
        name = str(self.getOutname())

        # Load the first run in
        filename = os.path.join(inpath, str(filenamelist[0])) 
        LoadRaw(Filename=filename, OutputWorkspace="added")

        # Then sequentially load and add each additional run
        for run in filenamelist[1:-1]:
            filename = os.path.join(inpath, str(run))
            LoadRaw(Filename=filename, OutputWorkspace="wtemp")
            Plus("added", "wtemp", "added")

        # Write out the new nexus file and clean up
        SaveNexus("added", os.path.join(outpath, (name +'.nxs'))) 
        mantid.deleteWorkspace("wtemp")
        mantid.deleteWorkspace("added")
        print self.runlist
        self.runlist = []
        print self.runlist

    def getFilelistForMenu(self):
        """Method for getting a sanitised filename list for menus in GUI
        """

        logging.debug('addRawDoc: Getting filelist for menu')
        infilelist = self.getFilelist()[0:-1]
        innerlooplist = []
        outfilelist = []
        logging.debug('addRawDoc: Filelist:' + str(infilelist))
        for file in infilelist:
            # If Raw then remove file suffix
            if file.endswith('.raw'):
                innerlooplist.append(file)
            
        # If it begins with large run number prefix then remove
        for file in innerlooplist:
            outfilelist.append(file.rstrip('.raw').lstrip('SANS2D000'))

        logging.debug('Returned filelist:' + str(outfilelist))
        return outfilelist

    def runlistToFilenames(self):
        """Method to take self.runlist and rebuild filenames

        Requires some thoughout how to do this best. For the moment
        the conversion is just hardcoded.
        """

        filelist = []
        for run in self.runlist:
            filelist.append('SANS2D0000' + run + '.raw')

        return filelist

class menusWidget(QWidget):
    """QT Widget controlling menus for selecting run numbers/files
    """
    def __init__(self, doc, *args):
        apply(QWidget.__init__, (self,) + args)

        self.doc = doc
        self.menulist = []
        self.grid = QGridLayout()


        # Set up the plus button
        self.plusbutton = QToolButton()
        self.plusbutton.setIcon(QIcon('images/onebit_31.png'))
        self.connect(self.plusbutton,
                          SIGNAL('clicked()'),
                          self.addMenu)

        # And the minus button (deactivated on init)
        self.minusbutton = QToolButton()
        self.minusbutton.setIcon(QIcon('images/onebit_33.png'))
        self.minusbutton.setEnabled(False)
        self.connect(self.minusbutton,
                          SIGNAL('clicked()'),
                          self.removeMenu)

        # Initial two menus for run selection
        self.addMenu();self.addMenu()
        self.setLayout(self.grid)

    def addMenu(self):
        newmenu = QComboBox()
        self.menulist.append(newmenu)
        
        # If path is set then populate the menu
        newmenu.clear()
        if self.doc.getPath():
            newmenu.addItem('')
            for file in self.doc.getFilelistForMenu():
                newmenu.addItem(file)
                newmenu.setEnabled(True)

        # If path is not set offer a friendly reminder and deactivate menu
        else:
            newmenu.addItem('Select a directory first')
            newmenu.setEnabled(False)


        # Connect signals to appropriate methods
        self.connect(newmenu, SIGNAL('currentIndexChanged(int)'),
                              self.emitRunMenuSelected)

        # Set in appropriate position and reposition +/- buttons
        self.grid.addWidget(newmenu,
                            len(self.menulist)+1, 0)
        self.repositionPlusMinusButtons()
        self.minusbutton.setEnabled(True)

    def removeMenu(self):
        """Remove a menu when not needed any more
        """
        self.grid.removeWidget(self.menulist[-1])
        self.menulist.pop().destroy()

        for menu in self.menulist:
            self.grid.removeWidget(menu)

        i=0
        for menu in self.menulist:
            i+=1
            self.grid.addWidget(menu, i, 0)

        self.repositionPlusMinusButtons()
        self.setLayout(self.grid)
        if len(self.menulist) == 0:
            self.minusbutton.setEnabled(False)


    def repositionPlusMinusButtons(self):
        """Reposition the add and remove menu buttons
        """
        self.grid.removeWidget(self.plusbutton)
        self.grid.removeWidget(self.minusbutton)
        self.grid.addWidget(self.plusbutton, (len(self.menulist)+1), 1)
        self.grid.addWidget(self.minusbutton, (len(self.menulist)+1), 2)

    def emitRunMenuSelected(self, int):
        self.emit(SIGNAL('sigViewRunMenuSelected'))
        logging.debug('add_raw: Emitted sigViewRunMenuSelected')

    def init(self):

        logging.debug('menusWidget: Initialising menu - path:' + 
                      self.doc.getPath())
        for menu in self.menulist:
            # If path is set then populate the menu
            menu.clear()
            if self.doc.getPath():
                menu.addItem('')
                for file in self.doc.getFilelistForMenu():
                    menu.addItem(file)
                menu.setEnabled(True)

            # If path is not set offer a friendly reminder and deactivate menu
            else:
                menu.addItem('Select a directory first')
                menu.setEnabled(False)            

    def getRunList(self):
        runlist = []
        for menu in self.menulist:
            if (menu.currentText() != '' and menu.currentIndex() != 0):
                runlist.append(menu.currentText())
        
        if runlist != []:
            return runlist
        else:
            return False
            

            
class addFileWidget(QWidget):
    """Qt Widget for selecting Raw files to add
    """

    def __init__(self, doc, *args):
        apply(QWidget.__init__, (self,) + args)
        
        # Set the passed document as the document of the view
        # The document is created by the controller just before
        # the view so it should be the right type. Probably a good
        # idea to provide a check of this in each subclass.
        self.doc = doc

        # Set up the window, title, grab focus and set layout as grid
        self.setGeometry(100, 100, 600, 300)
        self.setWindowTitle('Add RAW files')
        self.setFocus()
        self.grid = QGridLayout()

        # Textbox and directory select button for path
        self.pathlineedit = QLineEdit()
        self.selectpathbutton = QPushButton('Select Directory', self)
        self.grid.addWidget(self.pathlineedit, 0, 0)
        self.grid.addWidget(self.selectpathbutton, 0, 1)

        # Setup the menus widget
        self.menus = menusWidget(self.doc)
        self.grid.addWidget(self.menus, 1, 0, 1, 1)

        # Setup outgoing filename
        self.outnamelabel = QLabel('Output File Name')
        self.outnamelineedit = QLineEdit()
        self.useincomingnamecheck = QCheckBox('Use highest run number?', self)
        self.grid.addWidget(self.outnamelabel, 2, 0)
        self.grid.addWidget(self.outnamelineedit, 2, 1)
        self.grid.addWidget(self.useincomingnamecheck, 2, 2)
        
        # Setup outgoing path (optional)
        self.outpathlineedit = QLineEdit()
        self.selectoutpathbutton = QPushButton('Select Out Directory', self)
        self.grid.addWidget(self.selectoutpathbutton, 3, 0)
        self.grid.addWidget(self.outpathlineedit, 3, 1)

        # Setup the doing things button
        self.doAddButton = QPushButton('Add!', self)
        self.grid.addWidget(self.doAddButton, 4, 2)

        # Do the layout
        self.setLayout(self.grid)


        ####################
        #
        # Connections to shared actions to be notified to the document
        #
        # These actions need to signal the Controller so as to trigger
        # other actions. Shared actions implemented in the abstract 
        # class include the Upload action, changes to post title and to
        # post content.
        # 
        ####################

        self.connect(self.pathlineedit, SIGNAL('editingFinished()'),
                                        self.viewSetPath)

        # Action on pressing directory selection button
        self.connect(self.selectpathbutton, 
                         SIGNAL('clicked()'),
                         self.selectDirectoryDialog)

        self.connect(self.menus, SIGNAL('sigViewRunMenuSelected'),
                                        self.viewSetRunlist)

        self.connect(self.outnamelineedit, SIGNAL('editingFinished()'),
                                           self.viewSetOutname)

        self.connect(self.useincomingnamecheck,
                          SIGNAL('stateChanged(int)'),
                          self.viewSetUseIncomingFilename)

        self.connect(self.selectoutpathbutton,
                          SIGNAL('clicked()'),
                          self.setOutpathDialog)

        self.connect(self.outpathlineedit, SIGNAL('editingFinished()'),
                                           self.viewSetOutpath)

        self.connect(self.doAddButton, SIGNAL('clicked()'),
                                       self.viewDoAddition)

         ####################
        #
        # Connections to signals notified by the document
        #
        # These actions need to signal the view so as to trigger
        # actions in the GUI. The main action is to update the
        # menus when the path is changed.
        # 
        ####################
            
        self.connect(self.doc, SIGNAL('sigDocPathSet'),
                               self.menus.init)

        self.connect(self.doc, SIGNAL('sigDocUseIncomingChanged'),
                               self.toggleOutnameLineedit)
        
    def selectDirectoryDialog(self):
        """Triggers file dialog to select directory for upload"""

        directory = QFileDialog.getExistingDirectory(self, 
                    'Open Directory',
                    self.doc.getPath())
        self.pathlineedit.setText(directory)
        self.doc.setPath(directory)

    def setDataDirectoryLineEdit(self, signal):
        """Method triggered when doc signals Post Title Changed

        First check whether is the same as current text so as to
        prevent race condition. If it is different (e.g. if set
        via script or macro, then change linedit to match. This
        method is connected to sigDocDataDirectoryChanged.
        """

        if self.doc.getPath() == self.pathlineedit.text():
            return
        else:
            self.pathlineedit.setText(self.doc.getPath()) 

    def setOutpathDialog(self):
        """Triggers file dialog to select directory for upload"""

        directory = QFileDialog.getExistingDirectory(self, 
                    'Open Directory',
                    self.doc.getPath())
        self.outpathlineedit.setText(directory)
        self.doc.setOutpath(directory)

    def setOutPathLineEdit(self, signal):
        """Method triggered when doc signals Post Title Changed

        First check whether is the same as current text so as to
        prevent race condition. If it is different (e.g. if set
        via script or macro, then change linedit to match. This
        method is connected to sigDocDataDirectoryChanged.
        """

        if self.doc.getOutpath() == self.outpathlineedit.text():
            return
        else:
            self.outpathlineedit.setText(self.doc.getOutpath()) 

##############################
#
# Setter methods for the view to modify the document
#
##############################

    def viewSetPath(self):
        self.doc.setPath(self.dirpathlineedit.text())

    def viewSetRunlist(self):
        logging.debug('addFileWidget: Menu activated. Runlist: ' +
                                str(self.menus.getRunList()))
        if self.menus.getRunList():
            self.doc.setRunlist(self.menus.getRunList())

    def viewSetOutname(self):
        self.doc.setOutname(self.outnamelineedit.text())

    def viewSetUseIncomingFilename(self, integer):
        logging.debug('addFileWidget: Checkbox activated: ' + str(integer))
        if integer == 0:
            self.doc.setUseIncomingFilename(False)
        elif integer == 2:
            self.doc.setUseIncomingFilename(True)
        else:
            raise TypeError('Checkbox should be sending 0 or 2')

    def viewSetOutpath(self):
        self.doc.setOutpath(self.outpathlineedit.text())

    def viewDoAddition(self):
        self.doc.addRuns()

##############################
#
# Slots for the view to respond to the document
#
##############################

    def activateMenus(self):
        self.menus.init()
        
    def toggleOutnameLineedit(self):
        if self.doc.getUseIncomingFilename():
            if self.outnamelineedit.isEnabled() == True:
                self.outnamelineedit.setEnabled(False)
                self.outnamelineedit.setText('')

        else:
            if self.outnamelineedit.isEnabled() == False:
                self.outnamelineedit.setEnabled(True)
                self.outnamelineedit.setText(self.doc.getOutname())
                self.outnamelineedit.setFocus()


def main(args):
    LOG_FILENAME = '/logging.out'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    app=QApplication(args)
    doc = addRawDoc()
    docview = addFileWidget(doc)
    docview.show()
    app.exec_()


if 1==0:
    main(sys.argv)

else:
    app=QApplication.instance()
    doc = addRawDoc()
    docview = addFileWidget(doc)
    docview.show()

    
   

    
