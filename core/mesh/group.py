__author__ = "Zack Snyder"
__date__ = "1/23/19"

# import unique identifier library
from uuid import uuid4

class Group():
    """Group class desribing logical grouping of nodes in network"""

    def __init__(self, id=None, controller=None, nodes=dict(), max_size=0):
        """Initialize Group class

        * addresses: list of node addresses in group
        """
        # Set an unique id for the group
        if id is not None:
            self.id = id
        else:
            self.id = uuid4()
        
        self.controller = controller
        # Ordered list of tuples (address, distance) denoting nearby nodes
        self.nodes = [(address, distance) for address, distance in sorted(nodes.items(), lambda kv: kv[1])]
        # Address of all nodes in group
        self.addresses = [address for address, distance in self.nodes]
        # Distances between current node and other nodes
        self.distances = [distance for address, distance in self.nodes]
        # Maximum size of a group
        self.max_size = max_size

    def merge(self, group):
        """Merge two groups into one"""
        pass

    def add(self, address):
        """Add an address to the group"""
        pass

    def remove(self, address):
        """Remove an address from the group"""
        pass