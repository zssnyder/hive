"""Address class"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

import uuid

class Address():
    """Node class describing network entity""" 

    def __init__(self, id=None):
        """Initialize instance of address class"""

        if id is not None:
            self.id = id
        else: 
            self.id = uuid.uuid4() # Initialize unique address


    def __eq__(self, other):
        """Overrides equatable relation"""
        if isinstance(other, Address):
            return self.id == other.id
        return False
    
    def __ne__(self, other):
        """Overrides not equatable relation"""
        if isinstance(other, Address):
            return self.id != other.id
        return False