from serial import Serial
import struct

from modbus_message import ModbusMessage
from modbus_response import ReadCoilStatusResponse, ReadHoldingRegistersResponse, ReadInputRegistersResponse

class ModbusClient:
  def __init__(self, serial: Serial):
    self.serial = serial
  
  def sendMessage(self, payload: bytes) -> None:
    self.serial.write(payload)
  
  def readResponse(self) -> bytes:
    response_bytes = self.serial.readline()
    return response_bytes

  def readCoilStatus(self, slave_address: int, start_coil: int, number_of_coils: int) -> bytes:
    payload_word_struct = '>BBHH'
    function_code = 1

    payload = struct.pack(payload_word_struct, slave_address, function_code, start_coil, number_of_coils)

    message = ModbusMessage(payload, hasCRC16=False)
    message.addCRC16()

    self.sendMessage(message.payload)
    response_bytes = self.readResponse()

    if not response_bytes:
      raise Exception('No data received!')

    response = ReadCoilStatusResponse(response_bytes)

    return response
  
  def readHoldingRegisters(self, slave_address: int, start_register: int, number_of_registers: int) -> bytes:
    payload_word_struct = '>BBHH'
    function_code = 3

    payload = struct.pack(payload_word_struct, slave_address, function_code, start_register, number_of_registers)
    
    messsage = ModbusMessage(payload, hasCRC16=False)
    messsage.addCRC16()
    
    self.sendMessage(messsage.payload)
    response_bytes = self.readResponse()

    if not response_bytes:
      raise Exception('No data received!')

    response = ReadHoldingRegistersResponse(response_bytes)

    return response

  def readInputRegisters(self, slave_address: int, start_register: int, number_of_registers: int) -> bytes:
    payload_word_struct = '>BBHH'
    function_code = 4

    payload = struct.pack(payload_word_struct, slave_address, function_code, start_register, number_of_registers)
    
    messsage = ModbusMessage(payload, hasCRC16=False)
    messsage.addCRC16()
    
    self.sendMessage(messsage.payload)
    response_bytes = self.readResponse()

    if not response_bytes:
      raise Exception('No data received!')

    response = ReadInputRegistersResponse(response_bytes)

    return response
