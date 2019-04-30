__author__ = 'Zack Snyder'
__date__ = '4/23/19'

import math
import uuid

from geopy.geocoders import Nominatim
from geopy import distance

class Offset(object):

    precision = 4

    def __init__(self, id=None, x=0, y=0, z=0):
        """Initialize Offset 

        * x = x units position
        * y = y units position
        * z = z units position
        """
        self.id = uuid.uuid4().hex if id is None else id
        self.x = x
        self.y = y
        self.z = z

    def lat(self):
        """Get degrees latitude offset from meter distance"""
        return (self.y)/(110.54 * 1000)

    def long(self, latitude):
        """Get degrees longitude offset from meter distance"""
        lat_r = latitude * math.pi/180
        return (self.x)/(111.32 * math.cos(lat_r) * 1000)

    def to_dict(self):
        """Convert class to dictionary"""
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

    # ------- Overrides ---------

    def __eq__(self, other):
        """Define new equality"""
        if isinstance(other, Offset):
            x_equal = round(self.x, self.precision) == round(other.x, self.precision)
            y_equal = round(self.y, self.precision) == round(other.y, self.precision)
            z_equal = round(self.z, self.precision) == round(other.z, self.precision)
            return x_equal and y_equal and z_equal
        else:
            return False