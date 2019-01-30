"""Network class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

from address import Address
from group import Group

class Network():
    """Network class describing network topology
    
    Stores network configuration in network table
    """

    def __init__(self, groups=dict()):
        """Initialize instance of the network

        * groups - dictionary of (node address, group object)
        """
        self.groups = groups


    def set_group(self, address, group):
        """Add new group to network"""
        self.groups[address] = group

    def get_group(self, address):
        """Get route for destination address"""
        return self.groups[address]
    
    # def get_next(self, dest):
    #     """Get next address in path to dest"""
    #     for route in self.routes:
    #         if route.dest == dest:
    #             return route.next

