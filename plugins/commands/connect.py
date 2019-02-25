from hive.core.mesh.classes import Command
from hive.plugins.handlers.connect import ConnectHandler

class ConnectCommand(Command):
    """Default command used to connect to the mesh network"""

    def __init__(self):
        """Initialize ConnectCommand subclass of Command"""
        parameters = {
            'connect': True,
            'request': True
        }
        super(ConnectCommand, self).__init__(handler=ConnectHandler(), parameters=parameters)