"""Handler for receiving messages in the Hive mesh network"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

from config import MeshConfiguration as MC
from connection import Connection
from address import Address

# import string library
import string
import thread

def listen(address, connection, callback):
        """Listen for messages on network

        On-Time Call
        
        * address - address of listening node
        * connection - connection class defining radio connection
        * action_callback(destination, source, message) - handles all message actions
        """
        while True:
                message = connection.read()
                if message is not None:

                        split_message = message.split(MC.separator, 4) # split_message = next + rest of packet
                        # Break message into its respective pieces
                        next = Address(id=split_message[0])
                        destination = Address(id=split_message[1])
                        source = Address(id=split_message[2])
                        
                        # Decide when to invoke callback
                        if next == address or next == Address(id=MC.wildcard):
                                thread.start_new_thread(callback, (destination, source, split_message[3]))     


    

