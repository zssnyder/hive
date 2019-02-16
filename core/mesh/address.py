__author__ = "Zack Snyder"
__date__ = "1/10/2019"

import uuid

class Address(object):
    """Node class describing network entity""" 

    def __init__(self, id=None):
        """Initialize instance of address class"""

        self.id = id
        if id is None:
            self.id = uuid.uuid4() # Initialize unique address

    # ----- Overrrides -------

    def __str__(self):
        """Overrides string representation"""
        return id

    def __eq__(self, other):
        """Overrides equatable relation"""
        if isinstance(other, Address):
            return self.id == other.id
        else: 
            return self.id == other
        return False
    
    def __ne__(self, other):
        """Overrides not equatable relation"""
        if isinstance(other, Address):
            return self.id != other.id
        else: 
            return self.id != other
        return False