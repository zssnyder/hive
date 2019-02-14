__author__ = "Zack Snyder"
__date__ = "2/11/19"

import cmd

from .. import Connection

class Console(Connection):

    def open(self):
        """Does not need implementation"""
        pass
    
    def close(self):
        """Does not need implementation"""
        pass

    def write(self, message=""):
        print("Your message is: " + message)

    def read(self):
        return input("Type input here: ")