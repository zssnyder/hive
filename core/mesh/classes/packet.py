__author__ = "Zack Snyder"
__date__ = "2/9/19"

import string
import crcmod.predefined as detect

from hive.core.mesh.classes import Configuration
from hive.core.mesh import classes
from hive.core.mesh.classes import exceptions

class Packet(object):
    """Packet class defines the structure of a mesh network packet"""

    def __init__(self, route=None, command=None):
        self.route = route
        self.command = command

    @staticmethod
    def try_parse(packet=""):
        packet_CRC = packet[-4:]
        check_CRC = detect.Crc('crc-16')
        check_CRC.update((packet[:-4]).encode('utf-8'))

        if packet_CRC == check_CRC.hexdigest():
            p_components = packet[:-4].split(Configuration.separator)

            route = classes.Route.from_string(p_components[0], p_components[1], p_components[2], p_components[3])
            command = classes.Command.from_string(p_components[4], p_components[5], p_components[6])

            return Packet(route=route, command=command)
        else:
            raise exceptions.CorruptPacketException(['CRC code did not match.', packet])
        
    def crc16(self):
        crc = detect.Crc('crc-16')
        crc.update(str(self).encode('utf-8'))
        return crc.hexdigest()

    # ----- Route accessors ----

    def next_addr(self):
        return self.route.next_addr

    def dest_addr(self):
        return self.route.dest_addr

    def last_addr(self):    
        return self.route.last_addr

    def source_addr(self):
        return self.route.source_addr

    # ----- Command accessors --------

    def command_id(self):
        return self.command.id

    def command_code(self):
        return self.command.code

    def command_param(self):
        return self.command.parameters

    # ----- Overrides --------

    def __str__(self):
        return Configuration.separator.join([str(self.route), str(self.command)])
    