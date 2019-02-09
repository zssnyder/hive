__author__ = "Zack Snyder"
__date__ = "1/24/19"

import string
import uuid

from ..config import Configuration as config

class Command():
    """Command class defines the types of commands available to transmit"""

    codes = {}

    def __init__(self, id=None, code="", message=""):
        
        self.id = id
        if id is None: 
            self.id = uuid.uuid4()

        self.code = code
        self.message = message

    def __str__(self):
        return config.separator.join([ str(self.id), str(self.code), str(self.message) ])