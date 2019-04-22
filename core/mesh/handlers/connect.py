__author__ = 'Zack Snyder'
__date__ = '3/18/19'

import logging
from subprocess import check_output, CalledProcessError

from hive.core.mesh.classes import MeshConfiguration
from hive.core.mesh import classes
from hive.core.mesh import commands

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

class ConnectHandler(classes.Handler):
    """Handler for ConnectCommand"""

    def execute(self, parameters, source):
        """Execute connect command with given parameters
        
        * parameters - dictionary of configuration and initialization
        """
        if parameters['GS'] == True and MeshConfiguration.is_ground_station == False:

            MeshConfiguration.ground_station_address = source
            MeshConfiguration.ground_station_ip = parameters['ip']
            MeshConfiguration.max_group_size = parameters['max_group_size']
            MeshConfiguration.network_size = parameters['network_size']

            try:
                # Check if connect request
                if parameters['request'] == False:
                    return None

            except KeyError as ke:
                logging.debug('Command is not a connect request')
                logging.debug(ke.args)

            else:
                return commands.ConnectCommand()
