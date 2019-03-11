import logging

from hive.core.mesh import classes as mesh

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

class ConnectHandler(mesh.Handler):
    """Handler for ConnectCommand"""

    def execute(self, parameters):
        """Execute connect command with given parameters
        
        * parameters - dictionary of configuration and initialization
        """
        if parameters['response'] is not None:
            logging.debug(parameters['address'])
        