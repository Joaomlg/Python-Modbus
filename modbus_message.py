from modbus_utils import calculateDataCRC16, verifyPayloadCRC16

class ModbusMessage:
  def __init__(self, payload: bytes, hasCRC16=True):
    self.__payload = payload
    self.__has_crc16 = hasCRC16

    if self.hasCRC16:
      assert verifyPayloadCRC16(self.payload), Exception('Invalid message CRC16!')
    
  @property
  def payload(self) -> bytes:
    return self.__payload

  @property
  def hasCRC16(self) -> bool:
    return self.__has_crc16
  
  def addCRC16(self) -> None:
    if self.hasCRC16:
      raise Exception('Message already has CRC16!')

    self.__payload += calculateDataCRC16(self.payload)
    self.__has_crc16 = True
  
  def __str__(self) -> str:
    return str(self.payload)

  def __repr__(self) -> str:
    return f'ModbusMessage(payload={str(self.payload)}, hasCRC16={self.hasCRC16})'