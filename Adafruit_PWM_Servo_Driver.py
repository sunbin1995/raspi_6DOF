#!/usr/bin/python

import time
import math
from I2C import I2C

# ============================================================================
# Adafruit PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PWM :
  i2c = None

  #  Registers/etc.
  __SUBADR1            = 0x02
  __SUBADR2            = 0x03
  __SUBADR3            = 0x04
  __MODE1              = 0x00
  __PRESCALE           = 0xFE
  __LED0_ON_L          = 0x06
  __LED0_ON_H          = 0x07
  __LED0_OFF_L         = 0x08
  __LED0_OFF_H         = 0x09
  __ALLLED_ON_L        = 0xFA
  __ALLLED_ON_H        = 0xFB
  __ALLLED_OFF_L       = 0xFC
  __ALLLED_OFF_H       = 0xFD

  def __init__(self, address=0x40, debug=False):
    self.i2c = I2C(address)
    self.address = address
    self.debug = debug
    if (self.debug):
      print ('Reseting PCA9685')
    self.i2c.write8(self.__MODE1, 0x00)

  def setPWMFreq(self, freq):
    "Sets the PWM frequency"
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    if (self.debug):
      print ('Setting PWM frequency to %d Hz" % freq')
      print ('Estimated pre-scale: %d" % prescaleval')
    prescale = math.floor(prescaleval + 0.5)
    if (self.debug):
      print ('Final pre-scale: %d" % prescale')

    oldmode = self.i2c.readU8(self.__MODE1);
    newmode = (oldmode & 0x7F) | 0x10             # sleep
    self.i2c.write8(self.__MODE1, newmode)        # go to sleep
    self.i2c.write8(self.__PRESCALE, int(math.floor(prescale)))
    self.i2c.write8(self.__MODE1, oldmode)
    time.sleep(0.005)
    self.i2c.write8(self.__MODE1, oldmode | 0x80)

  def setPWM(self, channel, on, off):
    "Sets a single PWM channel"
    self.i2c.write8(self.__LED0_ON_L+4*channel, on & 0xFF)
    self.i2c.write8(self.__LED0_ON_H+4*channel, on >> 8)
    self.i2c.write8(self.__LED0_OFF_L+4*channel, off & 0xFF)
    self.i2c.write8(self.__LED0_OFF_H+4*channel, off >> 8)
  ## test
  def setServoPulse(self,channel,pulse):
    "Sets the Servo Pulse,The PWM frequency must be 50HZ"
    pulse = pulse * 4096 / 20000  # PWM frequency is 50HZ,the period is 20000us
    self.setPWM(channel, 0, pulse)


if __name__ == '__main__':

  pwm1 = PWM(0x40, debug=True)
  pwm1.setPWMFreq(50)
  while True:
    # setServoPulse(2,2500)
    for i in range(500, 2500, 10):
      pwm1.setServoPulse(0, i)
      time.sleep(0.02)

    for i in range(2500, 500, -10):
      pwm1.setServoPulse(0, i)
      time.sleep(0.02)




