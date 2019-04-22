__author__ = 'Zack Snyder'
__date__ = '4/20/19'

from hive.core.mesh import Handler
from hive.core.swarm import Formation

class PositionHandler(Handler):

    def __init__(self, node):

        self.node = node 
        pass

    def execute(self, parameters, source):
        """Execute Positioning handler"""
        
        if self.node.group.commander == self.node.address: 
            
            positions = parameters['positions']

            formation = Formation(positions)

        else: return
