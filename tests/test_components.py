# -*- coding: utf-8 -*-

"""Unittests for Janitoo-Roomba Server.
"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import warnings
warnings.filterwarnings("ignore")

import sys, os
import time, datetime
import unittest
import threading
import logging
from pkg_resources import iter_entry_points

from janitoo_nosetests.server import JNTTServer, JNTTServerCommon
from janitoo_nosetests.thread import JNTTThread, JNTTThreadCommon
from janitoo_nosetests.component import JNTTComponent, JNTTComponentCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

import janitoo_hostsensor_raspberry.component as jnt_component

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_DISCOVERY = 0x5000

assert(COMMAND_DESC[COMMAND_DISCOVERY] == 'COMMAND_DISCOVERY')
##############################################################

class TestComponentPiCPU(JNTTComponent, JNTTComponentCommon):
    """Test the component
    """
    component_name = "hostsensor.picpu"

    def test_100_hardware_cpu_temperature(self):
        self.onlyRasperryTest()
        component = self.factory[self.component_name]()
        print("Temperature : ", component.cpu_temperature(None, 0))
        self.assertNotEqual(component.cpu_temperature(None, 0), None)
        self.assertEqual(type(component.cpu_temperature(None, 0)), type(0.0))

    def test_110_hardware_cpu_frequency(self):
        self.onlyRasperryTest()
        component = self.factory[self.component_name]()
        print("Frequency : ", component.cpu_frequency(None, 0))
        self.assertNotEqual(component.cpu_frequency(None, 0), None)
        self.assertEqual(type(component.cpu_frequency(None, 0)), type(0))

    def test_120_hardware_cpu_volt(self):
        self.onlyRasperryTest()
        component = self.factory[self.component_name]()
        print("Voltage : ", component.cpu_volt(None, 0))
        self.assertNotEqual(component.cpu_volt(None, 0), None)
        self.assertEqual(type(component.cpu_volt(None, 0)), type(0.0))

    def test_130_cpu_governor(self):
        self.onlyRasperryTest()
        component = self.factory[self.component_name]()
        print("governor : ", component.set_governor(None, 0, 'conservative'))
        self.assertNotEqual(component.set_governor(None, 0, 'conservative'), None)
