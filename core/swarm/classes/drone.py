__author__ = 'Zack Snyder'
__date__ = '4/22/19'

from geopy import distance

from hive.core.swarm import Offset
from hive.core.swarm import Status
from hive.core.swarm import Position

class Drone(object):

    def __init__(self, node, gps):
        """Initialize a drone object

        * node = provides network access from mesh network
        * gps_device = handles gps location data
        """
        # Reference all of node's properties
        self.address = node.address
        self.group = node.group
        self.network = node.network
        self.gps = gps
        self.offset = Offset()
        self.status = Status.idle

    def is_commander(self):
        return self.group.commander == self.address

    def location(self):
        return self.gps.get_coords()

    def get_offset_from(self, latitude, longitude, altitude):
        """Set positional offset"""

        lat, long, alt = self.location()

        x = distance.distance((latitude, longitude), (latitude, long))
        y = distance.distance((latitude, longitude), (lat, longitude))
        z = alt - altitude

        return Offset(x, y, z)

    