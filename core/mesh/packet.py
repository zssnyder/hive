__author__ = "Zack Snyder"
__date__ = "2/9/19"

import string
import crcmod.predefined as detect

from address import Address
from commanding.command import Command
from config import Configuration as config
from route import Route

class Packet():
    """Packet class defines the structure of a mesh network packet"""

    def __init__(self, route=None, command=None):
        self.route = route
        self.command = command

    @staticmethod
    def tryParse(packet=""):
        packet_CRC = packet[-4:]
        check_CRC = detect.Crc('crc-16')
        check_CRC.update(packet[:-4])

        if packet_CRC == check_CRC.hexdigest():
            p_components = packet.split(config.separator)

            next = Address(p_components[0])
            dest = Address(p_components[1])
            source = Address(p_components[2])
            route = Route(next, dest, source)
            command = Command(p_components[3], p_components[4], p_components[5])

            return Packet(route=route, command=command)
        else:
            raise Exception('CRC code did not match. Message is corrupted')
        
    def crc16(self):
        crc = detect.Crc('crc-16')
        crc.update(str(self))
        return crc.hexdigest()

    def __str__(self):
        return config.separator.join([str(self.route), str(self.command)])
    