"""Initial script to start the mesh network"""

import threading
import time
import collections

from hive.core.mesh.classes import Address
from hive.core.mesh.classes import Command
from hive.core.mesh.classes import Node
from hive.core.mesh.classes import Configuration
from hive.core.mesh.classes import Group
# Exception module
from hive.core.mesh.classes import exceptions
# Commanding modules
from hive.core.mesh import commands
from hive.core.mesh import handlers

# Commands
from hive.core.mesh import commands

class mesh(object):

    configuration = Configuration()

    def __init__(self, configuration=Configuration()):
        """Initialize mesh object"""

        # Set node configuration
        self.node = Node()
        self.node.connection = self.configuration.plugins['connection']

        # Set network configuration values
        mesh.configuration = configuration

        # Response dictionary for passing packets
        self.requests = collections.deque()
        self.response = {}
        self.handlers = {}

        # Run connect() to establish a connection
        self.is_connected = False

        # Register network command handlers
        self.register(commands.GroupCommand, handlers.GroupHandler(self.node))

        # Start operating on network
        self.stop_event = threading.Event()

        self._receive_thread = threading.Thread()
        self._share_thread = threading.Thread()
        self._process_thread = threading.Thread()
        self._handler_thread = threading.Thread()
        self._start()

    # ----- Private Networking Threads ----------
    def _start(self):
        """Starts up networking threads"""

        # Receive data from network
        if not self._receive_thread.isAlive:
            self._receive_thread = threading.Thread(name='Receive Thread', target=self._receive)
            self._receive_thread.start()

        # Share data with network
        if not self._share_thread.isAlive:
            self._share_thread = threading.Thread(name='Share Thread', target=self._share)
            self._share_thread.start()
        
        # Process incoming packets
        if not self._process_thread.isAlive:
            self._process_thread = threading.Thread(name='Process Thread', target=self._process)
            self._process_thread.start()

        # Hanlder incoming requests
        if not self._handler_thread.isAlive:
            self._handler_thread = threading.Thread(name='Handler Thread', target=self._handle)
            self._handler_thread.start()

    def _stop(self):
        """Stop networking threads"""
        # Send stop event to all subthreads
        self.stop_event.set()
        # Wait for subthreads to end
        self._receive_thread.join()
        self._share_thread.join()
        self._handler_thread.join()
        self._process_thread.join()
        # Reset stop event flag so network can be started again
        self.stop_event.clear()

    def _receive(self):
        """Retrieves network data and stores in buffers"""

        while not self.stop_event.isSet:
            self.node.listen()


    def _share(self):
        """Sends network packets in buffer over network"""

        while not self.stop_event.isSet:
            # Wait for packet to be available
            if len(self.node.outgoing_deque) > 0:

                packet = self.node.outgoing_deque.pop()

                self.node.connection.open()
                self.node.connection.write(str(packet) + packet.crc16())
                self.node.connection.close()

    def _handle(self):
        """Handles incoming requests from the network"""
        
        while not self.stop_event.isSet:
            if len(self.requests) > 0:

                packet = self.requests.pop()

                try:
                    # Get registered handler
                    command_type = packet.command.parameters['name']
                    handler = self.handlers[command_type]
                except KeyError as ke:
                    print('Could not find handler key for request or handler is not registered')
                    print(ke.args)
                else:
                    # Respond to request
                    parameters = handler.execute(packet.command, packet.route.source_addr)
                    if parameters is not None:
                        response_command = Command(response_id=packet.command.response_id, parameters=parameters)
                        self.respond(response_command, packet.route.source_addr)

    def _process(self):
        """Process incoming data traffic and send to handler thread or respond"""

        while not self.stop_event.isSet:
            if (self.node.incoming_deque) > 0:
                packet = self.node.incoming_deque.pop()

                # Handle Command
                if packet.route.dest_addr == self.node.address or str(packet.route.dest_addr) == self.configuration.wildcard:
                    if packet.command.response_id in self.response.keys():
                        event = self.response[packet.command.response_id]

                        # Pass packet to response dictionary
                        self.response[str(packet.command.response_id)] = packet
                        # Notify proper thread for execution
                        event.set()
                    else:
                        self.requests.appendleft(packet)
                        

                # Relay Packet
                if self.node.group.controller == self.node.address:
                    try:
                        self.node.try_relay(packet)
                    except Exception as e:
                        print(e.args)

    # ------- Outgoing ----------------

    def try_request(self, command, dest=Address(mesh.configuration.wildcard), timeout=5.0):
        """Register custom handler for event"""
        event = threading.Event()
        self.response[str(command.id)] = event
        # Set request to true
        command.parameters['request'] = True

        # Broadcast or transmit to the network
        if str(dest) == self.configuration.wildcard:
            self.node.broadcast(command, self.node.address)
        else:
            self.node.transmit(command, dest, self.node.address)

        # Wait for response
        success = event.wait(timeout=timeout) 

        if success:
            # Get packet
            packet = self.response[str(command.id)]
            # Delete packet from record
            del self.response[str(command.id)]
            # Return response command and soure address
            return packet.command, packet.route.source_addr
        else: 
            raise exceptions.RequestTimeoutException(('Query did not receive a response in the specified time', command))


    def respond(self, command, dest):
        """Respond to a given command"""
        
        # Send response
        command.parameters['response'] = True
        self.node.transmit(command, dest, self.node.address)


    # ------- Register ------------

    def register(self, cmd_type, handler):
        """Register handlers for responding to network requests"""
        
        self.handlers[cmd_type.__name__] = handler

    # ------- Connect -------------

    def connect(self):
        """Connect node to group network"""
        
        self.is_connected = True
        self._start()

        connection_attempts = 0

        while connection_attempts < mesh.configuration.connection_timeout:

            # Create a connect command 
            command = commands.ConnectCommand()

            # Broadcast connect command to network
            try: 
                response, source = self.try_request(command)
            except exceptions.RequestTimeoutException as qte:
                print(qte.args)
                connection_attempts += 1
            else:

                self.is_connected = True

                # Set configuration
                self.configuration.ground_station_address = source
                self.configuration.ground_station_ip = response.parameters['ip']
                self.configuration.max_group_size = response.parameters['max_group_size']

        if connection_attempts >= mesh.configuration.connection_timeout:
            self.is_connected = False
            raise exceptions.ConnectTimeoutException(['Could not reach ground station', connection_attempts])

    def disconnect(self):
        """Disconnect from network"""

        # Send out disconnect packet

        self.is_connected = False

        self._stop()