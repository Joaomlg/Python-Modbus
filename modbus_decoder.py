import struct

class ModbusDecoder:
  def __init__(self, payload: bytes):
    self.__payload = payload
  
  @property
  def payload(self):
    return self.__payload
  
  