__author__ = "Zack Snyder"
__date = "1/23/19"

class Configuration(object):
    """Mesh Configuration class"""


    # Initialize node
    plugins = dict()

    # Packet
    separator = "///"
    wildcard = "*"
    # self.handler_module = ''
    # self.default_handler_module = 'hive.plugins.handlers'

    # Connection
    connection_timeout = 10

    # Ground Station
    is_ground_station = False
    ground_station_address = ''
    ground_station_ip = ''

    # Grouping
    max_group_size = 1
    # Number of seconds between grouping attempts
    group_interval = 30 

    def __init__(self):
        """Initialize Mesh Network class

        * plugins - dictionary of plugins which need to be loaded
        """
