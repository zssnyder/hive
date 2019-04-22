__author__ = 'Zack Snyder'
__date__ = '4/20/19'

from hive.core.mesh import Command

class PositionCommand(Command):

    def __init__(self, positions, velocity):
        """Initialize a position command
        """

        parameters = {
            'positions': positions,
            'velocity': velocity

        }

        super().__init__(parameters=parameters)