__author__ = "Zack Snyder"
__date__ = "1/23/19"

import queue

from hive.core import mesh
from hive.core.mesh import exceptions

class Node(object):
    """Node class defines and handles all network interactions among nodes in the network"""

    def __init__(self, address=mesh.Address(), group=None, network=None, connection=mesh.Connection()):
        """Initialize instance of Node class"""
        
        # Address
        self.address = address
        
        # Group
        self.group = group
        if group is None:
            self.group = mesh.Group(controller=address, addresses=[address], max_size=1)

        # Network
        self.network = network
        if network is None:
            self.network = mesh.Network(signals={self.address: 0}, groups={self.address: self.group})
        else: 
            self.network.add_signal(self.address, 0)
            self.network.add_group(self.address, self.group)

        # Connection
        self.connection = connection
        
        # Create a command queue to store commands before execution
        self.command_queue = queue.Queue(-1)

        # Create a transmission queue to store packets before transmit
        self.transmit_queue = queue.Queue(-1)

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
            packet = mesh.Packet.try_parse(message)
        except exceptions.ReadTimeoutException as rte:
            print("No packet read")
            print(rte.args)
        except exceptions.CorruptPacketException as cpe:
            print("Packet is corrupted")
            print(cpe.args)
        else: 
            # Add signal to network
            self.network.add_signal(packet.route.last_addr, rssi)
            # Add to command execution queue
            self.command_queue.put(packet.command, block=False)
            # Add to relay queue
            self.transmit_queue.put(packet, block=False)

    # ----- TRANSMISSION -----------

    def try_relay(self, packet):
        """Relays the message on to destination node(s)
        
        * packet - original packet to be relayed
        """
        if str(packet.route.dest_addr) == str(self.address):
            raise exceptions.RelayException(['This is the final destination node and should not be relayed', packet])
        elif self.group.controller != self.address:
            raise exceptions.RelayException(['Not a controller node.', packet])
        elif packet.route.next_addr == self.address or str(packet.route.next_addr) == mesh.config.wildcard:
            if packet.route.dest_addr in self.group.addresses:
                self.transmit(packet.command, packet.route.dest_addr, packet.route.soure_addr)
            else:
                self.broadcast(packet.command, packet.route.source_addr, dest=packet.route.dest_addr)            


    def broadcast(self, command, source, dest=mesh.Address(mesh.config.wildcard)):
        """Sends message to all nodes in network

        If a connection is established, sends message out to all nodes.
        Returns an exception if connection is null or fails.

        * command - command to broadcast
        * source - address of original commanding node
        """
        packet = mesh.Packet(command=command)

        if self.group.controller == self.address: 
            packet.route = mesh.Route(
                next_addr=mesh.Address(mesh.config.wildcard), 
                dest_addr=dest, 
                last_addr=self.address, 
                source_addr=source
            )
        else: 
            packet.route = mesh.Route(
                next_addr=self.group.controller,
                dest_addr=dest,
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
        packet = mesh.Packet(command=command)

        if dest in self.group.addresses:
            packet.route = mesh.Route(
                next_addr=dest, 
                dest_addr=dest, 
                last_addr=self.address, 
                source_addr=source
            )
        else:
            self.broadcast(command, source, dest=dest)
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
        packet = mesh.Packet(command=command)
        packet.route = mesh.Route(
            next_addr=dest,
            dest_addr=dest,
            last_addr=self.address,
            source_addr=self.address
        )

        self.connection.open()
        self.connection.write(str(packet) + packet.crc16)
        self.connection.close()