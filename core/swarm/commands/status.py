__author__ = 'Zack Snyder'
__date__ = '4/9/19'

from hive.core.mesh.classes import Command

class StatusCommand(Command):
    """Shares status of drone with GS"""
    def __init__(self, drone):

        parameters = {
            'status': drone.status, # Running, Processing, Idle
            'x': drone.offset.x,
            'y': drone.offset.y,
            'z': drone.offset.z,
            'battery': drone.battery_level()
        }

        super(StatusCommand, self).__init__(parameters=parameters)

    