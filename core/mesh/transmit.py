"""Handler for sending messages in the Hive mesh network"""


__author__ = "Zack Snyder"


from network import Network
from connection import Connection
from route import Route
from address import Address


def ping(source, connection):
    """Sends out a message requesting a response from all other nodes in network"""
    message = "ping"
    universal = Address("*")
    route = Route(source, universal, universal)
    
    connection.open()
    connection.write(route.get_path() + message, route.dest)
    connection.close()

def broadcast(message, connection, network):
    """Sends message to all nodes in network

    If a connection is established, sends message out to all nodes.
    Returns an exception if connection is null or fails.

    * message - string message to send
    * connection - connection class defining radio connection
    * network - network topology to use
    """
    for route in network.routes:
        transmit(message, route.dest, connection, network)

def transmit(message, dest, connection, network):
    """Sends message to given destintaion via the mesh network

    If a connection is established, sends message out on the given connection.
    Returns an exception if connection is null or fails.

    * message - string message to send
    * dest - final destination node address
    * connection - connection class defining radio connection         
    * network -
    """
    route = network.get_route(dest)

    connection.open()
    connection.write(route.get_path() + message, route.next) # Uses next in route to carry the message to destination
    connection.close()

def beam(message, dest, connection, network):
    """Sends message directly to destination address

    Sends message regardless of connection.
    If no ACK is receieved, exception is thrown.
    * 
    """
    route = network.get_route(dest)

    connection.open()
    connection.write(route.get_direct_path() + message, route.dest) # Uses destination instead of next in route
    connection.close()