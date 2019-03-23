__author__ = 'Zack Snyder'
__date__ = '3/15/19'

from subprocess import check_output, CalledProcessError

from hive.core.mesh.classes import Configuration
from hive.core.mesh import classes


class ConnectCommand(classes.Command):
    """Default command used to connect to the mesh network"""

    def __init__(self, max_group_size, is_ground_station):
        """Initialize ConnectCommand subclass of Command"""
        
        try:
            ip = str(check_output(['curl', 'ifconfig.me']))
        except CalledProcessError as cpe:
            print('Could not get ip')
            print(cpe.args)

            ip = ''

        parameters = {
            'ip': ip,
            'max_group_size': Configuration.max_group_size,
            'GS': Configuration.is_ground_station
        }
        
        super(ConnectCommand, self).__init__(parameters=parameters)