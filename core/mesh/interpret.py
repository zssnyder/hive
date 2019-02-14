"""Interprets incoming messages and converts them to the defined commands"""

__author__ = "Zack Snyder"
__date__ = "1/10/2019"

import string
import ast

import commanding
from config import Configuration as config

def interpret(packet=None, rssi=0):
    """Interpret a mesh network message"""

    

    

