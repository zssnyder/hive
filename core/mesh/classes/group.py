__author__ = "Zack Snyder"
__date__ = "1/23/19"

# import unique identifier library
from uuid import uuid4

class Group(object):
    """Group class desribing logical grouping of nodes in network"""

    def __init__(self, id=None, controller=None, addresses=None, max_size=0):
        """Initialize Group class

        * id: unique group identifier
        * controller: address of the group controller
        * addresses: list of addresses 
        """
        # Set an unique id for the group
        if id is not None:
            self.id = id
        else:
            self.id = uuid4().hex
        
        self.controller = controller

        # Address of all nodes in group
        self.addresses = addresses
        # Maximum size of a group
        self.max_size = max_size

    def merge(self, source, address, group):
        """Merge two groups together"""
        if source in group.addresses[:self.max_size + 1]:
            if address not in self.addresses: 
                self.addresses.append(address)
            if len(group.nodes) < self.max_size:
                self.max_size = len(group.addresses)
        elif address in self.addresses:
            self.addresses.remove(address)
        # Reduce size of group to max size
        self.addresses = self.addresses[:self.max_size]

    def add(self, address, network):
        """Add an address to the group"""
        if address in network.signals.keys():
            # Sort addresses by signal appended with new address
            self.addresses = sorted(self.addresses + address, lambda key: network.signals[key])
            return True
        return False

    def remove(self, address):
        """Remove an address from the group"""
        if address in self.addresses: 
            self.addresses.remove(address)
            return True
        return False

    # ----- Overrides -------

    def __str__(self):
        """String representation of the group"""
        return str(self.addresses)