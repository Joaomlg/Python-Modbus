class ModbusException(Exception):
  @staticmethod
  def fromExceptionCode(exception_code: int):
    if exception_code == 1:
      return IllegalFunctionError
    elif exception_code == 2:
      return IllegalDataAddressError
    elif exception_code == 3:
      return IllegalDataValueError
    elif exception_code == 4:
      return SlaveDeviceFailureError
    elif exception_code == 5:
      return AcknowledgeError
    elif exception_code == 6:
      return SlaveDeviceBusyError
    elif exception_code == 7:
      return NegativeAcknowledgeError
    elif exception_code == 8:
      return MemoryParityError
    elif exception_code == 10:
      return GatewayPathUnavailableError
    elif exception_code == 11:
      return GatewayTargetDeviceFailedToRespondError
    else:
      return Exception(f'Slave reported a unknown error, exception code: {exception_code}')

class IllegalFunctionError(ModbusException):
  pass

class IllegalDataAddressError(ModbusException):
  pass

class IllegalDataValueError(ModbusException):
  pass

class SlaveDeviceFailureError(ModbusException):
  pass

class AcknowledgeError(ModbusException):
  pass

class SlaveDeviceBusyError(ModbusException):
  pass

class NegativeAcknowledgeError(ModbusException):
  pass

class MemoryParityError(ModbusException):
  pass

class GatewayPathUnavailableError(ModbusException):
  pass

class GatewayTargetDeviceFailedToRespondError(ModbusException):
  pass

