__author__ = 'Zack Snyder'
__date__ = '4/22/19'

class GPSDevice(object):

    def get_coords(self):
        """Returns a tuple of (
            latitude,
            longitude,
            altitude
        )
        """
        raise NotImplementedError('Need to implement in subclass')