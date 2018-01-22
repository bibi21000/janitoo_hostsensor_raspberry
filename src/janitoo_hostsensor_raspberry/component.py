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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import logging
logger = logging.getLogger(__name__)

import os
import re
from pkg_resources import DistributionNotFound
import subprocess

from janitoo.compat import str_to_native
from janitoo.component import JNTComponent

##############################################################
#Check that we are in sync with the official command classes
#Must be implemented for non-regression
from janitoo.classes import COMMAND_DESC

COMMAND_METER = 0x0032
COMMAND_CONFIGURATION = 0x0070

assert(COMMAND_DESC[COMMAND_METER] == 'COMMAND_METER')
assert(COMMAND_DESC[COMMAND_CONFIGURATION] == 'COMMAND_CONFIGURATION')
##############################################################

from janitoo_hostsensor import OID

def make_picpu(**kwargs):
    return HardwareCpu(**kwargs)

class HardwareCpu(JNTComponent):
    """
    This class abstracts a roowifi and gives attributes for telemetry data,
    as well as methods to command the robot
    """
    def __init__(self, bus=None, addr=None, **kwargs):
        oid = kwargs.pop('oid', '%s.picpu'%OID)
        name = kwargs.pop('name', "Raspberry pi CPU")
        JNTComponent.__init__(self, oid=oid, bus=bus, addr=addr, name=name, **kwargs)

        self.re_nondecimal = re.compile(r'[^\d.]+')

        uuid="temperature"
        self.values[uuid] = self.value_factory['sensor_temperature'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The temperature of the CPU',
            label='CPUTemp',
            get_data_cb=self.cpu_temperature,
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

        uuid="frequency"
        self.values[uuid] = self.value_factory['sensor_frequency'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The frequency of the CPU',
            label='CPUFreq',
            get_data_cb=self.cpu_frequency,
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

        uuid="voltage"
        self.values[uuid] = self.value_factory['sensor_voltage'](options=self.options, uuid=uuid,
            node_uuid=self.uuid,
            help='The voltage of the CPU',
            label='CPUVolt',
            get_data_cb=self.cpu_volt,
        )
        poll_value = self.values[uuid].create_poll_value(default=300)
        self.values[poll_value.uuid] = poll_value

    def cpu_temperature(self, node_uuid, index):
        ret = None
        try:
            cmd = 'vcgencmd measure_temp'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            stdout = [x for x in stdout.split(str_to_native("\n")) if len(x) != 0]
            stderr = [x for x in stderr.split(str_to_native("\n")) if len(x) != 0]
            if process.returncode < 0 or len(stderr):
                for error in stderr:
                    logger.error('[%s] - Error when retrieving CPU temperature : %s', self.__class__.__name__, error)
            else:
                ret = float(self.re_nondecimal.sub('', stdout[0]))
        except ValueError:
            logger.exception('[%s] - Exception when retrieving CPU temperature', self.__class__.__name__)
            ret = None
        return ret

    def cpu_frequency(self, node_uuid, index):
        ret = None
        try:
            cmd = 'vcgencmd measure_clock arm'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            sstdout = [x for x in stdout.split(str_to_native("\n")) if len(x) != 0]
            sstderr = [x for x in stderr.split(str_to_native("\n")) if len(x) != 0]
            if process.returncode < 0 or len(sstderr):
                for error in sstderr:
                    logger.error('[%s] - Error when retrieving CPU frequency : %s', self.__class__.__name__, error)
            else:
                ret = int(sstdout[0].replace("frequency(45)=",""))/1000000
        except ValueError:
            logger.exception('[%s] - Exception when retrieving CPU frequency', self.__class__.__name__)
            ret = None
        return ret

    def cpu_volt(self, node_uuid, index):
        ret = None
        try:
            cmd = 'vcgencmd measure_volts core'
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            sstdout = [x for x in stdout.split(str_to_native("\n")) if len(x) != 0]
            sstderr = [x for x in stderr.split(str_to_native("\n")) if len(x) != 0]
            if process.returncode < 0 or len(sstderr):
                for error in sstderr:
                    logger.error('[%s] - Error when retrieving CPU voltage : %s', self.__class__.__name__, error)
            else:
                ret = float(self.re_nondecimal.sub('', sstdout[0]))
        except ValueError:
            logger.exception('[%s] - Exception when retrieving CPU voltage', self.__class__.__name__)
            ret = None
        return ret
