__author__ = 'Zack Snyder'
__date__ = '4/29/19'

from hive.core.mesh import Command

class ChoiceCommand(Command):

    def __init__(self, offset, distance):
        """Initialize choice command

        * offset = best offset choice
        * distance = distance to offset
        """
        parameters = {
            'off': offset.to_dict(),
            'dst': distance
        }

        super(ChoiceCommand, self).__init__(parameters=parameters)