"""Address class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

import uuid

class Address():
    """Node class describing network entity""" 

    def __init__(self, id=""):
        """Initialize instance of address class"""

        if (id != ""):
            self.id = id
        else: 
            self.id = uuid.uuid4() # Initialize unique address


    def __eq__(self, other):
        """Overrides equatable relation"""
        if isinstance(other, Address):
            return self.id == other.id
        return False