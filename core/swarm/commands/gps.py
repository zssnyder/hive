__author__ = 'Zack Snyder'
__date__ = '4/22/19'

from hive.core.mesh import Command

class GPSCommand(Command):

    def __init__(self, latitude, longitude, altitude):
        """Initialize GPS Command

        * coords = tuple of (lat, long, alt)
        """

        parameters = {
            'lat': latitude,
            'long': longitude,
            'alt': altitude
        }

        super(GPSCommand, self).__init__(parameters=parameters)
