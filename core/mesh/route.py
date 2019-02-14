"""Route class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

from address import Address
from config import Configuration as config
class Route():
    """Route class defines message path"""

    def __init__(self, next_addr, dest_addr, last_addr, source_addr):
        """Initialize instance of route class

        * next: string - address to send message next
        * dest: string - final address to send message to  
        * last: string - last address message was sent from
        * source: string - address original message comes from

        Use wildcard char for  next_addr  and  dest_addr  to denote all nodes
        """
        self.next_addr, self.dest_addr, self.last_addr, self.source_addr = next_addr, dest_addr, last_addr, source_addr
    
    @classmethod
    def fromString(cls, next_id="", dest_id="", last_id="", source_id=""):
        return cls(Address(id=next_id), Address(id=dest_id), Address(id=last_id), Address(id=source_id))

    def __str__(self):
        """Returns the route path to be prefixed to messages"""
        return config.separator.join([str(self.next_addr), str(self.dest_addr), str(self.last_addr), str(self.source_addr)])
