__author__ = "Zack Snyder"
__date__ = "1/23/19"

import Queue

from hive.core.mesh import Address, Configuration as config, Connection, Group, Network, Packet, Route
from commanding import Command
from exceptions import CorruptPacketException, ReadTimeoutException

class Node(object):
    """Node class defines and handles all network interactions among nodes in the network"""

    def __init__(self, address=Address(), group=None, network=None, connection=Connection()):
        """Initialize instance of Node class"""
        
        # Address
        self.address = address
        
        # Group
        self.group = group
        if group is None:
            self.group = Group(controller=address, addresses=[address], max_size=1)

        # Network
        self.network = network
        if network is None:
            self.network = Network(signals={self.address: 0}, groups={self.address: self.group})
        else: 
            self.network.add_signal(self.address, 0)
            self.network.add_group(self.address, self.group)

        # Connection
        self.connection = connection
        
        # Create a command queue to store commands before execution
        self.command_queue = Queue.Queue(-1)

        # Create a transmission queue to store packets before transmit
        self.transmit_queue = Queue.Queue(-1)

    # ------ CONNECTION -----------

    def connect(self):
        """Connect node to group network"""
        pass
        # command = Command.connect()
        # broadcast()

    def disconnect(self):
        pass

    # ----- RECEPTION --------------

    def listen(self):
        """Listen for messages on network
        
        * address - address of listening node
        * connection - connection class defining radio connection
        """
        try: 
            message, rssi = self.connection.read()
            packet = Packet.tryParse(message)

        except ReadTimeoutException, rte:
            print("No packet read")
            print(rte.args)
        except CorruptPacketException, cpe:
            print("Packet is corrupted")
            print(cpe.args)
        else: 
            # Add signal to network
            self.network.add_signal(packet.last_addr(), rssi)
            # Add to command execution queue
            self.command_queue.put(packet.command, block=False)
            # Add to relay queue
            self.transmit_queue.put(packet, block=False)

    # ----- TRANSMISSION -----------

    def relay(self, packet):
        """Relays the message on to destination node(s)
        
        * packet - original packet to be relayed
        """

        if str(packet.dest_addr()) == config.wildcard:
            self.broadcast(packet.command, packet.source_addr())
        elif packet.dest_addr() in self.group.addresses:
            self.transmit(packet.command, packet.dest_addr(), packet.source_addr())
        else:
            raise Exception('Packet should not be relayed')


    def broadcast(self, command, source):
        """Sends message to all nodes in network

        If a connection is established, sends message out to all nodes.
        Returns an exception if connection is null or fails.

        * command - command to broadcast
        * source - address of original commanding node
        """
        packet = Packet(command=command)

        if self.group.controller == self.address: 
            packet.route = Route(
                next_addr=Address(config.wildcard), 
                dest_addr=Address(config.wildcard), 
                last_addr=self.address, 
                source_addr=source
            )
        else: 
            packet.route = Route(
                next_addr=self.group.controller,
                dest_addr=Address(config.wildcard),
                last_addr=self.address, 
                source_addr=source
            )

        self.connection.open()
        self.connection.write(str(packet) + packet.crc16)
        self.connection.close()

    def transmit(self, command, dest, source):
        """Sends message to given destintaion via the mesh network

        If a connection is established, sends message out on the given connection.
        Returns an exception if connection is null or fails.

        * command - command to transmit
        * dest - final destination node address
        * source - address of original commanding node
        """
        packet = Packet(command=command)

        if dest in self.group.addresses:
            packet.route = Route(
                next_addr=dest, 
                dest_addr=dest, 
                last_addr=self.address, 
                source_addr=source
            )
        else:
            self.broadcast(command, source)
            return

        self.connection.open()
        self.connection.write(str(packet) + packet.crc16) # Uses next in route to carry the message to destination
        self.connection.close()

    def beam(self, command, dest):
        """Sends message directly to destination address

        Sends message regardless of connection.
        If no ACK is receieved, exception is thrown.

        * command - command to beam
        * dest - final destination node address
        """
        packet = Packet(command=command)
        packet.route = Route(
            next_addr=dest,
            dest_addr=dest,
            last_addr=self.address,
            source_addr=self.address
        )

        self.connection.open()
        self.connection.write(str(packet) + packet.crc16)
        self.connection.close()