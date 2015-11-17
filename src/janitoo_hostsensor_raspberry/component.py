# -*- coding: utf-8 -*-
"""The Raspberry hardware worker

Define a node for the cpu with 3 values : temperature, frequency and voltage

http://www.maketecheasier.com/finding-raspberry-pi-system-information/

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
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

import logging
logger = logging.getLogger( "janitoo.hostsensor" )

import os, sys
import threading
import re
from pkg_resources import get_distribution, DistributionNotFound

from janitoo.thread import JNTBusThread
from janitoo.options import get_option_autostart
from janitoo.utils import HADD
from janitoo.node import JNTNode
from janitoo.bus import JNTBus
from janitoo.component import JNTComponent
from janitoo.value import JNTValue, value_config_poll

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_METER = 0x0032
COMMAND_CONFIGURATION = 0x0070

assert(COMMAND_DESC[COMMAND_METER] == 'COMMAND_METER')
assert(COMMAND_DESC[COMMAND_CONFIGURATION] == 'COMMAND_CONFIGURATION')
##############################################################

def make_picpu(**kwargs):
    return HardwareCpu(**kwargs)

class HardwareCpu(JNTComponent):
    """
    This class abstracts a roowifi and gives attributes for telemetry data,
    as well as methods to command the robot
    """
    def __init__(self, bus=None, addr=None, **kwargs):
        JNTComponent.__init__(self, 'hostsensor.picpu', bus=bus, addr=addr, name="Raspberry pi CPU", **kwargs)

        self.re_nondecimal = re.compile(r'[^\d.]+')

        uuid="temperature"
        self.values[uuid] = self.value_factory['sensor_temperature'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The temperature of the CPU',
            label='CPUTemp',
            get_data_cb=self.cpu_temperature,
        )
        poll_value = self.values[uuid].create_poll_value()
        self.values[poll_value.uuid] = poll_value

        uuid="frequency"
        self.values[uuid] = self.value_factory['sensor_frequency'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The frequency of the CPU',
            label='CPUFreq',
            get_data_cb=self.cpu_frequency,
        )
        poll_value = self.values[uuid].create_poll_value()
        self.values[poll_value.uuid] = poll_value

        uuid="voltage"
        self.values[uuid] = self.value_factory['sensor_voltage'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The voltage of the CPU',
            label='CPUVolt',
            get_data_cb=self.cpu_volt,
        )
        poll_value = self.values[uuid].create_poll_value()
        self.values[poll_value.uuid] = poll_value

    def cpu_temperature(self, node_uuid, index):
        res = os.popen('vcgencmd measure_temp').readline()
        ret = None
        try:
            ret = float(self.re_nondecimal.sub('', res))
        except ValueError:
            logger.exception('Exception when retrieving CPU temperature')
            ret = None
        return ret

    def cpu_frequency(self, node_uuid, index):
        res = os.popen('vcgencmd measure_clock arm').readline()
        ret = None
        try:
            ret = int(res.replace("frequency(45)=",""))/1000000
        except ValueError:
            logger.exception('Exception when retrieving CPU frequency')
            ret = None
        return ret

    def cpu_volt(self, node_uuid, index):
        res = os.popen('vcgencmd measure_volts core').readline()
        ret = None
        try:
            ret = float(self.re_nondecimal.sub('', res))
        except ValueError:
            logger.exception('Exception when retrieving CPU voltage')
            ret = None
        return ret
