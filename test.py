# Simple demo of of the PCA9685 PWM servo/LED controller library.

import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 102  # Min pulse length out of 4096,100          x/20 = off/4096,   ==4096/20*(0.5+(度数/180)*2)
servo_max = 512  # Max pulse length out of 4096,500
servo_mid = 307
speed = 0.2      #servo speed
speed1 = 0.5     #servo speed1

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000    # 1000000 us per second
    pulse_length //= 60       # 60Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)

def ServoInitial():
    for i in range(7):
      pwm.set_pwm(i, 0, servo_mid)
      time.sleep(0.01)

def SetJointAngle(channel,angle):
    off_num = 4096/20*(0.5+(angle/180)*2)
    pwm.set_pwm(channel, on=0, off=off_num)