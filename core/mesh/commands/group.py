__author__ = 'Zack Snyder'
__date__ = '3/17/19'

from hive.core.mesh.classes import command

class GroupCommand(command.Command):
    """Initiate network grouping"""

    def __init__(self, group):
        """Initialize grouping command"""

        parameters = {
            'id': group.id,
            'group': group.addresses,
            'size': group.max_size
        }

        super(GroupCommand, self).__init__(parameters=parameters)