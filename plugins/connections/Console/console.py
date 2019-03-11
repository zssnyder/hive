__author__ = "Zack Snyder"
__date__ = "2/11/19"

import logging

from hive.core.mesh.classes import Connection

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class ConsoleConnection(Connection):

    def open(self):
        """Does not need implementation"""
        pass
    
    def close(self):
        """Does not need implementation"""
        pass

    def write(self, message=""):
        logging.debug('Output: %s', message)

    def read(self):
        return input('Input: ')