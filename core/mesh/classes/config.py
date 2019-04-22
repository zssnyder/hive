__author__ = "Zack Snyder"
__date = "1/23/19"

class MeshConfiguration(object):
    """Mesh Configuration class"""


    # Initialize plugins
    plugins = dict()

    # Packet
    separator = "///"
    wildcard = "*"

    # Connection
    connection_timeout = 10

    # Ground Station
    is_ground_station = False
    ground_station_address = ''
    ground_station_ip = ''

    # Grouping
    network_size = 1
    max_group_size = 1
    # Number of seconds between grouping attempts
    group_interval = 30 

    def __init__(self, plugins=dict(), separator='///', wildcard='*', connection_timeout=10, is_ground_station=False, ground_station_address='', ground_station_ip='', swarm_size=1, max_group_size=1, group_interval=30):
        """Initialize Mesh Network class

        * plugins - dictionary of plugins which need to be loaded
        """
        self.plugins = plugins

        self.separator = separator
        self.wildcard = wildcard
        self.connection_timeout = connection_timeout

        self.is_ground_station = is_ground_station
        self.ground_station_address = ground_station_address
        self.ground_station_ip = ground_station_ip

        self.network_size = swarm_size
        self.max_group_size = max_group_size
        self.group_interval = group_interval
