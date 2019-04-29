__author__ = "Zack Snyder"
__date__ = "2/9/19"

from hive.core.mesh.classes import Address

class Handler(object):
    """Handler class interprets and executes commands"""

    def __init__(self, callback, owner):
        """Initialize Handler class
        
        * callback = function to call when receiving this command
        """
        self.callback = callback
        self.owner = owner

    def execute(self, parameters=dict(), source=Address()):
        """Handles execution of specific command"""
        return self.callback(parameters, source, self=self.owner)
        # raise NotImplementedError( 'Needs implementation' )

    def __str__(self):
        return type(self).__name__