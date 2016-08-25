#!/usr/bin/python
import struct, array, time, io, fcntl
#import RPi.GPIO as GPIO
import time
import sys


enable = 4
ch1 = 17
ch2 = 27

I2C_SLAVE=0x0703

CHANNEL_0 = 0
CHANNEL_1 = 1

CMD_RESET = "\x06"
CMD_LATCH = "\x04"
CMD_CONVERSION = "\x08"
CMD_READ_CH0_16BIT = "\x88"
CMD_READ_CH1_16BIT = "\xA8"
	
BIN = "{0:8b}"



class i2c(object):
   def __init__(self, device, bus):
      self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
      self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
      # set device address
      fcntl.ioctl(self.fr, I2C_SLAVE, device)
      fcntl.ioctl(self.fw, I2C_SLAVE, device)
   def write(self, bytes):
      self.fw.write(bytes)
   def read(self, bytes):
      return self.fr.read(bytes)
   def __del__(self):
      self.fw.close()
      self.fr.close()

class MCP342X(object):
    def __init__(self, address):
        self.dev = i2c(address, 1)
        self.msleep = lambda x: time.sleep(x/1000.0)
        
    def reset(self):
        self.dev.write(CMD_RESET)

    def latch(self):
        self.dev.write(CMD_LATCH)

    def conversion(self):
        self.dev.write(CMD_CONVERSION)

    def configure(self, channel = 0):
        if channel == 1:
            self.dev.write(CMD_READ_CH1_16BIT)
        else:
            self.dev.write(CMD_READ_CH0_16BIT)
        self.msleep(100)

    def read(self):
        data = self.dev.read(3)
        buf = array.array('B', data)

        #for i in range(0, len(buf)):
        #   print i, ":", BIN.format(buf[i])

        status = buf[2]
        result = None

        if status & 128 != 128: #check ready bit = 0
            result = buf[0] << 8 | buf[1]

        return result



