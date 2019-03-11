__author__ = "Zack Snyder"
__date__ = "1/24/19"

import string
import uuid
import ast
import importlib

from hive.core.mesh.classes import handler
from hive.core.mesh.classes.config import Configuration as config

class Command(object):
    """Command class defines the types of commands available to transmit"""

    def __init__(self, id=None, handler=handler.Handler(), parameters=dict()):
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

    @classmethod
    def fromString(cls, id="", handler="", parameters=""):
        # Parse out handler module
        handler_module = importlib.import_module(config.handler_module)
        handler = getattr(handler_module, handler)()
        # Evaluate string dictionary
        param_dict = ast.literal_eval(parameters)
        return cls(id=id, handler=handler, parameters=param_dict)

    def handle(self):
        """Executes handler for command"""
        self.handler.execute(self.parameters)

    # ----- Overrides -------

    def __str__(self):
        return config.separator.join([ str(self.id), str(self.handler), str(self.parameters) ])