__author__ = 'Zack Snyder'
__date__ = '3/17/19'

from hive.core.mesh.classes import handler

class GroupHandler(handler.Handler):
    """Handler class for network requests"""

    def __init__(self, node):
        """Initialize handler for node grouping
        
        * node = current Node which is connected to the network
        """

        self.node = node

    def execute(self, parameters):
        """Execute grouping command handler"""

        pass