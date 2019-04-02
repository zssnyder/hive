"""Connection class plugin interface"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

import threading

class Connection(object):
    """Defines the lowest level radio connection interface. 
    
    Each radio requires a new instance of subclass.

    Needs implementation 
    * open()
    * close()
    * write()
    * read()
    """

    def __init__(self):
        """Initialize instance of connection

        * baud - baud rate (default 9600)
        """
        self.lock = threading.Lock()

    def open(self):
        """Opens connection to mesh network"""
        raise NotImplementedError( 'Needs implementation' )

    def close (self):
        """Closes connection to mesh network"""
        raise NotImplementedError( 'Needs implementation' )

    def write (self, message=""): 
        """Writes message to mesh network
        
        * message - string message to send over the network
        """
        raise NotImplementedError( 'Needs implementation' )

    def read(self):
        """Reads message from mesh network"""
        raise NotImplementedError( 'Needs implementation' )