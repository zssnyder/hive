"""Initial script to start the mesh network"""

from hive.core import mesh
from hive.plugins.connections import console

def start(plugins={'connection': console.ConsoleConnection()}):
    
    # Establish connection type
    console_connection = plugins['connection']

    # Initialize node
    node = mesh.node.Node(connection=console_connection)

    # Connect the node to the network
    node.connect()

    # while node.isConnected():

    #     node.listen()
