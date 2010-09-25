# SansReduce: A wrapping library for SANS data reduction in the Mantid
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

import logging
import sys
import os
import shutil
from PyQt4.QtCore import *

try:
    import SANSReduction
except ImportError: #If testing outside of Mantid use the test module instead
    import SANSReduction_for_testing_only as SANSReduction

# For testing outside of the Mantid environment
try:
    from mantidsimple import *
except ImportError:
    def LoadNexus(filename, wsname):
        pass
    def LoadRaw(filename, wsname):
        pass
    def LoadSampleDetailsFromRaw(wsname, filename):
        pass
    def UserPath(string):
        pass
    def MaskFile(string):
        pass

class AbstractScatteringRun(object):
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
        self.initWorkspace()
    
        if input:
            input = str(input)
            self.mungeNames(input)


    ###############
    # Init Methods#
    ###############
    def initRunnumber(self):
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
        """Routine to set the Run number

        Run number may include the modifier '-add' to indicate it is an
        added file. This can be left in the run number and will in principle
        be handled correctly through the code chain. TODO: This needs to be more
        thoroughly tested than it had been thus far.
        """

        logging.debug("SansReduce:setRunnumber: setto: " +
                        str(runno))
        try:
            assert type(runno) == str or type(runno) == QString

        except AssertionError:
            raise TypeError('Run number must be a string')

        self.runnumber = str(runno).rstrip('.nxs').rstrip('.raw')
        if '.' in runno and len(runno.split('.')) >1:
            self.setExt(runno.split('.')[1])

        self.runnumberToFilename()

    def getRunnumber(self):
        logging.debug("SansReduce:getRunnumber: returning: " + self.runnumber)
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

        holder = str(string).split('.')
        if len(holder) > 1 and (holder[-1] == 'nxs' or 
                                holder[-1] == 'raw'):
            self.setExt(holder[-1])
        self.filename = str(string).rstrip('.nxs').rstrip('.raw')

        self.filenameToRunnumber()

    def getFilename(self):
        logging.debug("SansReduceDoc:getFilename: returning: " +
                        self.filename)
        return self.filename

    def setPath(self, string):
        try:
            assert type(string) == str or type(string) == QString
        except AssertionError:
            raise TypeError('Path must be a string or Qstring')

        self.path = str(string)
        logging.debug("SansReduceDoc:setPath: setto: " + self.path)
        logging.debug("SansReduceDoc:setPath: getPath() returns " +
                      self.getPath())

    def getPath(self):
        logging.debug("SansReduceDoc:getPath: returning: " + self.path)
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
            self.mungeNames(input)

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
        
        Method  provides a way of making sure that filenames, run number, 
        path and extension are all consistent. Run numbers may include the
        '-add' modifier and filenames may not have run numbers at all in 
        some cases.
        """

        # If there is an input then try to deal with it
        if input:
            # If input is a full filename
            if input.startswith('SANS2D'):
                self.filename = str(input).rstrip('.nxs').rstrip('.raw')
                self.filenameToRunnumber()

            # If input is a run number with or without extension
            elif input.rstrip('.nxs').rstrip('.raw').rstrip('-add').isdigit():
                # setRunnumber will strip the filetype extension
                self.runnumber = input.rstrip('.nxs').rstrip('.raw')
                self.runnumberToFilename()
            else: pass

            # If input has a filetype extension then setExt
            if len(input.split('.')) > 1:
                # Using [-1] index means the routine is safe against people
                # including periods in the filename
                if input.split('.')[-1] == 'nxs' or input.split(
                    '.')[-1] == 'raw':
                    self.setExt(input.split('.')[-1])
            

    def filenameToRunnumber(self):
        """Convert filename to runnumber and populate

        If have a filename but not a run number then set the run number
        The filename is not guaranteed to have the filetype extension
        removed.
        """

        if self.runnumber:
            return
        else:
            self.runnumber = self.getFilename().lstrip('SANS2D0'
                                     ).rstrip('.nxs').rstrip('.raw')

    def runnumberToFilename(self):
        """Convert runnumber to filename and populate
        
        If have a run number but not a filename then set the filename
        self.runnumber is guaranteed not to have a filetype extension.
        This can cause problems if using filenames that actually are
        the runnumber rather than runnumber plus other information 
        (e.g. 3339.nxs rather than SANS2D00003339.nxs). Therefore the 
        currently set directory is checked for simpler versions of the 
        filename just in case. Routine tests for existence of the file
        in both cases and returns True if it exists and False if not.
        This is only a best efforts case and depends on the path being
        set correctly.
        """

        # Test whether a file exists with the filename set as runnumber
        self.filename = self.getRunnumber()
        if self._testFullPath():
            return True
        # If it doesn't convert runnumber to a standard SANS2D name
        else:
            filename_prefix = 'SANS2D'
            self.filename = filename_prefix + '0'*(
                            8-len(self.getRunnumber().rstrip('-add'))
                                      ) + self.getRunnumber()
            return self._testFullPath()


    def _buildFullPath(self):
        """Convenience method for constructing full path
        """

        logging.debug("SansReduceDoc:_buildFullPath: returning:" +
                      os.path.join(self.getPath(),
                                   self.getFilename() + '.' + self.getExt()))
        logging.debug("\nself.getPath(): " + self.getPath() + 
                      '\nself.getFilename(): ' + self.getFilename())
        return os.path.join(self.getPath(),
                            self.getFilename() + '.' + self.getExt())

    def _testFullPath(self):
        """Method to test whether a target file actually exists
        """

        if os.path.exists(self._buildFullPath()): return True
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
        AbstractScatteringRun.__init__(self, input)

    def _buildWSName(self):
        return (self.getRunnumber() + '_trans_' + self.getExt())

class DirectBeam(Trans):
    """Subclass of Trans to represent direct beam runs

    Direct beam runs are handled differently than transmissions and
    backgrounds in the underlying scripts so this class is simple a 
    convenience method for making that distinction.
    """

    def __init_(self, input = None):
        Trans.__init__(self, input)

    def _buildWSName(self):
        return (self.getRunnumber() + '_directbeam_' + self.getExt())

class AbstractSans(AbstractScatteringRun):
    """A class representing SANS measurements

    The AbstractSans Class is the core object for manipulating SANS data. It
    will be the primary reference point around which the rest of the 
    reduction process revolves. The abstract class provides the notion
    of an associated transmission run (instance of the Trans class)
    """

    def __init__(self, input = None, transrun = None):
        AbstractScatteringRun.__init__(self, input)
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
    data elements are provided by the earlier classes. Reductions
    can be initialised either we pre-existing SANS and TRANS objects
    or with run numbers or filenames to represent those objects.
    Subclasses should pass the relevant variables to the abstract
    class init methods or if this is not desired overwrite the relevant
    init methods.
    """

    def __init__(self, sansrun = None, bgdrun = None, directbeamrun = None,
                 sanstrans = None, bgdtrans = None, maskfile = None):
        self.initSansRun(sansrun, sanstrans)
        self.initBackgroundRun(bgdrun, bgdtrans)
        self.initDirectBeamRun(directbeamrun)
        self.initInstrument()
        self.initMaskfile(maskfile)
        self.initWavRangeLow()
        self.initWavRangeHigh()
        self.initDetector()
        self.initGravity()
        self.initVerbose()

        self.__instrumentlist = ['SANS2D', 'LOQ', 'ZOOM']
        self.__detectorlist = ['front-detector', 'rear-detector']



    ###############
    # Init Methods#
    ###############
    def initSansRun(self, sansrun, sanstrans):
        """Initialisation method for the SANS element of the reduction

        If a sansrun has been passed to the init method then check 
        whether it is a string or an AbstractSans object. If a str
        then initialise a new AbstractSans object, with trans if
        avaiable. If it is an AbstractSans object then set self.sans
        to be that object. Otherwise set self.sans to be None.
        """

        if sansrun:
            if type(sansrun) == str:
                self.sans = AbstractSans(sansrun, sanstrans)
            elif type(sansrun) == SansReduce.AbstractSans:
                self.sans = sansrun

        else:
            self.sans = AbstractSans()

    def initBackgroundRun(self, bgdrun, bgdtrans):
        """Initialisation method for the background for the reduction

        If a bgdrun has been passed to the init method then check 
        whether it is a string or an AbstractSans object. If a str
        then initialise a new AbstractSans object, with trans if
        available. If it is an AbstractSans object then set self.sans
        to be that object. Otherwise set self.background to be None.
        """

        if bgdrun:
            if type(bgdrun) == str:
                self.background = AbstractSans(bgdrun, bgdtrans)
            elif type(bgdrun) == SansReduce.AbstractSans:
                self.background = bgdrun

        else:
            self.background = AbstractSans()

    def initDirectBeamRun(self, directbeamrun):
        """Initialisation method for the direct beam tranmission

        If a directbeam has been passed to the init method then check 
        whether it is a string or an AbstractSans object. If a str
        then initialise a new Trans object. If it is a Trans object then 
        set self.directbeam to be that object. Otherwise set 
        self.directbeam to be None.
        """

        if directbeamrun:
            if type(directbeamrun) == str:
                self.directbeam = DirectBeam(directbeamrun)
            elif type(directbeamrun) == SansReduce.DirectBeam:
                self.directbeam = directbeamrun

            else:
                raise Warning("Direct beam needs to be of type 'DirectBeam'")

        else:
            self.directbeam = DirectBeam()

    def initInstrument(self):
        self.instrument = 'SANS2D'

    def initMaskfile(self, maskfile):
        self.maskfile = ''
        self.__maskfile_directory = ''
        self.__maskfile_filename = ''
        self.__maskfile_abspath = ''
        self.__maskfile_isabs = ''
        self.__maskfile_currentdirwhenset = ''

        if maskfile:
            self.setMaskfile(maskfile)

    def initWavRangeLow(self):
        self.wavrangelow = 2.0

    def initWavRangeHigh(self):
        self.wavrangehigh = 14.0
    
    def initDetector(self):
        self.detector = 'rear-detector'

    def initGravity(self):
        self.gravity = True

    def initVerbose(self):
        self.verbose = False

    #####################
    #Getters and Setters#
    #####################
    def setSansRun(self, runnumber):
        """Method for setting the SANS run number
        """

        logging.debug("SansReduce:setSansRun: setting to: " +
                      str(runnumber))
        # If there is an input make sure it is a string or QString
        if runnumber:
            try:
                assert type(runnumber) == str or type(runnumber) == QString
            except AssertionError:
                raise TypeError('Run identifier must be a string or QString')

        self.sans.setRunnumber(str(runnumber))

    def getSansRun(self):
        return self.sans

    def setSansTrans(self, transrun):
        """Convenience method for setting the transmission run"""

        self.sans.trans.setRunnumber(transrun)

    def getSansTrans(self):
        return self.sans.trans
        
    def setBackgroundRun(self, runnumber):
        """Method for setting the background run
        """

        # If there is an input make sure it is a string or QString
        if runnumber:
            try:
                assert type(runnumber) == str or type(runnumber) == QString
            except AssertionError:
                raise TypeError('Run identifier must be a string or QString')

        self.background.setRunnumber(runnumber)

    def getBackgroundRun(self):
        return self.background

    def setBackgroundTrans(self, runnumber):
        """Convenience method for setting the background transmission"""
        self.background.trans.setRunnumber(runnumber)

    def getBackgroundTrans(self):
        return self.background.trans

    def setDirectBeam(self, runnumber):
        """Method for setting and initialising the directbeam run
        """

        # If there is an input make sure it is a string or QString
        if runnumber:
            try:
                assert type(runnumber) == str or type(runnumber) == QString
            except AssertionError:
                raise TypeError('Run identifier must be a string or QString')
        self.directbeam.setRunnumber(runnumber)

    def getDirectBeam(self):
        return self.directbeam

    def setPathForAllRuns(self, path):
        """A convenience method to set paths to all runs to the same value
        """
        
        path = str(path) # In case it is a QString or other object
        logging.debug("Doc:setPathForAllRuns: setto: " + path)
        try:
            assert os.path.isdir(path)
        except AssertionError:
            raise ValueError('This does not appear to be a valid path')

        self.getSansRun().setPath(path)
        self.getBackgroundRun().setPath(path)
        self.getSansTrans().setPath(path)
        self.getBackgroundTrans().setPath(path)
        self.getDirectBeam().setPath(path)
        logging.debug("Doc:setPathForAllRuns: setto: " + path)
        logging.debug(self.getSansRun().getPath())

    def setInstrument(self, instrument):
        """Function for setting the instrument

        This function wraps the various instrument definition functions in
        SANSReduction.py. The input is first tested against acceptable values
        and then the appropriate lower level function is called.
        """

        instrument = str(instrument)
        try:
            assert type(instrument) == str
            assert instrument in self.__instrumentlist
        except AssertionError:
            raise TypeError('Instrument must be "SANS2D", "LOQ", or "ZOOM"')

        if instrument == self.__instrumentlist[0]:
            self.instrument = self.__instrumentlist[0]
            SANSReduction.SANS2D()

        if instrument == self.__instrumentlist[1]:
            self.instrument = self.__instrumentlist[1]
            SANSReduction.LOQ()

        if instrument == self.__instrumentlist[2]:
            self.instrument = self.__instrumentlist[2]
            raise NotImplementedError(self.__instrumentlist[2] + 
                                         " doesn't exist yet!")

        
    def getInstrument(self):
        return self.instrument

    def setDetector(self, detector):
        """Function for setting the detector

        TODO Do a sanity check between instrument and detector.
        """

        detector = str(detector)
        try:
            assert type(detector) == str
            assert detector in self.__detectorlist
        except AssertionError:
            raise TypeError('Instrument must be "front-detector" or "rear-detector"')

        self.detector = detector
        SANSReduction.Detector(detector)
        
    def getDetector(self):
        return self.instrument

    def setMaskfile(self, path):
        """Method for setting the Mask File
        
        The method currently takes a path and will attempt to determine 
        whether the file exists and whether the path is relative or absolute. 
        Aspects of the path are then placed in a number of private variables. 
        The lower level functions UserPath(path) and MaskFile(filename) are 
        then called.
        """

        try:
            assert type(path) == str or type(path) == QString
        except AssertionError:
            raise TypeError('Path must be a string or QString')

        path = str(path)
        try:
            assert os.path.exists(path)
        except AssertionError:
            raise ValueError('Path to Maskfile is incorrect or broken!')
         
        self.maskfile = path

        self.__maskfile_directory, self.__maskfile_filename = os.path.split(self.maskfile)
        self.__maskfile_abspath = os.path.abspath(path)
        self.__maskfile_isabs = os.path.isabs(path)
        self.__maskfile_currentdirwhenset = os.path.abspath('')

        SANSReduction.UserPath(self.__maskfile_directory)
        SANSReduction.MaskFile(self.__maskfile_filename)

    def getMaskfile(self, forceabs = False):
        """Method for returning the Maskfile path

        The method will aim to provide a relative path to the Maskfile but will
        return an absolute path if forceabs is set to True. The method raises a
        ValueError if the maskfile isn't where it should be.
        """

        if forceabs == False:
            if os.path.isfile(self.maskfile):
                return self.maskfile

            elif os.path.isfile(self.__maskfile_abspath):
                self.setMaskfile(os.path.relpath(self.__maskfile_abspath))
                return self.maskfile

            else:
                raise ValueError("I can't find the Maskfile any more")

        elif forceabs == True:
            if os.path.isfile(self.maskfile):
                return os.path.abspath(self.maskfile)

            elif os.path.isfile(self.__maskfile_abspath):
                self.setMaskfile(os.path.relpath(self.__maskfile_abspath))
                return self.maskfile

            else:
                raise ValueError("I can't find the Maskfile any more")
                               
        else:
            raise TypeError("Forceabs must be True or False")

                
    def setWavRangeLow(self, wavelength):
        """Function to set lowest wavelength for reduction

        Currently there is not sanity testing for these values. Integers
        are converted to floats.
        """
        
        # Convert to float if incoming is a string or QString
        if (type(wavelength)) == str or (type(wavelength) == QString):
            wavelength = float(str(wavelength))
        try:
            assert type(wavelength) == float or type(wavelength) == int
        except AssertionError:
            raise TypeError("Wavelength must be a float or int")

        self.wavrangelow = float(wavelength)

    def getWavRangeLow(self):
        return self.wavrangelow

    def setWavRangeHigh(self, wavelength):
        """Function to set highest wavelength for reduction

        Currently there is not sanity testing for these values. Integers
        are converted to floats.
        """

        # Convert to float if incoming is a string or QString
        if (type(wavelength) == str) or (type(wavelength) == QString):
            wavelength = float(str(wavelength))  
        try:
            assert type(wavelength) == float or type(wavelength) == int
        except AssertionError:
            raise TypeError("Wavelength must be a float or int")

        self.wavrangehigh = float(wavelength)

    def getWavRangeHigh(self):
        return self.wavrangehigh

    def setGravity(self, boolean):
        """Function for setting whether to take account of gravity. 

        Default value is True. The setter calls the lower level method which sets
        the global variable for reduction process.
        """

        try:
            assert type(boolean) == bool
        except AssertionError:
            raise TypeError("Gravity must be set to True or False")

        SANSReduction.Gravity(boolean)
        self.gravity = boolean

    def getGravity(self):
        """Function returns whether gravity is being taken into account

        Checks whether the local internal variable is set to the same thing
        as the lower level (global) variable. If not it will return the global
        and reset the local variable.
        """

        if self.gravity == SANSReduction.GRAVITY:
            return self.gravity
        else:
            self.setGravity(SANSReduction.GRAVITY)
            return self.gravity

    def setVerbose(self, boolean):
        """Function for setting Verbose flag. 

        Default value is False. The setter calls the lower level method which sets
        the global variable for reduction process.
        """

        try:
            assert type(boolean) == bool
        except AssertionError:
            raise TypeError("Verbose must be set to True or False")

        SANSReduction.SetVerboseMode(boolean)
        self.verbose = boolean

    def getVerbose(self):
        """Function returns whether gravity is being taken into account

        Checks whether the local internal variable is set to the same thing
        as the lower level (global) variable. If not it will return the global
        and reset the local variable.
        """

        if self.verbose == SANSReduction._VERBOSE_:
            return self.verbose
        else:
            self.setVerbose(SANSReduction._VERBOSE_)
            return self.verbose
    

        
class Standard1DReductionSANS2DRearDetector(AbstractReduction):
    """Class representing a standard 1D reduction
    """

    def __init__(self, sansrun = None, bgdrun = None, directbeamrun = None,
                 sanstrans = None, bgdtrans = None, maskfile = None):
        AbstractReduction.__init__(self, sansrun, 
                                   bgdrun, directbeamrun, 
                                   sanstrans, bgdtrans, maskfile)
        self.setInstrument('SANS2D')
        self.setDetector('rear-detector')
        self.setGravity(True)
        self.setVerbose(False)
            

    #######################
    #The reduction routine#
    #######################

    def doReduction(self):
        """Method for actually doing the reduction

        The method first checks that all the required information is available
        and set, and that pointers correspond to real files. Then all the 
        required lower level variables are set and the reduction is run.
        In the current version nothing is plotted.
        """

        # Check required information is available
        if not self.getSansRun().getRunnumber():
            raise Warning('No SANS run set')
            return False

        if not self.getSansTrans().getRunnumber():
            raise Warning('No SANS transmission run number set')
            return False

        if not self.getBackgroundRun().getRunnumber():
            raise Warning('No background run number set')
            return False

        if not self.getBackgroundTrans().getRunnumber():
            raise Warning('No background transmission run number set')
            return False

        if not self.getDirectBeam().getRunnumber():
            raise Warning('No direct beam run number set')
            return False

        if not self.getSansRun().getFilename():
            self.getSansRun().mungeNames()

        if not self.getSansTrans().getFilename():
            self.getSansTrans().mungeNames()

        if not self.getBackgroundRun().getFilename():
            self.getBackgroundRun().mungeNames()

        if not self.getBackgroundTrans().getFilename():
            self.getBackgroundTrans().mungeNames()

        if not self.getDirectBeam().getFilename():
            self.getDirectBeam().mungeNames()

        if not self.getInstrument():
            raise Warning('No instrument has been set')
            return False

        if not self.getMaskfile():
            raise Warning('No maskfile path is available')
            return False

        if not self.getWavRangeLow():
            raise Warning('Lowest wavelength to reduce not set')
            return False

        if not self.getWavRangeHigh():
            raise Warning('Highest wavelength to reduce not set')
            return False
    
        logging.debug("\n\nSansReduce: Reduction done with:\nSANS RN:" +
                          self.getSansRun().getRunnumber() +
                          "\nSANS Trans:" + 
                          self.getSansTrans().getRunnumber() +
                          "\nBackground:" +
                          self.getBackgroundRun().getRunnumber() +
                          "\nBgd Trans:" + 
                          self.getBackgroundTrans().getRunnumber()+
                          "\n\n")
     
        # Check the files actually exist
        try:
            assert self.getSansRun()._testFullPath(), \
                                      'SANS file not where expected: ' + \
                                      self.getSansRun()._buildFullPath()
            assert self.getSansTrans()._testFullPath(),\
                                      'Sample trans file not where expected'
            assert self.getBackgroundRun()._testFullPath(), \
                                      'Background file not where expected'
            assert self.getBackgroundTrans()._testFullPath(), \
                                      'Background trans file not where expected'
            assert self.getDirectBeam()._testFullPath(),\
                                      'Direct Beam file not where expected'
            assert os.path.isfile(self.getMaskfile()), \
                                      'Maskfile is not where expected'

        except AssertionError, e:
            raise Warning(e)
            return False

        # Now actually do the setting of appropriate global variables etc.
        # We set DataPath for each sample to protect against the case where
        # files are in different directories. The way that the SANSReduction
        # works with AssignSample/Can calling _assignerHelper, which in turn
        # references the global variable DATA_PATH, set by 
        # SANSReduction.DataPath(path) means we should be ok. If all paths are
        # the same I'm just wasting time here, but not too much.
        #
        # Setting the sample
        SANSReduction.DataPath(self.getSansRun().getPath())
        SANSReduction.AssignSample(self.getSansRun().getRunnumber() + 
                                   '.' + self.getSansRun().getExt())

        # Setting the sample transmision
        SANSReduction.DataPath(self.getSansRun().trans.getPath())
        SANSReduction.TransmissionSample(self.getSansRun().trans.getRunnumber()
                                         + '.' + 
                                         self.getSansRun().trans.getExt(),
                                         self.getDirectBeam().getRunnumber() +
                                         '.' + self.getDirectBeam().getExt())

        # Setting the background
        SANSReduction.DataPath(self.getBackgroundRun().getPath())
        SANSReduction.AssignCan(self.getBackgroundRun().getRunnumber() +
                                 '.' + self.getBackgroundRun().getExt())

        # Setting the background transmision
        SANSReduction.DataPath(self.getBackgroundRun().trans.getPath())
        SANSReduction.TransmissionCan(self.getBackgroundRun().trans.getRunnumber()
                                         + '.' + 
                                         self.getBackgroundRun().trans.getExt(),
                                         self.getDirectBeam().getRunnumber() +
                                         '.' + self.getDirectBeam().getExt())
        
        # Set the path to the Maskfile
        SANSReduction.UserPath(os.path.dirname(self.getMaskfile()))
        SANSReduction.MaskFile(os.path.basename(self.getMaskfile()))

        # Find the beam center ###DO I REALLY NEED TO DO THIS? ### Not if the maskfile is correct
        # SANSReduction.FindBeamCentre(50., 170., 2)

        # DO THE REDUCTION!
        self.reducedworkspace = SANSReduction.WavRangeReduction(self.getWavRangeLow(),
                                                                self.getWavRangeHigh())

        return self.reducedworkspace
 
