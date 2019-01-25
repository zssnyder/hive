"""Connection class plugin interface"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

class Connection():
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

        * baud - radio baud rate
        * protocol - string identifier 'UART', 'I2C', 'SPI'
        """
        # self.baud = baud
        # self.protocol = protocol
        pass

    def open(self):
        """Opens connection to mesh network"""
        raise NotImplementedError( 'Needs implementation' )

    def close (self):
        """Closes connection to mesh network"""
        raise NotImplementedError( 'Needs implementation' )

    def write (self, message, dest): 
        """Writes message to mesh network
        
        * message - string message to send over the network
        """
        raise NotImplementedError( 'Needs implementation' )

    def read(self, source):
        """Reads message from mesh network"""
        raise NotImplementedError( 'Needs implementation' )