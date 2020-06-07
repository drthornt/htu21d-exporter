#!/usr/bin/env python3

import random, logging, struct, array, time, io, fcntl, sys

from prometheus_client import start_http_server, Summary, Gauge
from prometheus_client import Gauge

# from smbus2 import SMBus

# I2C_SLAVE= 703 # 0x0703
I2C_SLAVE=0x0703
# HTU21D_ADDR = 40 # 0x40
HTU21D_ADDR = 0x40
CMD_READ_TEMP_HOLD = b'\xe3' # 0xE3
CMD_READ_HUM_HOLD = b'\xe5' # 0xE5
CMD_READ_TEMP_NOHOLD = b'\xf3' # 0xF3
CMD_READ_HUM_NOHOLD = b'\xf5' # 0xF5
CMD_WRITE_USER_REG = b'\xe6' # 0xE6
CMD_READ_USER_REG = b'\xe7' # 0xE7
CMD_SOFT_RESET= b'\376'

print ("RESET is {}".format(CMD_SOFT_RESET))

# Create a metric to track time spent and requests made.
# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
HUMIDITY = Gauge('relative_humidity', 'Relative Humidity')
TEMPERATURE = Gauge('temperature', 'Temperature')

logger = logging.getLogger(sys.argv[0])
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class i2c(object):
  def __init__(self, device, bus):
    self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
    self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
    fcntl.ioctl(self.fr, I2C_SLAVE, device)
    fcntl.ioctl(self.fw, I2C_SLAVE, device)

  def write(self, bytes):
    if __debug__:
      print("i2c.write() Writing bytes {}".format(bytes))
      print("i2c.write() type of bytes {}".format(type(bytes)))
      print("i2c.write() sizeof of bytes {}".format(sys.getsizeof(bytes)))
    self.fw.write(bytes)

  def read(self, bytes):
    return self.fr.read(bytes)

  def close(self):
    self.fw.close()
    self.fr.close()


class HTU21D(object):
  def __init__(self):
    print("HTU21D.__init__() type of HTU21D_ADDR type is {}".format(type(HTU21D_ADDR)))
    print("HTU21D.__init__() HTU21D_ADDR is {}".format(HTU21D_ADDR))
    self.dev = i2c(HTU21D_ADDR, 1) #HTU21D 0x40, bus 1
    print("HTU21D.__init__() type of CMD_SOFT_RESET is {}".format(type(CMD_SOFT_RESET)))
    print("HTU21D.__init__() Sending soft reset {}".format(CMD_SOFT_RESET))
    # x = self.dev.write(CMD_SOFT_RESET.to_bytes(2, byteorder='big')) #soft reset
    x = self.dev.write(CMD_SOFT_RESET) #soft reset
    print("return on CMD_SOFT_RESET is {}".format(x))
    time.sleep(.1)

  def ctemp(self, sensorTemp):
    tSensorTemp = sensorTemp / 65536.0
    return -46.85 + (175.72 * tSensorTemp)

  def chumid(self, sensorHumid):
    tSensorHumid = sensorHumid / 65536.0
    return -6.0 + (125.0 * tSensorHumid)

  def crc8check(self, value):
    # Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
    remainder = ( ( value[0] << 8 ) + value[1] ) << 8
    remainder |= value[2]

    # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
    # divsor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
    divsor = 0x988000

    for i in range(0, 16):
      if( remainder & 1 << (23 - i) ):
        remainder ^= divsor
      divsor = divsor >> 1

    if remainder == 0:
      return True
    else:
      return False

  def crc8check(self, value):
    # Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
    remainder = ( ( value[0] << 8 ) + value[1] ) << 8
    remainder |= value[2]

    # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
    # divsor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
    divsor = 0x988000

    for i in range(0, 16):
      if( remainder & 1 << (23 - i) ):
        remainder ^= divsor
      divsor = divsor >> 1

    if remainder == 0:
      return True
    else:
      return False

  def read_temperature(self):
    self.dev.write(CMD_READ_TEMP_NOHOLD) #measure temp
    time.sleep(.1)

    data = self.dev.read(3)
    buf = array.array('B', data)

    if self.crc8check(buf):
      temp = (buf[0] << 8 | buf [1]) & 0xFFFC
      return self.ctemp(temp)
    else:
      return -255

  def read_humidity(self):
    self.dev.write(CMD_READ_HUM_NOHOLD) #measure humidity
    time.sleep(.1)

    data = self.dev.read(3)
    print ("HTU21D.read_humidity(): {}".format(data))
    buf = array.array('B', data)

    if self.crc8check(buf):
      humid = (buf[0] << 8 | buf [1]) & 0xFFFC
      return self.chumid(humid)
    else:
      return -255

def update_gauges(device):
  HUMIDITY.set(device.read_humidity())
  TEMPERATURE.set(device.read_temperature())

if __name__ == '__main__':

  logger.info("initilize htu sensor")
  myhtu = HTU21D()

  logger.info("initalise gauges")
  update_gauges(myhtu)

  logger.info('Startup')
  # Start up the server to expose the metrics.
  start_http_server(8000)
  logger.info('Prometheus server started')
  
  while True:
    logger.debug("tick")
    time.sleep(60)
    update_gauges(myhtu)

