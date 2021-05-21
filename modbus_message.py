import struct

from modbus_utils import calculateDataCRC16, verifyPayloadCRC16
from modbus_constants import LITTLE_ENDIAN, BIG_ENDIAN

class ModbusMessageBuilder:
  def __init__(self, endian=BIG_ENDIAN):
    self.__message_endian = endian
    self.__struct_format = bytes()
    self.__payload_buffer = list()

  def setPayload(self, payload: bytes):
    self.__payload = payload

  def addChar(self, char: int):
    self.__struct_format += 'b'
    self.__payload_buffer.append(char)
  
  def addUnsignedChar(self, char: int):
    self.__struct_format += 'B'
    self.__payload_buffer.append(char)

  def addShort(self, short: int):
    self.__struct_format += 'h'
    self.__payload_buffer.append(short)
  
  def addUnsignedShort(self, short: int):
    self.__struct_format += 'H'
    self.__payload_buffer.append(short)
  
  def build(self) -> bytes:
    struct_format_with_endian = self.__message_endian + self.__struct_format
    message_payload_data = struct.pack(struct_format_with_endian, *self.__payload_buffer)
    message_payload_crc16 = calculateDataCRC16(message_payload_data)
    return message_payload_data + message_payload_crc16

class ReadMessageBuilder:
  def __init__(self, slave_address, function_code, start_register, number_of_registers):
    self.__slave_address = slave_address
    self.__function_code = function_code
    self.__start_register = start_register
    self.__number_of_registers = number_of_registers

    self.__assertDeviceAddress()
    self.__assertFunctionCode()
    self.__assertRegisterAddress()
    self.__assertRegisterCount()

  @property
  def slave_address(self) -> int:
    return self.__slave_address
  
  def __assertDeviceAddress(self):
    assert self.slave_address > 0, ValueError('Device address must be greater than zero for read functions.')
  
  @property
  def function_code(self) -> int:
    return self.__function_code
  
  def __assertFunctionCode(self):
    assert self.function_code > 0, ValueError('Function code must be greater than zero.')

  @property
  def start_register(self) -> int:
    return self.__start_register
  
  def __assertRegisterAddress(self):
    assert self.start_register >= 0, ValueError('Register address must be greater or equal than zero.')
  
  @property
  def number_of_registers(self) -> int:
    return self.__number_of_registers
  
  def __assertRegisterCount(self):
    assert self.number_of_registers > 0, ValueError('Register count must be at least one.')
  
  def build(self) -> bytes:
    message_builder = ModbusMessageBuilder()
    message_builder.addUnsignedChar(self.slave_address)
    message_builder.addUnsignedChar(self.function_code)
    message_builder.addUnsignedShort(self.start_register)
    message_builder.addUnsignedShort(self.number_of_registers)
    return message_builder.build()

class ReadCoilStatusMessageBuilder(ReadMessageBuilder):
  def __init__(self, slave_address, start_coil, number_of_coils):
    super().__init__(slave_address=slave_address, function_code=1, start_register=start_coil, number_of_registers=number_of_coils)

class ReadHoldingRegisterMessageBuilder(ReadMessageBuilder):
  def __init__(self, slave_address, start_register, number_of_registers):
    super().__init__(slave_address=slave_address, function_code=3, start_register=start_register, number_of_registers=number_of_registers)

class ReadInputRegisterMessageBuilder(ReadMessageBuilder):
  def __init__(self, slave_address, start_register, number_of_registers):
    super().__init__(slave_address=slave_address, function_code=4, start_register=start_register, number_of_registers=number_of_registers)
