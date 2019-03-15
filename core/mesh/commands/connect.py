__author__ = 'Zack Snyder'
__date__ = '3/15/19'

from subprocess import check_output, CalledProcessError
from hive.core.mesh.classes import Command
from hive.core.mesh.handlers import ConnectHandler

class ConnectCommand(Command):
    """Default command used to connect to the mesh network"""

    def __init__(self):
        """Initialize ConnectCommand subclass of Command"""
        
        try:
            ip = str(check_output(['hostname', '-I']))
        except CalledProcessError as cpe:
            print('Could not get ')
            print(cpe.args)

            ip = ''

        parameters = {
            'connect': True,
            'request': True,
            'ip': ip,
        }
        
        super(ConnectCommand, self).__init__(parameters=parameters)