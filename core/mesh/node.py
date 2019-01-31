__author__ = "Zack Snyder"
__date__ = "1/23/19"

from address import Address
from group import Group
from network import Network
from connection import Connection
from listen import listen
from transmit import broadcast, transmit, beam, ping

class Node():
    """Node class defines and handles all network interactions among nodes in the network"""

    def __init__(self, address=None, group=None, network=None, connection=None):
        """Initialize instance of Node class"""
        
        # Address
        self.address = address
        if address is None:
            self.address = Address()
        
        # Group
        self.group = group
        if group is None:
            self.group = Group(id=None, controller=address, distances={address: 0}, max_size=0)
        
        # Network
        self.network = network
        if network is None:
            self.network = Network(groups={address: self.group})
        
        # Connection
        self.connection = connection
        if connection is None:
            self.connection = Connection()
        
        # Dictionary of sent messages waiting for an ack
        # Key: Message identifier
        # Value: 
        # self.waiting_for_ack = dict()

    def connect(self):
        """Connect node to group network"""
        broadcast(
            "Connect", 
            self.connection, 
            self.network
        )
        
        listen(self.address, self.connection, self.message_handler)

    def disconnect(self):
        pass
        

    def message_handler(self, dest, source, message):
        """Determines what to do with a message"""
        pass