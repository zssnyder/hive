"""Initial script to start the mesh network"""

import threading
import logging

from hive.plugins.connections import console
from hive.core.mesh import classes as mesh
from hive.core.mesh.classes import exceptions
    

def start(wilcard='*', separator='///', handler_module='hive.plugins.handlers', 
            plugins={'connection': console.ConsoleConnection()}):
    
    # Set configuration
    mesh.config.wildcard = wilcard
    mesh.separator = separator
    mesh.config.handler_module = handler_module

    # Initialize node
    node = mesh.Node(connection=plugins['connection'])

    # Connect the node to the network
    node.connect()

    while True:

        try: 
            # Read Connection
            message, rssi = node.connection.read()
            packet = mesh.Packet.try_parse(message)

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
            node.network.add_signal(packet.route.last_addr, rssi)

            # Handle Command
            if packet.route.dest_addr == node.address or str(packet.route.dest_addr) == mesh.config.wildcard:
                command_thread = threading.Thread(target=packet.command.handle)
                command_thread.start()

            # Relay Packet
            if node.group.controller == node.address:
                relay_thread = threading.Thread(target=node.try_relay, args=(packet,))     
                relay_thread.start()