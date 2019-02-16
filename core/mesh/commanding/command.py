__author__ = "Zack Snyder"
__date__ = "1/24/19"

import string
import uuid

from ..config import Configuration as config
from hive.core.mesh import Handler
class Command(object):
    """Command class defines the types of commands available to transmit"""

    def __init__(self, id=None, handler=Handler(), parameters=dict()):
        
        self.id = id
        if id is None: 
            self.id = uuid.uuid4()

        self.handler = handler
        self.parameters = parameters



    # ----- Overrides -------

    def __str__(self):
        return config.separator.join([ str(self.id), str(self.handler), str(self.parameters) ])