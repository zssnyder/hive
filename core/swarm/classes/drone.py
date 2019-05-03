__author__ = 'Zack Snyder'
__date__ = '4/22/19'

import math

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
        """Get positional offset from lat, long, alt"""

        lat, long, alt = self.location()

        x = distance.distance((latitude, longitude), (latitude, long))
        y = distance.distance((latitude, longitude), (lat, longitude))
        z = alt - altitude

        return Offset(x, y, z)

    def get_distance_from(self, offset):
        """Get distance another offset"""

        return math.sqrt((offset.x - self.offset.x)^2 + (offset.y - self.offset.y)^2 + (offset.z - self.offset.z)^2)

    def battery_level(self):
        """Get battery level for drone"""
        return 100