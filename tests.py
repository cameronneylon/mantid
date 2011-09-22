# MantidTests: Tests and testing framework for the Mantid utilities
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

import unittest
import os
import SansReduce
import SansReduceGui

# Tests for SansReduce.py
# 
# Most of these tests are intended to be able to run outside of the
# Mantid environment for convenience. Clearly those that actually
# load or write data, or manipulate workspaces will not. These are
# not protected outside of Mantid so will fail visibly in tests run
# outside of Mantid

class SetupSansReduceTestCase(unittest.TestCase):
    """A shared set up and tear down class for the tests
    """

    def setUp(self):
        self.testfilename = 'SANS2D00003325'
        self.testext = ['nxs', 'raw']
        self.testrunno = '3325'
        self.testpath = 'test_data'
        self.testfullrelativepath = os.path.join(self.testpath, 
                                                 self.testfilename +
                                                 '.' + self.testext[1])
        self.testint = 1
        self.testfloat = 1.4

    def tearDown(self):
        self.testfilename = None
        self.testext = None
        self.testrunno = None
        self.testpath = None

class TestCreationScatteringObjects(unittest.TestCase):
    """Testing the setup of the scattering objects"""

    def setUp(self):
        self.abstractscattering = SansReduce.AbstractScatteringRun()
        self.trans = SansReduce.Trans()
        self.directbeam = SansReduce.DirectBeam()
        self.abstractsans = SansReduce.AbstractSans()

    def tearDown(self):
        self.abstractscattering.dispose()
        self.trans.dispose()
        self.directbeam.dispose()
        self.abstractsans.dispose()

class TestAbstractScatteringGettersSetters(SetupSansReduceTestCase):
    """Test the getters and setters of the abstract scattering class
    """

    def testEmptySetup(self):
        """Testing for correct setup and getters and setters behaving
        """

        self.scattering = SansReduce.AbstractScatteringRun()
        #TODO Get the class name clearly reported for each type

        # Testing that the scattering object is initialised correctly
        self.assertEqual(self.scattering.getRunnumber(),  '')
        self.assertEqual(self.scattering.getFilename(), '')
        self.assertEqual(self.scattering.getExt(), '')
        self.assertEqual(self.scattering.getWorkspace(), None)

        # Test setters work and don't raise errors with correct type
        # and that the getters return the expected value
        self.scattering.setRunnumber(self.testrunno)
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        for ext in self.testext:
            self.scattering.setExt(ext)
            self.assertEqual(self.scattering.getExt(), ext)
        self.scattering.setFilename(self.testfilename)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.scattering.setPath(self.testpath)
        self.assertEqual(self.scattering.getPath(), self.testpath)

        # Test that Type errors raised when set with wrong type
        self.assertRaises(TypeError, 
                          self.scattering.setRunnumber, self.testint)
        self.assertRaises(TypeError,
                          self.scattering.setExt, self.testint)
        self.assertRaises(TypeError,
                          self.scattering.setExt, 'wrong extension')
        self.assertRaises(TypeError,
                          self.scattering.setFilename, self.testint)
        self.assertRaises(TypeError,
                          self.scattering.setPath, self.testint)

        # Do the cleanup
        self.scattering.__init__()
        self.scattering = None

    def testExtensionHandling(self):
        """Tests of the set routines to handle extensions properly
        """

        self.scattering = SansReduce.AbstractScatteringRun()
        
        # Set runno with an extension: Run number and extension should
        # then be correct
        self.scattering.setRunnumber(self.testrunno + '.' + self.testext[0])
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getExt(), self.testext[0])
        self.scattering.__init__()

        # Set a filename with an extension: Filename and extension should 
        # both then be set correctly
        self.scattering.setFilename(self.testfilename + '.' + self.testext[1])
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.assertEqual(self.scattering.getExt(), self.testext[1])

    def testMungenames(self):
        """Test methods for the mungenames function

        Mungenames is intended to handle the creation of required names
        where only part of the information is available.
        """

        self.scattering = SansReduce.AbstractScatteringRun()

        # Set a filename and then use the name munger
        self.scattering.setFilename(self.testfilename)
        self.scattering.mungeNames()
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.scattering.__init__()

        # Set a runnumber and then check the name
        self.scattering.setRunnumber(self.testrunno)
        self.scattering.mungeNames()
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.scattering.__init__()

    def testAbstractScatteringSetupWithInput(self):
        """Test methods that pass input to the generator
        """

        # Test creation of a an abstract scattering run with a clean runno
        self.scattering = SansReduce.AbstractScatteringRun(self.testrunno)
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.scattering.__init__()

        # Test creation of absScat with runno with extension
        self.scattering = SansReduce.AbstractScatteringRun(self.testrunno +
                                                           '.' +
                                                           self.testext[0])
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.assertEqual(self.scattering.getExt(), self.testext[0])

        # Test creation of absScat with a clean filename
        self.scattering = SansReduce.AbstractScatteringRun(self.testfilename)
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.scattering.__init__()

        # Test creation of absScat with runno with extension
        self.scattering = SansReduce.AbstractScatteringRun(self.testfilename +
                                                           '.' +
                                                           self.testext[1])
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.assertEqual(self.scattering.getExt(), self.testext[1])
        

    def testSubclassSetupWithInput(self):
        """Test that all the subclasses are correctly created with input
        """

        # Testing Trans
        self.scattering = SansReduce.Trans(self.testrunno)
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.scattering.__init__()

        # Testing Trans with extension
        self.scattering = SansReduce.Trans(self.testrunno + '.' + 
                                           self.testext[1])
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.assertEqual(self.scattering.getExt(), self.testext[1])
        self.scattering.__init__()

        # Testing Direct Beam
        self.scattering = SansReduce.DirectBeam(self.testrunno)
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.scattering.__init__()

        # Testing Abstract Sans
        self.scattering = SansReduce.AbstractSans(self.testrunno)
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.scattering.__init__()
        # Here we test that the trans run is also created
        self.scattering = SansReduce.AbstractSans(self.testrunno,
                                                  self.testrunno)
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.getFilename(), self.testfilename)
        self.assertEqual(self.scattering.trans.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering.trans.getFilename(), self.testfilename)
        self.scattering.__init__()

    def testPrivateMethods(self):
        """Tests for the private methods
        """

        # Test that for AbstractScattering _buildWS name does nothing
        # and that _buildFullPath and _testFullPath do what is expected
        self.scattering = SansReduce.AbstractScatteringRun(self.testrunno)
        self.scattering.setPath(self.testpath)
        self.scattering.setExt(self.testext[1])

        self.assertEqual(self.scattering._buildFullPath(), 
                         self.testfullrelativepath)
        self.failUnless(os.path.exists(self.scattering._buildFullPath()))
        self.assertEqual(self.scattering._testFullPath(), True)

        # Break the path name so it is wrong and then check that _testFullPath
        # returns False. This relies on not changing filenames in the test_data 
        # directory!
        self.scattering.setFilename('SANS2D00000001') # file should not exist
        self.assertEqual(self.scattering._testFullPath(), False)

        # Test that _buildWSName returns nothing
        self.assertEqual(self.scattering._buildWSName(), None)

        self.scattering.__init__()

    def testSubclass_buildWSNameMethods(self):
        """Test for each of the subclass _buildWSName functions
        """

        # Testing Trans _buildWSName
        self.scattering = SansReduce.Trans(self.testrunno + '.' + 
                                           self.testext[1])
        self.assertEqual(self.scattering.getRunnumber(), self.testrunno)
        self.assertEqual(self.scattering._buildWSName(),
                         self.testrunno + '_trans_' + self.testext[1])
        self.scattering.__init__()

        # Testing DirectBeam _buildWSName
        self.scattering = SansReduce.DirectBeam(self.testrunno + '.' +
                                                self.testext[0])
        self.assertEqual(self.scattering._buildWSName(),
                         self.testrunno + '_directbeam_' + self.testext[0])
        self.scattering.__init__()

        # Testing Abstract Sans _buildWSName
        self.scattering = SansReduce.AbstractSans(self.testrunno + '.' +
                                                  self.testext[1])
        self.assertEqual(self.scattering._buildWSName(),
                         self.testrunno + '_sans_' + self.testext[1])
        self.scattering.__init__()


class InitialAbstractReductionTests(unittest.TestCase):


    def testSansRunSetup(self):
        self.reduction = SansReduce.AbstractReduction()
        # Test setting with run numbers for Sans and Trans
        self.reduction.initSansRun('3326.nxs', '3325.nxs')
        self.assertEqual(self.reduction.getSansRun().getRunnumber(), '3326')
        self.assertEqual(self.reduction.getSansRun().trans.getRunnumber(),
                         '3325')

    def testReductionSetupWithRunnumbers(self):
        self.reduction = SansReduce.AbstractReduction(
                     '3333.nxs', # Sans run
                     '3325.nxs', # Bgd run
                     '3332.nxs', # direct beam
                     '3328.nxs', # SANS transmission
                     '3331.nxs') # Bgd transmission

        self.assertEqual(self.reduction.getSansRun().getRunnumber(), '3333')
        self.assertEqual(self.reduction.getSansRun().trans.getRunnumber(), '3328')
        self.assertEqual(self.reduction.getSansRun().getExt(), 'nxs')
        self.assertEqual(self.reduction.getDirectBeam().getRunnumber(), '3332')
        self.assertEqual(self.reduction.getDirectBeam().getFilename(), 
                         'SANS2D00003332')

        self.reduction.getSansRun().setPath('test_data/')
        self.assertEqual(self.reduction.getSansRun()._testFullPath(), True)

    def testMaskfile(self):
        self.reduction = SansReduce.AbstractReduction()
        self.reduction.setMaskfile('test_data/MASKSANS2D_095B.txt')
        self.assertEqual(self.reduction.getMaskfile(),
                         'test_data/MASKSANS2D_095B.txt')
        self.assertEqual(self.reduction.getMaskfile(forceabs=True),
    '/Users/Cameron/Documents/Python/mantid/test_data/MASKSANS2D_095B.txt')

    def testWaveRanges(self):
        """Test for setters and getters of the WavRange variables
        """

        self.reduction = SansReduce.AbstractReduction()
        self.reduction.setWavRangeLow(3)
        self.assertEqual(self.reduction.getWavRangeLow(), 3.0)
        self.reduction.setWavRangeLow(3.4)
        self.assertEqual(self.reduction.getWavRangeLow(), 3.4)
        self.reduction.setWavRangeLow('3.5')
        self.assertEqual(self.reduction.getWavRangeLow(), 3.5)
        self.assertRaises(TypeError, self.reduction.setWavRangeLow, True)

        self.reduction = SansReduce.AbstractReduction()
        self.reduction.setWavRangeHigh(3)
        self.assertEqual(self.reduction.getWavRangeHigh(), 3.0)
        self.reduction.setWavRangeHigh(3.4)
        self.assertEqual(self.reduction.getWavRangeHigh(), 3.4)
        self.reduction.setWavRangeHigh('3.5')
        self.assertEqual(self.reduction.getWavRangeHigh(), 3.5)
        self.assertRaises(TypeError, self.reduction.setWavRangeHigh, True)

    def testGravity(self):
        """Quick test that gravity can be set and got"""

        self.reduction = SansReduce.AbstractReduction()
        self.reduction.setGravity(True)
        self.assertEqual(self.reduction.getGravity(), True)

        self.reduction = SansReduce.AbstractReduction()
        self.reduction.setGravity(False)
        self.assertEqual(self.reduction.getGravity(), False)

        self.assertRaises(TypeError, self.reduction.setGravity, 3)

    def testVerbose(self):
        """Quick test that verbose can be set and got"""

        self.reduction = SansReduce.AbstractReduction()
        self.reduction.setVerbose(True)
        self.assertEqual(self.reduction.getVerbose(), True)

        self.reduction = SansReduce.AbstractReduction()
        self.reduction.setVerbose(False)
        self.assertEqual(self.reduction.getVerbose(), False)

        self.assertRaises(TypeError, self.reduction.setVerbose, 3)

    def testReduction(self):
        """Test of reduction process and error raising
        """
        self.reduction = SansReduce.Standard1DReductionSANS2DRearDetector()

        self.assertRaises(Warning, self.reduction.doReduction)
        self.reduction.setSansRun('3333.nxs')
        self.assertRaises(Warning, self.reduction.doReduction)
        self.reduction.setBackgroundRun( '3325.raw')
        self.assertRaises(Warning, self.reduction.doReduction)
        self.reduction.setDirectBeam('3332.raw')
        self.assertRaises(Warning, self.reduction.doReduction)
        self.reduction.setSansTrans('3328.nxs')
        self.assertRaises(Warning, self.reduction.doReduction)
        self.reduction.setBackgroundTrans('3331.nxs')
        self.assertRaises(ValueError, self.reduction.doReduction)
        self.reduction.setMaskfile('test_data/MASKSANS2d_095B.txt')
        self.assertRaises(Warning, self.reduction.doReduction)
        self.reduction.setPathForAllRuns('test_data/')
        self.reduction.doReduction()

class SansReduceGuiDocTest(unittest.TestCase):
    """Test Class for Getters and Setters in SansReduceGuiDoc"""

    def setUp(self):
        """Set up some standard objects and cases"""

        self.testdoc = SansReduceGui.SansReduceDoc()

        
    def testInit(self):
        """Test the initialised state of the Doc"""
        
        self.assertEqual(self.testdoc.inPath, SansReduceGui.DEFAULT_IN_PATH)
        self.assertEqual(self.testdoc.maskfile, '')
        self.assertEqual(self.testdoc.directbeam, '')
        self.assertEqual(self.testdoc.showRawInMenus, True)
        self.assertEqual(self.testdoc.showNexusInMenus, False)
        self.assertEqual(self.testdoc.outputLOQ, False)
        self.assertEqual(self.testdoc.outputCanSAS, True)
        self.assertEqual(self.testdoc.useRunnumberForOutput, True)
        self.assertEqual(self.testdoc.blog, False)
        self.assertEqual(self.testdoc.queue, False)
        self.assertEqual(self.testdoc.reductionQueue, [])
        self.assertEqual(self.testdoc.queueViewVisible, False)
        self.assertEqual(self.testdoc.outPath, '')
        self.assertEqual(self.testdoc._inPathFileList, '')

        # Not currently testing blog variables because these will change

    def testGetAndSetCurrentReduction(self):
        """Test that getters and setters behave themselves

        These methods test that the getters and setters that relate to
        the currentReduction internal object are behaving correctly. The
        major issues are the directbeam and maskfile objects that are
        held both by the current reduction object and by the Doc for 
        passing between reductions in queues."""

        self.testdoc.setSansRun('3325')
        self.assertEqual(self.testdoc.getSansRun(), '3325')
        self.testdoc.setSansRun('3325.nxs')
        self.assertEqual(self.testdoc.getSansRun(), '3325')
        self.assertRaises(TypeError, self.testdoc.setSansRun, 3325)
        self.assertEqual(self.testdoc.getSansRun(), '3325')  
        self.assertRaises(TypeError, self.testdoc.setSansRun, True)

        self.testdoc.setSansTrans('3325')
        self.assertEqual(self.testdoc.getSansTrans(), '3325')
        self.testdoc.setSansTrans('3325.nxs')
        self.assertEqual(self.testdoc.getSansTrans(), '3325')
        self.assertRaises(TypeError, self.testdoc.setSansTrans, 3325)
        self.assertEqual(self.testdoc.getSansTrans(), '3325')  
        self.assertRaises(TypeError, self.testdoc.setSansTrans, True)

        self.testdoc.setBackgroundRun('3325')
        self.assertEqual(self.testdoc.getBackgroundRun(), '3325')
        self.testdoc.setBackgroundRun('3325.nxs')
        self.assertEqual(self.testdoc.getBackgroundRun(), '3325')
        self.assertRaises(TypeError, self.testdoc.setBackgroundRun, 3325)
        self.assertEqual(self.testdoc.getBackgroundRun(), '3325')  
        self.assertRaises(TypeError, self.testdoc.setBackgroundRun, True)

        self.testdoc.setBackgroundTrans('3325')
        self.assertEqual(self.testdoc.getBackgroundTrans(), '3325')
        self.testdoc.setBackgroundTrans('3325.nxs')
        self.assertEqual(self.testdoc.getBackgroundTrans(), '3325')
        self.assertRaises(TypeError, self.testdoc.setBackgroundTrans, 3325)
        self.assertEqual(self.testdoc.getBackgroundTrans(), '3325')  
        self.assertRaises(TypeError, self.testdoc.setBackgroundTrans, True)

        self.testdoc.setDirectBeam('3325')
        self.assertEqual(self.testdoc.getDirectBeam(), '3325')
        self.assertEqual(self.testdoc.currentReduction.getDirectBeam(
                                   ).getRunnumber(), '3325')
        self.testdoc.setDirectBeam('3326.nxs')
        # This behaviour is different because testdoc.directbeam is 
        # just the string being stored
        self.assertEqual(self.testdoc.getDirectBeam(), '3326.nxs')
        self.assertEqual(self.testdoc.currentReduction.getDirectBeam(
                                   ).getRunnumber(), '3326')
        self.assertRaises(TypeError, self.testdoc.setDirectBeam, 3325)
        self.assertEqual(self.testdoc.getDirectBeam(), '3326.nxs')  
        self.assertRaises(TypeError, self.testdoc.setDirectBeam, True)

        self.assertRaises(ValueError, self.testdoc.setMaskfile, '/some/bad/path')
        self.testdoc.setMaskfile('test_data/MASKSANS2D_095B.txt')
        self.assertEqual(self.testdoc.getMaskfile(), 'test_data/MASKSANS2D_095B.txt')
        self.assertEqual(self.testdoc.currentReduction.getMaskfile(),
                                           'test_data/MASKSANS2D_095B.txt')
        self.testdoc.setMaskfile('test_data/3326.nxs')
        # This behaviour is different because testdoc.maskfile is 
        # just the string being stored
        self.assertEqual(self.testdoc.getMaskfile(), 'test_data/3326.nxs')
        self.assertEqual(self.testdoc.currentReduction.getMaskfile( ), 
                                                'test_data/3326.nxs')
        self.assertEqual(self.testdoc.getMaskfile(), 'test_data/3326.nxs')  
        self.assertRaises(TypeError, self.testdoc.setMaskfile, True)


    def testGetAndSetDoc(self):
        """Test the remaining getters and setters from the Doc"""
        
        # Testing setInPath
        self.assertRaises(TypeError, self.testdoc.setInPath, 55)
        self.assertRaises(TypeError, self.testdoc.setInPath, True)
        self.assertRaises(ValueError, self.testdoc.setInPath, 'false/path')
        self.testdoc.setInPath('test_data') # path checked in SansReduce.py
        self.assertEqual(self.testdoc.getInPath(), 'test_data')
        self.testdoc.setInPath('/')
        self.assertEqual(self.testdoc.getInPath(), '/')

        # Testing setShowRawInMenus
        self.assertRaises(TypeError, self.testdoc.setShowRawInMenus, 55)
        self.assertRaises(TypeError, self.testdoc.setShowRawInMenus, 'string')
        self.testdoc.setShowRawInMenus(False)
        self.assertEqual(self.testdoc.getShowRawInMenus(), False)
        self.testdoc.setShowRawInMenus(True)
        self.assertEqual(self.testdoc.getShowRawInMenus(), True)

        # Testing setShowNexusInMenus
        self.assertRaises(TypeError, self.testdoc.setShowNexusInMenus, 55)
        self.assertRaises(TypeError, self.testdoc.setShowNexusInMenus, 'string')
        self.testdoc.setShowNexusInMenus(False)
        self.assertEqual(self.testdoc.getShowNexusInMenus(), False)
        self.testdoc.setShowNexusInMenus(True)
        self.assertEqual(self.testdoc.getShowNexusInMenus(), True)

        # Testing setOutputLOQ
        self.assertRaises(TypeError, self.testdoc.setOutputLOQ, 55)
        self.assertRaises(TypeError, self.testdoc.setOutputLOQ, 'string')
        self.testdoc.setOutputLOQ(False)
        self.assertEqual(self.testdoc.getOutputLOQ(), False)
        self.testdoc.setOutputLOQ(True)
        self.assertEqual(self.testdoc.getOutputLOQ(), True)

        # Testing setOutputCanSAS
        self.assertRaises(TypeError, self.testdoc.setOutputCanSAS, 55)
        self.assertRaises(TypeError, self.testdoc.setOutputCanSAS, 'string')
        self.testdoc.setOutputCanSAS(False)
        self.assertEqual(self.testdoc.getOutputCanSAS(), False)
        self.testdoc.setOutputCanSAS(True)
        self.assertEqual(self.testdoc.getOutputCanSAS(), True)

        # Testing setUseRunnumberForOutput
        self.assertRaises(TypeError, self.testdoc.setUseRunnumberForOutput, 55)
        self.assertRaises(TypeError, self.testdoc.setUseRunnumberForOutput, 'string')
        self.testdoc.setUseRunnumberForOutput(False)
        self.assertEqual(self.testdoc.getUseRunnumberForOutput(), False)
        self.testdoc.setUseRunnumberForOutput(True)
        self.assertEqual(self.testdoc.getUseRunnumberForOutput(), True)

        # Testing setBlogReduction
        self.assertRaises(TypeError, self.testdoc.setBlogReduction, 55)
        self.assertRaises(TypeError, self.testdoc.setBlogReduction, 'string')
        self.testdoc.setBlogReduction(False)
        self.assertEqual(self.testdoc.getBlogReduction(), False)
        self.testdoc.setBlogReduction(True)
        self.assertEqual(self.testdoc.getBlogReduction(), True)

        # Testing setQueue
        self.assertRaises(TypeError, self.testdoc.setQueue, 55)
        self.assertRaises(TypeError, self.testdoc.setQueue, 'string')
        self.testdoc.setQueue(False)
        self.assertEqual(self.testdoc.getQueue(), False)
        self.testdoc.setQueue(True)
        self.assertEqual(self.testdoc.getQueue(), True)
        
        # Testing setQueueViewVisible
        self.assertRaises(TypeError, self.testdoc.setQueueViewVisible, 55)
        self.assertRaises(TypeError, self.testdoc.setQueueViewVisible, 'string')
        self.testdoc.setQueueViewVisible(False)
        self.assertEqual(self.testdoc.getQueueViewVisible(), False)
        self.testdoc.setQueueViewVisible(True)
        self.assertEqual(self.testdoc.getQueueViewVisible(), True)

        # Testing setOutPath
        self.assertEqual(self.testdoc.outPath, '')
        self.testdoc.setInPath('test_data/')
        self.assertEqual(self.testdoc.getOutPath(), 'test_data/')                 
        self.assertRaises(TypeError, self.testdoc.setOutPath, 55)
        self.assertRaises(TypeError, self.testdoc.setOutPath, True)
        self.assertRaises(ValueError, self.testdoc.setOutPath, 'false/path')
        self.testdoc.setOutPath('test_data') # path checked in SansReduce.py
        self.assertEqual(self.testdoc.getOutPath(), 'test_data')
        self.testdoc.setInPath('/')
        self.assertEqual(self.testdoc.getOutPath(), 'test_data')
        self.testdoc.setOutPath('/')
        self.assertEqual(self.testdoc.getOutPath(), '/')
        
class SansReduceGuiMenuDocTest(unittest.TestCase):
    """Test Class for Menu utility methods for SansReduceGuiDoc"""

    def setUp(self):
        """Set up some standard objects and cases"""

        self.testdoc = SansReduceGui.SansReduceDoc()
        self.testdoc.setInPath('test_data')
        self.nexusteststring = 'nxsteststring.nxs'
        self.nx5teststring = 'nx5teststring.nx5'
        self.rawteststring = 'rawteststrging.raw'
        self.teststringdot = 'teststringdot.'
        self.leadingdotstring = '.teststringleaddot'
        self.emptyteststring = ''
        self.testfloat = 5.0

    def testIncludeRun(self):
        """Test the filter method that chooses what to populate dropdowns

        Method needs to test each of the possible setting for what is to be
        shown in the menus.
        """

        self.testdoc.setShowRawInMenus(True)
        self.testdoc.setShowNexusInMenus(False)
        self.assertEqual(self.testdoc.includeRun(self.nexusteststring), False)
        self.assertEqual(self.testdoc.includeRun(self.nx5teststring), False)
        self.assertEqual(self.testdoc.includeRun(self.rawteststring), True)
        self.assertEqual(self.testdoc.includeRun(self.teststringdot), False)
        self.assertEqual(self.testdoc.includeRun(self.leadingdotstring), False)
        self.assertEqual(self.testdoc.includeRun(self.emptyteststring), False)

        self.testdoc.setShowRawInMenus(False)
        self.testdoc.setShowNexusInMenus(True)
        self.assertEqual(self.testdoc.includeRun(self.nexusteststring), True)
        self.assertEqual(self.testdoc.includeRun(self.nx5teststring), True)
        self.assertEqual(self.testdoc.includeRun(self.rawteststring), False)
        self.assertEqual(self.testdoc.includeRun(self.teststringdot), False)
        self.assertEqual(self.testdoc.includeRun(self.leadingdotstring), False)
        self.assertEqual(self.testdoc.includeRun(self.emptyteststring), False)

        self.testdoc.setShowRawInMenus(True)
        self.testdoc.setShowNexusInMenus(True)
        self.assertEqual(self.testdoc.includeRun(self.nexusteststring), True)
        self.assertEqual(self.testdoc.includeRun(self.nx5teststring), True)
        self.assertEqual(self.testdoc.includeRun(self.rawteststring), True)
        self.assertEqual(self.testdoc.includeRun(self.teststringdot), False)
        self.assertEqual(self.testdoc.includeRun(self.leadingdotstring), False)
        self.assertEqual(self.testdoc.includeRun(self.emptyteststring), False)

        self.testdoc.setShowRawInMenus(False)
        self.testdoc.setShowNexusInMenus(False)
        self.assertEqual(self.testdoc.includeRun(self.nexusteststring), False)
        self.assertEqual(self.testdoc.includeRun(self.nx5teststring), False)
        self.assertEqual(self.testdoc.includeRun(self.rawteststring), False)
        self.assertEqual(self.testdoc.includeRun(self.teststringdot), False)
        self.assertEqual(self.testdoc.includeRun(self.leadingdotstring), False)
        self.assertEqual(self.testdoc.includeRun(self.emptyteststring), False)

        self.assertRaises(TypeError, self.testdoc.includeRun, self.testfloat)
        self.assertRaises(TypeError, self.testdoc.includeRun, True)
        
    def testGetRunListForMenu(self):
        """Tests for getRunListForMenu"""

        self.testdoc.setShowRawInMenus(True)
        self.testdoc.setShowNexusInMenus(False)
        self.assertEqual(self.testdoc.getRunListForMenu(), 
                 ['3325.raw', '3328.raw', '3329.raw', '3332.raw', '3333.raw'])

        self.testdoc.setShowRawInMenus(False)
        self.testdoc.setShowNexusInMenus(True)
        self.assertEqual(self.testdoc.getRunListForMenu(), 
                 ['3326.nxs', '3328.nxs', '3331.nxs', '3333.nxs'])

        self.testdoc.setShowRawInMenus(True)
        self.testdoc.setShowNexusInMenus(True)
        self.assertEqual(self.testdoc.getRunListForMenu(), 
                 ['3325.raw', '3326.nxs', '3328.nxs', '3328.raw', '3329.raw', 
                  '3331.nxs', '3332.raw', '3333.nxs', '3333.raw'])

        self.testdoc.setShowRawInMenus(False)
        self.testdoc.setShowNexusInMenus(False)
        self.assertEqual(self.testdoc.getRunListForMenu(), 
                 [])

# class QueueTests(unittest.TestCase):

if __name__ == '__main__':
    unittest.main()
