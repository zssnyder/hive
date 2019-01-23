"""Network class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

from address import Address
from route import Route

class Network():
    """Network class describing network topology
    
    Stores network configuration in network table
    """

    def __init__(self, routes=[]):
        """Initialize instance of the network

        * group - network biases group nodes in network table !!!! How to optimize groups?
        """
        self.routes = routes


    def add_route(self, route):
        """Add new route to network"""
        self.routes.append(route)

    def get_route(self, dest):
        """Get route for destination address"""
        for route in self.routes:
            if route.dest == dest:
                return route
    
    def get_next(self, dest):
        """Get next address in path to dest"""
        for route in self.routes:
            if route.dest == dest:
                return route.next

