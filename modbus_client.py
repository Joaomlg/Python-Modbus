from serial import Serial
import struct

from modbus_message import ReadCoilStatusMessageBuilder, ReadHoldingRegisterMessageBuilder, ReadInputRegisterMessageBuilder
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
    message_builder = ReadCoilStatusMessageBuilder(slave_address, start_coil, number_of_coils)
    read_coil_status_message = message_builder.build()

    self.sendMessage(read_coil_status_message)
    response_bytes = self.readResponse()

    if not response_bytes:
      raise Exception('No data received!')

    response = ReadCoilStatusResponse(response_bytes)

    return response
  
  def readHoldingRegisters(self, slave_address: int, start_register: int, number_of_registers: int) -> bytes:
    message_builder = ReadHoldingRegisterMessageBuilder(slave_address, start_register, number_of_registers)
    read_holding_registers_messsage = message_builder.build()
    
    self.sendMessage(read_holding_registers_messsage)
    response_bytes = self.readResponse()

    if not response_bytes:
      raise Exception('No data received!')

    response = ReadHoldingRegistersResponse(response_bytes)

    return response

  def readInputRegisters(self, slave_address: int, start_register: int, number_of_registers: int) -> bytes:
    messsage_builder = ReadInputRegisterMessageBuilder(slave_address, start_register, number_of_registers)
    read_input_registers_message = messsage_builder.build()
    
    self.sendMessage(read_input_registers_message)
    response_bytes = self.readResponse()

    if not response_bytes:
      raise Exception('No data received!')

    response = ReadInputRegistersResponse(response_bytes)

    return response
