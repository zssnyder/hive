__author__ = 'Zack Snyder'
__date__ = '4/25/19'

from enum import Enum

class Status(Enum):

    idle = 'idle'
    processing = 'processing'
    ready = 'ready'
    moving = 'moving'
