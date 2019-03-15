__author__ = "Zack Snyder"
__date__ = "1/24/19"

import string
import uuid
import ast
import importlib

from hive.core.mesh.classes import handler
from hive.core.mesh import mesh

class Command(object):
    """Command class defines the types of commands available to transmit"""

    def __init__(self, id=None, response_id=None, parameters=dict()):
        """Initializes instance of Command class
        
        * id - unique identifier for each command
        * handler - the type of hanlder required to execute command
        * parameters - dictionary of key, value pairs required by handler
        """
        self.id = id
        if id is None: 
            self.id = uuid.uuid4().hex

        self.response_id = response_id
        if response_id is None:
            self.response_id = id

        self.parameters = parameters

        self.parameters['name'] = type(self).__name__

    @classmethod
    def from_string(cls, id="", response_id="", parameters=""):
        # Parse out handler module
        # handler_module = importlib.import_module(config.handler_module)
        # handler = getattr(handler_module, handler)()

        # Evaluate string dictionary
        param_dict = ast.literal_eval(parameters)
        return cls(id=id, response_id=response_id, parameters=param_dict)

    # ----- Overrides -------

    def __str__(self):
        return mesh.configuration.separator.join([ str(self.id), str(self.response_id), str(self.parameters) ])