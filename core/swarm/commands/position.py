__author__ = 'Zack Snyder'
__date__ = '4/20/19'

from hive.core.mesh import Command

class PositionCommand(Command):

    def __init__(self, offsets, velocity):
        """Initialize a position command

        * positions = list of x, y, z offset tuples
        """

        parameters = {
            'off': offsets,
            'vel': velocity,
        }

        super(PositionCommand, self).__init__(parameters=parameters)