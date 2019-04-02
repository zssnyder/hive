__author__ = 'Zack Snyder'
__date__ = '3/17/19'

from hive.core.mesh.classes import handler
from hive.core.mesh.classes import Address
from hive.core.mesh.classes import Group

from hive.core.mesh import commands

class GroupHandler(handler.Handler):
    """Handler class for network requests"""

    def __init__(self, node):
        """Initialize handler for node grouping
        
        * node = current Node which is connected to the network
        """
        self.node = node

    def execute(self, parameters, source):
        """Execute grouping command handler"""

        return commands.GroupCommand(self.node.group, self.node.network.score())
