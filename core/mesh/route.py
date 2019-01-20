"""Route class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

from address import Address

class Route(object):
    """Route class defines message path"""

    def __init__(self, source, next, dest):
        """Initialize instance of route class

        * source: string - address message comes from
        * next: string - address to send message next
        * dest: string - final address to send message to  
        
        Use '*' for both __next__ and __dest__ to denote all nodes
        """
        self.source, self.next, self.dest = source, next, dest


    def get_path(self):
        """Returns the route path to be prefixed to messages"""
        return self.source.id + "///" + self.dest.id + "///"