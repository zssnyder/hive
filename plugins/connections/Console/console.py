__author__ = "Zack Snyder"
__date__ = "2/11/19"

from hive.core.mesh import Connection

class ConsoleConnection(Connection):

    def open(self):
        """Does not need implementation"""
        pass
    
    def close(self):
        """Does not need implementation"""
        pass

    def write(self, message=""):
        print("Output: " + message)

    def read(self):
        return input("Input: ")