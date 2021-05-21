def calculateDataCRC16(data: bytes, length=2, byteorder='little') -> bytes:
  crc_word = 0xFFFF
  for byte in range(len(data)):
    crc_word ^= data[byte]
    for _ in range(8):
      if crc_word & 0x0001 != 0:
        crc_word >>= 1
        crc_word ^= 0xA001
      else:
        crc_word >>= 1
  crc16 = crc_word.to_bytes(length, byteorder)
  return crc16
  
def verifyPayloadCRC16(payload: bytes, offset=-2) -> bool:
  payload_data = payload[:offset]
  payload_crc16 = payload[offset:]
  calculated_crc16 = calculateDataCRC16(payload_data)
  return payload_crc16 == calculated_crc16
