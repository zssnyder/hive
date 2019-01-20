"""Handler for receiving messages in the Hive mesh network"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"


from network import Network
from connection import Connection
from address import Address

import string

def listen(source, dest, connection):
        """Listen for messages on network
        
        * dest - Filter packets by destination node address
        * source - Filter packets by source node address
        * connection - connection class defining radio connection
        """
        while True:
                message = connection.read(source)
                if message != "":
                        split_message = message.split("///", 2)
                        if source != None and (split_message[0] == source.id or split_message[0] == "*"): break # Interpret message
                        elif dest != None and (split_message[1] == dest.id or split_message[1] == "*"): break  # Interpret message            
                        elif dest == None: break  # Interpret message
                

    

