__author__ = 'Zack Snyder'
__date__ = '3/15/19'

import threading
import logging
# Mesh
from hive.core.mesh import Handler
from hive.core.mesh import exceptions
# Classes
from hive.core.swarm import Drone
from hive.core.swarm import SwarmConfiguration
from hive.core.swarm import Formation
from hive.core.swarm import Status
from hive.core.swarm import Position
# Commands
from hive.core.swarm.commands import GPSCommand
from hive.core.swarm.commands import PositionCommand
from hive.core.swarm.commands import StatusCommand

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

class swarm(object):

    def __init__(self, mesh, configuration=SwarmConfiguration()):
        """Initialize a swarm object"""

        self.mesh = mesh
        self.configuration = configuration

        self.drone = Drone(
            self.mesh.node, 
            self.configuration.peripherals['gps']
        )

        self.formation = Formation()
        self.reference_pos = Position(*self.drone.location())

        # Register callback
        self.register(PositionCommand, Handler(self._position_callback, self))
        self.register(StatusCommand, Handler(self._status_callback, self))
        self.register(GPSCommand, Handler(self._gps_callback, self))

        self._update_thread = None

    # ------ Positioning Thread ------------

    def _start(self):
        # Begin updating thread
        if not self._update_thread.isAlive:
            self._update_thread = threading.Thread(name='Update Thread', target=self._update)
            self._update_thread.start()

    def _update(self):

        while not self.mesh.is_ground_station():
            if self.drone.get_offset_from(*self.reference_pos.to_tuple()) == self.drone.offset:
                self.drone.status = Status.idle
            elif len(self.reference_pos) > 1:
                self.drone.status = Status.processing
            elif len(self.reference_pos) == 0: 
                self.drone.status = Status.ready
            else:
                self.drone.status = Status.running
                # Call Move method here
    

    def register(self, cmd_type, handler):
        """Register a handler for a command type"""
        self.mesh.register(cmd_type, handler)

    def get_status(self):
        """Return statuses of all drones in swarm"""
        latitude, longitude, altitude = self.drone.location()
        command = GPSCommand(latitude, longitude, altitude)
        # Handle GCS status request
        if self.mesh.configuration.is_ground_station:
            try:
                responses = self.mesh.try_request(command, responses=self.configuration.swarm_size)
            except exceptions.RequestTimeoutException as rte:
                logging.debug('GCS GPS command failed: %s', rte.args)
                return None
            else: 
                return [(source, responses[source].parameters) for source in responses.keys()]
        # Handle commander status request (in progress)
        # elif self.drone.is_commander():
        #     drones = []
        #     for address in self.drone.group.addresses:
        #         if address != self.drone.address:
        #             try:
        #                 source, command = self.mesh.try_request(command, address)
        #             except exceptions.RequestTimeoutException as rte:
        #                 logging.debug('Commander GPS command failed: %s', rte.args)
        #             else:
        #                 drones.append((source, command.parameters))
        #     return drones

    def form(self, formation):
        """Forms a swarm into a 3D formation"""

        # Get current GPS location and add it to positioning packet
        command = PositionCommand(formation, self.configuration.max_speed)

        for group in self.mesh.node.network.groups:

            is_error = True

            while is_error:

                try:
                    response = self.mesh.try_request(command, group.commander)
                except exceptions.RequestTimeoutException as rte:
                    logging.debug('Could not command group %s: %s', group, rte.args)
                else:
                    is_error = False

    # --------- Handlers ------------------

    def _gps_callback(self, parameters, source):
        """Handler for gps commands"""

        latitude = parameters['lat']
        longitude = parameters['long']
        altitude = parameters['alt']

        # Update current offset
        if self.drone.is_commander() and self.mesh.configuration.ground_station_address == source:
            offset = self.drone.get_offset_from(latitude, longitude, altitude)
        elif not self.drone.is_commander() and self.mesh.node.group.commander == source:
            offset = self.drone.get_offset_from(latitude, longitude, altitude)

        # WORK IN PROGRESS

        # Update current formation
        # if self.drone.is_commander():
        #     drones = self.get_status()

        return StatusCommand(self.drone.offset.x, self.drone.offset.y, self.drone.offset.z, self.drone.status)

    def _position_callback(self, parameters, source): 
        """Handler for position commands"""

        if not self.mesh.configuration.is_ground_station:

            if self.drone.is_commander(): 
                
                offsets = parameters['off']
                self.configuration.max_speed = parameters['vel']
                
                for offset in offsets:
                    position = Position()
                    formation = Formation(positions)

            else: return

    def _status_callback(self, parameters, source):
        """Handler for status commands"""
        
        if self.mesh.configuration.is_ground_station:

        # else:



            return StatusCommand
        
        