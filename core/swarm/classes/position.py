__author__ = 'Zack Snyder'
__date__ = '4/25/19'

import uuid

from hive.core.swarm import Offset

class Position(object):

    def __init__(self, latitude, longitude, altitude, id=None, offset=Offset()):
        """Initialize position object
        
        * lat, long, alt = gps coordinates
        * offset = x, y, z coordinates of position
        """
        self.latitude = latitude + offset.lat()
        self.longitude = longitude + offset.long(latitude)
        self.altitude = altitude + offset.z

    def to_tuple(self):
        """Return tuple"""
        return (self.latitude, self.longitude, self.altitude)

    # def x(self):

    # ------ Overrides ----------

    def __len__(self):
        return 0
