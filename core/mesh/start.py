"""Initial script to start the mesh network"""

from hive.plugins.connections import console
from hive.core.mesh import classes as mesh

def start(plugins={'connection': console.ConsoleConnection()}):
    
    # Establish connection type
    console_connection = plugins['connection']

    # Initialize node
    node = mesh.Node(connection=console_connection)

    # Connect the node to the network
    node.connect()

    while True:

        node.listen()
