__author__ = "Zack Snyder"
__date__ = "2/9/19"

class Handler(object):
    """Handler class interprets and executes commands"""

    def execute(self, parameters=dict()):
        """Handles execution of specific command"""
        raise NotImplementedError( 'Needs implementation' )

    def __str__(self):
        return type(self).__name__