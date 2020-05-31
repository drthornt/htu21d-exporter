#!/usr/bin/env python3

from smbus2 import SMBus
from binascii import unhexlify

# device address
HTU21D_ADDR = 64
RESET = 376

#HUMIDITY = const(0xF5)
#TEMPERATURE = const(0xF3)
# _RESET = const(0xFE)

#_RESET = 0xFE
_RESET = 0xFE
# resetbin = unhexlify("FE")
resetbin = 254

#_READ_USER1 = const(0xE7)
#_USER1_VAL = const(0x3A)


#with SMBus(1) as bus:
#    # Write a byte to address 80, offset 0
#    print("immabus")
#    bus.write_byte_data(HTU21D_ADDR, 0, resetbin)
    
# Open i2c bus 1 and read one byte from address 80, offset 0
bus = SMBus(1)

#b = bus.read_byte_data(40, 0)
#print(b)
#bus.close()

for device in range(254):
      try:
         bus.read_byte(device)
         print(hex(device))
      except: # exception if read_byte fails
         pass


#b = bus.write_byte_data(64, 1)
#bus.write_byte_data(80, 0, data)
#print(b)
#bus.close()

