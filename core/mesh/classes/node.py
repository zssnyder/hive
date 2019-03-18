__author__ = "Zack Snyder"
__date__ = "1/23/19"

import threading
from collections import deque

# Core 
from hive.core.mesh import mesh
from hive.core.mesh import classes
from hive.core.mesh.classes import exceptions

class Node(object):
    """Node class defines and handles all network interactions among nodes in the network"""

    def __init__(self, address=classes.Address(), group=None, network=None, connection=classes.Connection()):
        """Initialize instance of Node class"""

        # Address
        self.address = address
        
        # Group
        self.group = group
        if group is None:
            self.group = classes.Group(controller=address, addresses=[address], max_size=mesh.configuration.max_group_size)

        # Network
        self.network = network
        if network is None:
            self.network = classes.Network(signals={str(self.address): 0}, groups={str(self.address): self.group})
        else: 
            self.network.add_signal(self.address, 0)
            self.network.add_group(self.address, self.group)

        # Connection
        self.connection = connection

        # Double-ended Queue Buffers
        self.incoming_deque = deque()
        self.outgoing_deque = deque()

        # Create a history table of past commands {Command.id: Source Address}
        self.packet_history = {}

        # Is node connected to the network
        self.is_connnected = False

    # ------ Grouping ----------
            
    def update_group(self):

        # Clear group
        for address in self.group.addresses:
            self.group.remove(address)

        # Add all nodes nearby to group
        for address_str in self.network.signals.keys():
            if address_str != str(mesh.configuration.ground_station_address):
                self.group.add(classes.Address(address_str), self.network)


        while True:
            # Make a copy of the group structure before changes
            before = self.network.groups.copy()

            # Merge group with other groups nearby
            for address in self.group.addresses[:mesh.configuration.max_group_size + 1]:
                if address != self.address: 
                    neighbor_group = self.network.get_group(address)
                    self.group.merge(address, self.address, neighbor_group)
                

            # Update global storage
            self.network.add_group(self.address, self.group)

            # Check if network has updated
            after = self.network.groups
            if before == after: break
            else: print('Grouping node...')

    def disconnect(self):
        
        # command = disconnect.DisconnectCommand()
        # self.broadcast(command, self.address)

        self.is_connnected = False

    # ----- RECEPTION --------------

    def listen(self):

        try: 
            # Read Connection
            message, rssi = self.connection.read()
            packet = classes.Packet.try_parse(message)

        except exceptions.ReadTimeoutException as rte:
            print("No packet read")
            print(rte.args)

        except exceptions.CorruptPacketException as cpe:
            print("Packet is corrupted")
            print(cpe.args)

        except TypeError as te:
            print("Packet not properly encoded")
            print(te.args)

        except Exception as exc:
            print("Unknown exception")
            print(exc.args)

        else: 
            # Add signal to network
            self.network.add_signal(packet.route.last_addr, rssi)

            # Add to incoming deque
            self.incoming_deque.appendleft(packet)

    # ----- TRANSMISSION -----------

    def try_relay(self, packet):
        """Relays the message on to destination node(s)
        
        * packet - original packet to be relayed
        """
        if str(packet.route.dest_addr) == str(self.address):
            raise exceptions.RelayException(['This is the final destination node and should not be relayed', packet])
        elif self.group.controller != self.address:
            raise exceptions.RelayException(['Not a controller node.', packet])
        elif packet.route.next_addr == self.address or str(packet.route.next_addr) == mesh.configuration.wildcard:
            if packet.route.dest_addr in self.group.addresses:
                self.transmit(packet.command, dest=packet.route.dest_addr, source=packet.route.soure_addr)
            else:
                self.broadcast(packet.command, dest=packet.route.dest_addr, source=packet.route.source_addr)      
        else:
            raise Exception(['Unknown relay case', packet])      


    def broadcast(self, command, source, dest=classes.Address(mesh.configuration.wildcard)):
        """Sends message to all nodes in network

        If a connection is established, sends message out to all nodes.
        Returns an exception if connection is null or fails.

        * command - command to broadcast
        * source - address of original commanding node
        """
        packet = classes.Packet(command=command)

        if self.group.controller == self.address: 
            packet.route = classes.Route(
                next_addr=classes.Address(mesh.configuration.wildcard), 
                dest_addr=dest, 
                last_addr=self.address, 
                source_addr=source 
            )
        else: 
            packet.route = classes.Route(
                next_addr=self.group.controller,
                dest_addr=dest,
                last_addr=self.address, 
                source_addr=source
            )

        self.outgoing_deque.appendleft(packet)

    def transmit(self, command, dest, source):
        """Sends message to given destintaion via the mesh network

        If a connection is established, sends message out on the given connection.
        Returns an exception if connection is null or fails.

        * command - command to transmit
        * dest - final destination node address
        * source - address of original commanding node
        """
        packet = classes.Packet(command=command)

        if dest in self.group.addresses:
            packet.route = classes.Route(
                next_addr=dest, 
                dest_addr=dest, 
                last_addr=self.address, 
                source_addr=source
            )
        else:
            self.broadcast(command, source, dest=dest)
            return

        self.outgoing_deque.appendleft(packet)

    def beam(self, command, dest):
        """Sends message directly to destination address

        Sends message regardless of connection.
        If no ACK is receieved, exception is thrown.

        * command - command to beam
        * dest - final destination node address
        """
        packet = classes.Packet(command=command)
        packet.route = classes.Route(
            next_addr=dest,
            dest_addr=dest,
            last_addr=self.address,
            source_addr=self.address
        )

        self.outgoing_deque.appendleft(packet)