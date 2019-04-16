__author__ = 'Zack Snyder'
__date__ = '3/22/19'

import time

from digi.xbee import devices
from digi.xbee.reader import XBeeMessage

from hive.core.mesh import Configuration
from hive.core.mesh import Connection
from hive.core.mesh.classes import exceptions

class XBeeConnection(Connection):

    def get_address(self):
        return self.device.get_64bit_addr()

    def __init__(self, port, baud=9600):
        """Initialize XBeeConnection class

        * port = /dev/tty* port connection
        * baud = baud rate of device
        """
        self.device = devices.XBeeDevice(port, baud)
        self.network = self.device.get_network()
        super(XBeeConnection, self).__init__()


    def open(self):
        """Open a connection"""
        self.device.open()

    def close(self):
        """Close a connection"""
        self.device.close()

    def write(self, message, dest):
        """Write to network connection"""
        
        if str(dest) == Configuration.wildcard:
            # Get network information
            network = self.device.get_network()

            # Run discovery process for XBee network
            network.start_discovery_process()
            while network.is_discovery_running():
                time.sleep(0.5)

            # Get list of remote devices
            devices = network.get_devices()

            # Send message to each device in network
            for remote in devices:
                self.device.send_data(remote, message)
        else: 

            remote_device = devices.RemoteXBeeDevice(self.device, x64bit_addr=dest)
            self.device.send_data(remote_device, message)

    def read(self, timeout=None):
        """Read xbee data"""
        message = self.device.read_data(timeout)

        if message is None:
            raise exceptions.ReadTimeoutException(['No data available'])
        else: 
            return message.data.decode("utf8"), message
