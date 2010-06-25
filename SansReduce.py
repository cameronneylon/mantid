# SansReduce: A GUI utility for SANS 1D data reduction in the Mantid
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

try:
    from mantidsimple import *
except ImportError:
    pass

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import logging
import sys
import os
import shutil

class AbstractScatteringRun:
    """An abstract class to represent SANS runs

    The abstract class will provide internal data elements for run
    number, filename, and translation between them. It also provides
    the generic loading and saving methods.

    self.runnumber is the shortened run number, generally without any
    leading or trailing zeros. It may or may not be set with a file
    extension. If it is it will be stripped.

    self.filename is intended to hold the full filename (without 
    extension) without any path elements. Path elements and extension
    will be stripped and placed in the appropriate data elements if
    given.

    self.path is the full path to the directory holding the file. It 
    may be relative or absolute but no guarantees are made on the 
    initialised home directory.

    self.workspace is the reference to the workspace in which the run
    is placed. This will generally be named after the run number or
    filename with some additional information (provided by the method
    classSpecificLoadFunctions, which should be re-implemented for each
    sub-class).
    """

    def __init__(self, input=None):
        self.initRunnumber()
        self.initFilename()
        self.initPath()
        self.initExt()
        self.initWorkspace
    
        if input:
            self.mungeNames(input)

    ###############
    # Init Methods#
    ###############
    def initRunnmber(self):
        self.runnumber = ''

    def initFilename(self):
        self.filename = ''

    def initPath(self):
        self.path = ''

    def initExt(self):
        self.ext = ''

    def initWorkspace(self):
        self.workspace = None

    #####################
    #Getters and Setters#
    #####################
    def setRunnumber(self, runno):
        try:
            assert type(runno) == str or type(runno) == QString

        except AssertionError:
            raise TypeError('Run number must be a string')

        self.runnumber = runno.rstrip('.nxs').rstrip('.raw')
        if runno.split('.')[1] != None:
            self.setExt(runno.split('.')[1])

    def getRunnumber(self):
        return self.runnumber

    def setExt(self, string):
        try:
            assert type(string) == str or type(string) == QString
            assert string == 'nxs' or string == 'raw'

        except AssertionError:
            raise TypeError("Ext must be one of 'nxs' or 'raw'")

        self.ext = str(string)

    def getExt(self):
        return self.ext

    def setFilename(self, string):
        try:
            assert type(string) == str or type(string) == QString
        except AssertionError:
            raise TypeError('Filename must be a string or Qstring')

        self.filename = str(string)

    def getFilename(self):
        return self.filename

    def setPath(self, string):
        try:
            assert type(string) == str or type(string) == QString
        except AssertionError:
            raise TypeError('Path must be a string or Qstring')

        self.path = str(string)

    def getPath(self):
        return self.path

    def setWorkspace(self, string):
        """Method for setting the workspace relating to a run

        The setter method takes the _name_ of the workspace as given
        rather than the workspace itself.

        TODO Enable the setter method to take both name and WS
        """

        try:
            assert type(string) == str or type(string) == QString
        except AssertionError:
            raise TypeError('Workspace name must be a string or Qstring')

        self.workspace = mtd[str(string)]

    def getWorkspace(self):
        return self.workspace

    def getWorkspaceName(self):
        return self.workspace.getName()


    ###################
    #Loaders and tools#
    ###################
    def load(self, input = None):
        """Method to load a file to a new workspace

        This shouldn't actually be used in practice because the 
        reduction routines do the actual loading. This is provided
        as a convenience.

        The method will first try to use all available internal data
        elements to construct a complete path. Failing this it will
        attempt a range of possible values based on the available lists
        """

        if input:
            self.mungenames(input)

        fullfilename = os.path.join(self.getPath(), 
                                     self.getFilename() + self.getExt())
        if self._testFullPath():
            if self.getExt() == 'nxs':
                LoadNexus(self._buildFullPath(),
                          self._buildWSName())
                self.setWorkspace(self._buildWSName())
            elif self.getExt() == 'raw':
                LoadRaw(self._buildFullPath(),
                        self._buildWSName())
                self.setWorkspace(self._buildWSName())
                LoadSampleDetailsFromRaw(self.getWorkspaceName(),
                                         self._buildFullPath())

    def mungeNames(self, input = None):
        """Method for converting run numbers to filenames and vice versa
        
        Method shouldn't in practice be required but provides a clean 
        way of making sure that filenames, run number, path and 
        extension are all consistent.
        """

        filename_prefix = SANS2D

        # If there is an input then try to deal with it
        if input:
            if input.startswith('SANS2D'):
                self.setFilename(input)
            elif input.rstrip('.nxs').rstrip('raw').isdigit():
                # setRunnumber will strip the filetype extension
                self.setRunnumber(input)
            else: pass

            # If input has a filetype extension then setExt
            if input.split('.')[1] == 'nxs' or input.split('.')[1] == 'raw':
                self.setExt(input.split('.')[1])
            

        # If have a filename but not a run number then set the run number
        # The filename is not guaranteed to have the filetype extension
        # removed
        if self.getFilename() and not self.getRunnumber():
            self.setRunnumber(self.getFilename().
                              lstrip('SANS2D0').rstrip('.nxs').rstrip('.raw'))


        # If have a run number but not a filename then set the filename
        # self.Runnumber is guaranteed not to have a filetype extension
        if self.getRunnumber() and not self.getFilename():
            self.setFilename(filename_prefix + 
                            '0'*(8-len(self.getRunnumber())) +
                             self.getRunnumber())        

    def _buildFullPath(self):
        """Convenience method for constructing full path
        """
        return os.path.join(self.getPath(),
                            self.getFilename() + '.' + self.getExt())

    def _testFullPath(self):
        """Method to test whether a target file actually exists
        """

        if os.path.exists(self._buildFullPath): return True
        else: return False
       
    def _buildWSName(self):
        """Template method for building a standard Workspace name

        This method should be overwritten in each subclass to provide
        individualised means of naming loaded workspaced.
        """
        pass
            
class Trans(AbstractScatteringRun):
    """A class to represent transmission measurements
    """

    def __init_(self, input = None):
        abstractScatteringRun.__init__(input)

    def _buildWSName(self):
        return (self.getRunnumber() + '_trans_' + self.getExt())

class DirectBeam(Trans):
    """Subclass of Trans to represent direct beam runs

    Direct beam runs are handled differently than transmissions and
    backgrounds in the underlying scripts so this class is simple a 
    convenience method for making that distinction.
    """

    def __init_(self, input = None):
        abstractScatteringRun.__init__(input)

    def _buildWSName(self):
        return (self.getRunnumber() + '_directbeam_' + self.getExt())

class AbstractSans(AbstractScatteringRun):
    """A class representing SANS measurements

    The AbstractSans Class is the core object for manipulating SANS data. It
    will be the primary reference point around which the rest of the 
    reduction process revolves. The abstract class provides the notion
    of an associated transmission run (instance of the Trans class)
    """

    def __init_(self, input = None, transrun = None):
        abstractScatteringRun.__init__(input)
        self.initTrans(transrun)

    def initTrans(self, transrun):
        """Initialise an associated transmission run for the SANS run
        """
        self.trans = Trans(transrun)

    def _buildWSName(self):
        return (self.getRunnumber() + '_sans_' + self.getExt())
    


class AbstractReduction:
    """An abstract class representing reduction processes

    The abstract class provides the internal data elements for
    SANS, TRANS, Background, and direct beam runs. These internal
    data elements are provided by the earlier classes.
    """

    def __init__(self):
        pass

class Standard1DReduction(AbstractReduction):
    """Class representing a standard 1D reduction
    """

    def __init__(self):
        pass
