__author__ = 'Zack Snyder'
__date__ = '3/19/19'

class Formation(object):

    def __init__(self, positions=[]):
        """Initialize a formation object"""
        self.offsets = dict()
        self.choices = dict()
        self.distances = dict()

    # ----- Update methods -----------

    def add_position(self, offset, distance):
        """Add a position to the formation and order it by distance"""
        self.distances[str(offset.id)] = distance
        self.offsets[str(offset.id)] = offset

    def choose_position(self, offset, address):
        """Update position for address"""
        self.choices[str(address)] = offset.id
        self.offsets[str(offset.id)] = offset

    # ----- Get Methods -----------

    def get_positions(self):
        """Get ordered list of positions sorted by distance"""
        return sorted([offset for offset in self.offsets.items()], key=lambda offset: self.distances[str(offset.id)])

    def get_position_for(self, address):
        """Get specific position for address"""
        return self.offsets[str(self.choices[str(address)])]