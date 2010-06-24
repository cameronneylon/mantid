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

from mantidsimple import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import logging
import sys
import os
import shutil

class AbstractScatteringRun(Object):
    """An abstract class to represent SANS runs

    The abstract class will provide internal data elements for run
    number, filename, and translation between them. It also provides
    the generic loading and saving methods.
    """

    def __init__(self):
        pass

class Trans(abstractScatteringRun):
    """A class to represent transmission measurements
    """

    def __init_(self):
        pass

class Sans(abstractScatteringRun):
    """A class representing SANS measurements
    """
    
    def __init__(self):
        pass

class AbstractReduction(Object):
    """An abstract class representing reduction processes

    The abstract class provides the internal data elements for
    SANS, TRANS, Background, and direct beam runs. These internal
    data elements are provided by the earlier classes.
    """

    def __init__(self):
        pass

class 1DReduction(AbstractReduction):
    """Class representing a standard 1D reduction
    """

    def __init__(self):
        pass
