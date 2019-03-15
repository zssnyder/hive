__author__ = "Zack Snyder"
__date = "1/23/19"

from hive import plugins

class Configuration(object):
    """Mesh Configuration class"""


    def __init__(self, plugins={'connection': plugins.console.ConsoleConnection()}):
        """Initialize Mesh Network class

        * plugins - dictionary of plugins which need to be loaded
        """
        # Initialize node
        self.plugins = plugins

        self.separator = "///"
        self.wildcard = "*"
        # self.handler_module = ''
        # self.default_handler_module = 'hive.plugins.handlers'

        self.connection_timeout = 10

        self.ground_station_address = ''
        self.ground_station_ip = ''

        self.max_group_size = 1