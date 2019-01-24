__author__ = "Zack Snyder"
__date__ = "1/23/19"

# import unique identifier library
from uuid import uuid4

class Group():
    """Group class desribing logical grouping of nodes in network"""

    def __init__(self, id=None, controller=None, addresses=[]):
        """Initialize Group class

        * addresses: list of node addresses in group
        """
        if id is not None:
            self.id = id
        else:
            self.id = uuid4()
        
        self.controller = controller
        self.addresses = addresses

    def merge(self, group):
        """Merge two groups into one"""
        pass

    def add(self, address):
        """Add an address to the group"""
        pass

    def remove(self, address):
        """Remove an address from the group"""
        pass