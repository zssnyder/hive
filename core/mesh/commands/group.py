__author__ = 'Zack Snyder'
__date__ = '3/17/19'

from hive.core.mesh.classes import command

class GroupCommand(command.Command):
    """Initiate network grouping"""

    def __init__(self, node):
        """Initialize grouping command"""

        parameters = {
            'id': node.group.id,
            'group': node.group.addresses,
            'size': node.group.max_size
        }

        super(GroupCommand, self).__init__(parameters=parameters)