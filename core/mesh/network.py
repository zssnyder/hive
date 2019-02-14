"""Network class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

from address import Address
from group import Group

class Network():
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
        self.signals[address] = signal
    
    def remove_signal(self, address):
        """Remove address or signal from network"""
        if address in self.signals.keys():
            del self.signals[address]

    # ----- Groups --------
    def add_group(self, address, group):
        """Add new group to network or override existing group"""
        self.groups[address] = group

    def get_group(self, address):
        """Get route for destination address"""
        return self.groups[address]
    
    # ----- Addresses ------
    def addresses(self):
        """Get value sorted list of known addresses"""
        return [address for address, in sorted(self.signals.items(), lambda kv: kv[1])]

