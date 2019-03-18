__author__ = 'Zack Snyder'
__date__ = '3/15/19'

from subprocess import check_output, CalledProcessError

from hive.core.mesh import mesh
from hive.core.mesh import classes


class ConnectCommand(classes.Command):
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
            'max_group_size': mesh.configuration.max_group_size,
            'GS': mesh.configuration.is_ground_station
        }
        
        super(ConnectCommand, self).__init__(parameters=parameters)