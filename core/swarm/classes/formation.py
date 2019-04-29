__author__ = 'Zack Snyder'
__date__ = '3/19/19'

class Formation(object):

    def __init__(self):
        """Initialize a formation object"""
        self.positions = dict()

    def set_position(self, address, position):
        """Update position for address"""
        self.positions[str(address)] = position