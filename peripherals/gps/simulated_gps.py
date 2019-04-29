__author__ = 'Zack Snyder'
__date__ = '4/22/19'

from geopy.geocoders import Nominatim

from hive.core.swarm import GPSDevice
from hive.core.swarm import Offset

class SimulatedGPS(GPSDevice):

    def get_coords(self, offset=Offset(0, 0, 0)):
        """Get coordinates of device"""

        geolocator = Nominatim(user_agent='simulated_gps')
        location = geolocator.geocode({
            'street': '8600 University Blvd',
            'city': 'Evansville',
            'state': 'Indiana',
            'country': 'US',
            'postalcode': '47712'
        })

        return location.latitude + offset.lat(), location.longitude + offset.long(location.latitude), 0 + offset.z
        

