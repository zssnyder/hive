__author__ = 'Zack Snyder'
__date__ = '3/17/19'

from hive.core.mesh.classes import handler
from hive.core.mesh.classes import Address
from hive.core.mesh.classes import Group

class GroupHandler(handler.Handler):
    """Handler class for network requests"""

    def __init__(self, node):
        """Initialize handler for node grouping
        
        * node = current Node which is connected to the network
        """
        self.node = node

    def execute(self, parameters, source):
        """Execute grouping command handler"""

        # Initialize neighbor group
        addresses = [Address(addr) for addr in parameters['group']]
        group = Group(parameters['id'], source, addresses, int(parameters['size']))
        # Update neighbor group in network
        self.node.network.add_group(source, group)
