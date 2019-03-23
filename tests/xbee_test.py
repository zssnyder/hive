__author__ = 'Zack Snyder'
__date__ = '3/22/19'

from hive.peripherals.connections import XBeeConnection

xbee = XBeeConnection('/dev/tty.usbserial-AK05ZLDC')

xbee.open()
xbee.write('Suck it Trebeck..........................................................')
xbee.close()