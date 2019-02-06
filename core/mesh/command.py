__author__ = "Zack Snyder"
__date__ = "1/24/19"

import string

from config import Configuration

class Command():
    """Command class defines the types of commands available to transmit"""

    def parse(self, command):
        parts = string.split(command, Configuration.separator)
