__author__ = 'Zack Snyder'
__date__ = '3/15/19'


from hive.core.swarm.classes import SwarmConfiguration
from hive.core.swarm.commands import PositionCommand

class swarm(object):

    def __init__(self, mesh, configuration=SwarmConfiguration()):
        """Initialize a swarm object"""
        self.mesh = mesh
        self.configuration = configuration

    def form(self, formation):
        """Forms a swarm into a 3D formation"""

        command = PositionCommand(formation, self.configuration.max_speed)

        self.mesh
        
        