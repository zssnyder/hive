__author__ = 'Zack Snyder'
__date__ = '3/18/19'

import logging
from subprocess import check_output, CalledProcessError

from hive.core.mesh.classes import Configuration
from hive.core.mesh import classes
from hive.core.mesh import commands

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

class ConnectHandler(classes.Handler):
    """Handler for ConnectCommand"""

    def execute(self, parameters, source):
        """Execute connect command with given parameters
        
        * parameters - dictionary of configuration and initialization
        """
        if parameters['GS'] == True or Configuration.is_ground_station:
            try:
                # Check if connect request
                if parameters['request'] == False:
                    return None

            except KeyError as ke:
                print('Command is not a connect request')
                print(ke.args)

            else:
                return commands.ConnectCommand()