from modbus_utils import verifyPayloadCRC16
from modbus_exceptions import ModbusException

class ModbusResponse:
  def __init__(self, payload: bytes):
    self.__payload = payload
    assert verifyPayloadCRC16(self.payload), Exception('Invalid response CRC16!')

  @property
  def payload(self):
    return self.__payload
  
  @property
  def slave_address(self) -> int:
    return self.payload[0]
  
  @property
  def function_code(self) -> int:
    return self.payload[1]

  @property
  def crc16(self) -> bytes:
    return self.payload[-2:]

  def __str__(self) -> str:
    return str(self.payload)

  def __repr__(self) -> str:
    return f'ModbusResponse({str(self.payload)})'

class ModbusReadFunctionResponse(ModbusResponse):
  EXPECTED_FUNCTION_CODE = None
  EXCEPTION_FUNCTION_CODE = None
  
  def __init__(self, payload: bytes):
    super().__init__(payload)

    if self.function_code == self.EXCEPTION_FUNCTION_CODE:
      exception_code = self.payload[2]
      raise ModbusException.fromExceptionCode(exception_code)

    if self.function_code != self.EXPECTED_FUNCTION_CODE:
      raise Exception(f'Invalid function code: {self.function_code}')
  
  @property
  def data_size(self) -> int:
    return self.payload[2]

  @property
  def data_bytes(self) -> bytes:
    data_start_idx = 3
    data_end_idx = 3 + self.data_size
    return self.payload[data_start_idx:data_end_idx]
  
  @property
  def data_array(self) -> list:
    return list(self.data_bytes)

class ReadCoilStatusResponse(ModbusReadFunctionResponse):
  EXPECTED_FUNCTION_CODE = 0x01
  EXCEPTION_FUNCTION_CODE = 0x81  

class ReadHoldingRegistersResponse(ModbusReadFunctionResponse):
  EXPECTED_FUNCTION_CODE = 0x03
  EXCEPTION_FUNCTION_CODE = 0x83

class ReadInputRegistersResponse(ModbusReadFunctionResponse):
  EXPECTED_FUNCTION_CODE = 0x04
  EXCEPTION_FUNCTION_CODE = 0x84
