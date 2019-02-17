__author__ = "Zack Snyder"
__date__ = "1/24/19"

import string
import uuid

from hive.core.mesh import Configuration as config, Handler

class Command(object):
    """Command class defines the types of commands available to transmit"""

    def __init__(self, id=None, handler=Handler(), parameters=dict()):
        """Initializes instance of Command class
        
        * id - unique identifier for each command
        * handler - the type of hanlder required to execute command
        * parameters - dictionary of key, value pairs required by handler
        """
        self.id = id
        if id is None: 
            self.id = uuid.uuid4()

        self.handler = handler
        self.parameters = parameters

    # ----- Overrides -------

    def __str__(self):
        return config.separator.join([ str(self.id), str(self.handler), str(self.parameters) ])