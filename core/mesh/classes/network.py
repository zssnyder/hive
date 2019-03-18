"""Network class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

class Network(object):
    """Network class describing network topology
    
    Stores network configuration in network table
    """

    def __init__(self, signals=dict(), groups=dict()):
        """Initialize instance of the network

        * signals - dictionary of [node address: RSSI strength]
        * groups - dictionary of [node address, group]
        """
        self.signals = signals
        self.groups = groups

    # ----- Signals -------
    def add_signal(self, address, signal):
        """Add new address and rssi to network or override existing rssi"""
        self.signals[str(address)] = signal
    
    def remove_signal(self, address):
        """Remove address or signal from network"""
        if str(address) in self.signals.keys():
            del self.signals[str(address)]

    # ----- Groups --------
    def add_group(self, address, group):
        """Add new group to network or override existing group"""
        self.groups[str(address)] = group

    def remove_group(self, address, group):
        """Remove a group from network table"""
        if str(address) in self.groups.keys():
            del self.groups[str(address)]

    def get_group(self, address):
        """Get route for destination address"""
        return self.groups[str(address)]
    
    # ----- Addresses ------
    def addresses(self):
        """Get value sorted list of known addresses"""
        return [address for address, in sorted(self.signals.items(), lambda kv: kv[1])]