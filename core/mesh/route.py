"""Route class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

from address import Address
from config import Configuration as config
class Route():
    """Route class defines message path"""

    def __init__(self, next, dest, source):
        """Initialize instance of route class

        * source: string - address message comes from
        * next: string - address to send message next
        * dest: string - final address to send message to  
        
        Use '*' for both __next__ and __dest__ to denote all nodes
        """
        self.next, self.dest, self.source = next, dest, source


    def __str__(self):
        """Returns the route path to be prefixed to messages"""
        return config.separator.join([str(self.next), str(self.dest), str(self.source)])