__author__ = "Zack Snyder"
__date__ = "2/11/19"

import logging
import uuid
import random

from hive.core.mesh import classes as mesh

from hive.core.mesh.commands import ConnectCommand


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

class ConsoleConnection(mesh.Connection):

    address = mesh.Address('console_connection')

    def open(self):
        """Does not need implementation"""
        pass
    
    def close(self):
        """Does not need implementation"""
        pass

    def write(self, message=""):
        logging.debug('Output: %s', message)

    def read(self):
        parameters = input('Input: ')
        # Route
        route = mesh.Route.from_string('*', '*', str(self.address), str(self.address))
        # Command
        command = ConnectCommand()
        command.parameters = parameters
        # Packet
        packet = mesh.Packet(route, command)
        return str(packet) + packet.crc16(), random.randint(-100, -1)