__author__ = 'Zack Snyder'
__date__ = '3/15/19'

from subprocess import check_output, CalledProcessError

from hive.core.mesh import MeshConfiguration
from hive.core.mesh import Command


class ConnectCommand(Command):
    """Default command used to connect to the mesh network"""

    def __init__(self):
        """Initialize ConnectCommand subclass of Command"""
        
        try:
            ip = str(check_output(['curl', 'ifconfig.me']))
        except CalledProcessError as cpe:
            print('Could not get ip')
            print(cpe.args)

            ip = ''

        parameters = {
            'ip': ip,
            'network_size': MeshConfiguration.network_size,
            'max_group_size': MeshConfiguration.max_group_size,
            'GS': MeshConfiguration.is_ground_station
        }
        
        super(ConnectCommand, self).__init__(parameters=parameters)