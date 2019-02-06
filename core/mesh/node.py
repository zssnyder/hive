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

    def __init__(self, address=Address(), group=Group(), network=Network(), connection=Connection()):
        """Initialize instance of Node class"""
        
        # Address
        self.address = address
        
        # Group
        self.group = group
        
        # Network
        self.network = network
        self.network.add_signal(self.address, 0)
        self.network.add_group(self.address, self.group)

        # Connection
        self.connection = connection
        
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