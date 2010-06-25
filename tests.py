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

# Tests for SansReduce.py
# 
# Most of these tests are intended to be able to run outside of the
# Mantid environment for convenience. Clearly those that actually
# load or write data, or manipulate workspaces will not. These are
# not protected outside of Mantid so will fail visibly in tests run
# outside of Mantid

import SansReduce

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
                                                 '.' + self.testext[0])
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
        self.scattering.setExt(self.testext[0])

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
        self.reduction.setSansRun('3326.nxs', '3325.nxs')
        self.assertEqual(self.reduction.getSansRun().getRunnumber(), '3326')
        self.assertEqual(self.reduction.getSansRun().trans.getRunnumber(),
                         '3325')

    def testMaskfile(self):
        pass

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

    def testVerbose(self):
        """Quick test that verbose can be set and got"""

        self.reduction = SansReduce.AbstractReduction()
        self.reduction.setVerbose(True)
        self.assertEqual(self.reduction.getVerbose(), True)

if __name__ == '__main__':
    unittest.main()
