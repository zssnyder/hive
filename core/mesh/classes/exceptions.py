__author__ = "Zack Snyder"
__date__ = "2/15/19"

class CorruptPacketException(Exception):
  def __init__(self, arg):
    self.args = arg

class ReadTimeoutException(Exception):
  def __init__(self, arg):
    self.args = arg

class RequestTimeoutException(Exception):
  def __init__(self, arg):
    self.args = arg

class RelayException(Exception):
  def __init__(self, arg):
    self.args = arg

class ConnectTimeoutException(Exception):
  def __init__(self, arg):
    self.args = arg