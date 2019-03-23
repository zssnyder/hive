__author__ = 'Zack Snyder'
__date__ = '3/22/19'

from digi.xbee.devices import XBeeDevice

from hive.core.mesh import Connection

class XBeeConnection(Connection):

    def __init__(self, port, baud=9600):
        """Initialize XBeeConnection class

        * port = /dev/tty* port connection
        * baud = baud rate of device
        """
        self.device = XBeeDevice(port, baud)

        super(XBeeConnection, self).__init__()


    def open(self):
        """Open a connection"""
        self.device.open()

    def close(self):
        """Close a connection"""
        self.device.close()

    def write(self, message):
        """Write to network connection"""
        self.device.send_packet(message)

    def read(self, timeout=None):
        """Read xbee data"""
        return self.device.read_data(timeout)
