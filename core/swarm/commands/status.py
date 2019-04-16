__author__ = 'Zack Snyder'
__date__ = '4/9/19'

from hive.core.mesh.classes import Command

class StatusCommand(Command):
    """Shares status of drone with GS"""
    def __init__(self, x, y, z, status):

        parameters = {
            'status': status, # Running, Processing, Idle
            'x': x,
            'y': y,
            'z': z,
            'battery': 0
        }

        super(StatusCommand, self).__init__(parameters=parameters)

    