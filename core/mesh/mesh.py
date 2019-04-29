"""Initial script to start the mesh network"""

import threading
import time
import collections
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

from hive.core.mesh.classes import Address
from hive.core.mesh.classes import Node
from hive.core.mesh.classes import MeshConfiguration
from hive.core.mesh.classes import Group
from hive.core.mesh.classes import Packet
from hive.core.mesh.classes import Handler
# Exception module
from hive.core.mesh.classes import exceptions
# Commanding modules
from hive.core.mesh import commands

class mesh(object):

    configuration = MeshConfiguration()

    def __init__(self, configuration=MeshConfiguration()):
        """Initialize mesh object"""

        # Set network configuration values
        self.configuration = configuration

        # Set node configuration
        self.node = Node()
        self.node.connection = self.configuration.peripherals['connection']

        # Packet data structures
        self.requests = collections.deque()
        self.response = {}
        self.handlers = {}
        self.packet_history = collections.deque(maxlen=100)

        # Run connect() to establish a connection
        self.is_connected = False

        # Register network command handlers
        self.register(commands.ConnectCommand, Handler(self._connect_callback, self))
        self.register(commands.GroupCommand, Handler(self._group_callback, self))

        # Start operating on network
        self.stop_event = threading.Event()
        self._responses_lock = threading.Lock()

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
            
            try: 
                # Get raw message and parse it
                message, rssi = self.node.connection.read()
                packet = Packet.try_parse(message)

            except exceptions.ReadTimeoutException as rte:
                logging.debug("No packet read")
                logging.debug(rte.args)

            except exceptions.CorruptPacketException as cpe:
                logging.debug("Packet is corrupted")
                logging.debug(cpe.args)

            except TypeError as te:
                logging.debug("Packet not properly encoded")
                logging.debug(te.args)

            except Exception as exc:
                logging.debug("Unknown exception")
                logging.debug(exc.args)

            else: 
                # Add signal to network
                self.node.network.add_signal(packet.route.last_addr, rssi)
                
                if packet.command.id not in self.packet_history:
                    # Keep track of previous packets
                    self.packet_history.appendleft(packet.command.id)
                    # Add to incoming deque
                    self.node.incoming_deque.appendleft(packet)


    def _share(self):
        """Sends network packets in buffer over network"""

        while not self.stop_event.isSet:
            # Wait for packet to be available
            if len(self.node.outgoing_deque) > 0:

                packet = self.node.outgoing_deque.pop()
                # Keep log of outgoing packets
                self.packet_history.appendleft(packet.command.id)

                self.node.connection.open()
                self.node.connection.write(str(packet) + packet.crc16(), packet.route.next_addr)
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
                    logging.debug('Could not find handler key for request or handler is not registered')
                    logging.debug(ke.args)
                else:
                    # Respond to request
                    response = handler.execute(packet.command, packet.route.source_addr)
                    if response is not None:
                        response.response_id = packet.command.response_id
                        self.respond(response, packet.route.source_addr)

    def _process(self):
        """Process incoming data traffic and send to handler thread or respond"""

        while not self.stop_event.isSet:
            # Process incoming packets
            if (self.node.incoming_deque) > 0:
                packet = self.node.incoming_deque.pop()

                # Handle Command
                if packet.route.dest_addr == self.node.address or str(packet.route.dest_addr) == self.configuration.wildcard:
                    if packet.command.response_id in self.response.keys():
                        
                        with self._responses_lock:
                            # Read event from responses
                            event = self.response[packet.command.response_id]

                            # Pass packet to response dictionary
                            self.response[str(packet.command.response_id)] = packet

                            # Notify proper thread for execution
                            event.set()
                    else:
                        try:
                            if packet.command.parameters['request'] == True: 
                                self.requests.appendleft(packet)
                        except KeyError as ke:
                            print('Command is not a connect request')
                            print(ke.args)
                        except Exception as e:
                            print(e.args)

                # Relay Packet
                if self.node.group.commander == self.node.address:
                    try:
                        self.node.try_relay(packet)
                    except Exception as e:
                        logging.debug(e.args)

            elif int(time.time()) % self.configuration.group_interval == 0 and not self.configuration.is_ground_station:
                
                # Manage network grouping
                self.update_group()

    # ------- Outgoing ----------------

    def try_request(self, command, dest=Address(MeshConfiguration.wildcard), timeout=5.0, responses=1):
        """Register custom handler for event
        
        = returns a dictionary of { source: command } items
        """
        event = threading.Event()
        self.response[str(command.id)] = event
        # Set request to true
        command.parameters['request'] = True

        # Broadcast or transmit to the network
        if str(dest) == self.configuration.wildcard:
            self.node.broadcast(command, self.node.address)
        else:
            self.node.transmit(command, dest, self.node.address)

        # return value
        response_dict = dict()

        while len(response_dict) < responses:
            # Wait for response
            success = event.wait(timeout=timeout) 
            event.clear()

            if success:
                # Perform thread-safe read/write
                with self._responses_lock:
                    # Get packet
                    packet = self.response[str(command.id)]
                    # Pass event back to process thread
                    self.response[str(command.id)] = event

                # Return response command and soure address
                response_dict[str(packet.route.source_addr)] = packet.command
            else: 
                raise exceptions.RequestTimeoutException(('Query did not receive a response in the specified time', command))
        
        # Delete response request
        del self.response[str(command.id)]

        # Return the responses
        return response_dict

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
        
        self._start()

        connection_attempts = 0

        if self.configuration.is_ground_station:
            while connection_attempts < mesh.configuration.connection_timeout:

                # Create a connect command 
                command = commands.ConnectCommand()

                # Broadcast connect command to network
                try: 
                    responses = self.try_request(command, responses=self.configuration.network_size - 1)

                except exceptions.RequestTimeoutException as qte:
                    logging.debug(qte.args)
                    connection_attempts += 1
                else:

                    if connection_attempts >= mesh.configuration.connection_timeout:
                        self.is_connected = False
                        raise exceptions.ConnectTimeoutException(['Could not connect to nodes in network', connection_attempts])
                    else:

                        self.is_connected = True
                        # Return a list of tuples containing the node Address and Parameters 
                        return [(Address(address), responses[address].parameters) for address in responses.keys() ]

        else: 
            # Wait for GS connect command
            while self.configuration.ground_station_address == '': 
                pass

            self.is_connected = True


    def disconnect(self):
        """Disconnect from network"""

        # Send out disconnect packet

        self.is_connected = False

        self._stop()

    # ------ Grouping ----------
            
    def update_group(self):

        # Clear group
        self.node.group.clear()

        # Add all nodes nearby to group
        for address_str in self.node.network.signals.keys():
            if address_str != str(mesh.configuration.ground_station_address):
                self.node.group.add(Address(address_str), self.node.network)

        # Track number of grouping attempts
        grouping_attempts = 0

        while True:

            # Share group with network
            group_command = commands.GroupCommand(self.node.group, self.node.network.score())
            
            try:
                # Request responses of other groups (won't receive response from self or ground station)
                responses = self.try_request(group_command, responses=self.configuration.network_size - 2)
            
            except exceptions.RequestTimeoutException as rte:
                logging.debug("Could not request Group information from network")
                logging.debug(rte.args)

                # Try to group 3 times
                if grouping_attempts < 3:
                    grouping_attempts += 1
                else:  
                    break

            # Update network with other groups
            for source_str in responses.keys():

                parameters = responses[source_str].parameters
                source = Address(source_str)

                # Initialize neighbor group
                addresses = [Address(addr) for addr in parameters['group']]
                group = Group(parameters['id'], Address(parameters['commander']), addresses, int(parameters['size']))
                # Update neighbor group in network
                self.node.network.add_group(source, group)

            # Make a copy of the network before changes
            before = self.node.network.groups.copy()

            # Merge group with other groups nearby
            for address in self.node.group.addresses[:self.configuration.max_group_size + 1]:
                if address != self.node.address: 
                    neighbor_group = self.node.network.get_group(address)
                    self.node.group.merge(address, self.node.address, neighbor_group)
                

            # Update network
            self.node.network.add_group(self.node.address, self.node.group)

            # Check if network has updated
            after = self.node.network.groups
            
            # If grouping hasn't changed, consider the process finished
            if before == after: 
                
                # Set commander for group
                for address in self.node.group.addresses:
                    
                    # Current group commander is not self
                    if str(address) in responses.keys() and str(self.node.group.commander) in responses.keys():
                        score = responses[str(address)].parameters['score']
                        current_score = responses[str(self.node.group.commander)]
                    
                        if score > current_score: self.node.group.commander = address

                    # Current group commander is self
                    elif str(address) in responses.keys() and self.node.group.commander == self.node.address:
                        score = responses[str(address)].parameters['score']
                        current_score = self.node.score()

                        if score > current_score: self.node.group.commander = address

                break
                
            else: logging.debug('Grouping node...')

    # ----------- Handlers -----------------

    def _connect_callback(self, parameters, source):
        """Handler for connect commands"""

        if parameters['GS'] == True and self.configuration.is_ground_station == False:

            MeshConfiguration.ground_station_address = source
            MeshConfiguration.ground_station_ip = parameters['ip']
            MeshConfiguration.max_group_size = parameters['max_group_size']
            MeshConfiguration.network_size = parameters['network_size']

            try:
                # Check if connect request
                if parameters['request'] == False:
                    return None

            except KeyError as ke:
                logging.debug('Command is not a connect request')
                logging.debug(ke.args)

            else:
                return commands.ConnectCommand()

    def _group_callback(self, parameters, source): 
        """Handler for group commands"""
        return commands.GroupCommand(self.node.group, self.node.score())