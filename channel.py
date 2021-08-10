# this class is responsible for controlling IO based on the incoming sACN (subset) data
from sys import platform

# Don't try to import RPI modules if running on Windows
if platform != "win32":
  import RPi.GPIO as GPIO
  import board, neopixel

import logging, sys

class Channel:
  def __init__(self, config):
    self.name = config.get('name')
    self.pin = config.get('pin')
    self.logger = logging.getLogger(self.name)
    self.logger.info('Channel \'{}\' initialized with pin {}'.format(self.name, self.pin))

  def start(self):
    self.logger.info('Checking hardware access for relay control')
    if(sys.platform == "win32"):
      self.logger.info('WINDOWS: simulating GPIO setup for pin %d', self.pin)
      return
    else:
      self.logger.debug('Configuring GPIO pin %d', self.pin)
      GPIO.setup(self.pin, GPIO.OUT)
      GPIO.output(self.pin, False)

  def update(self, sacnData):
    if(sys.platform == 'win32'):
      self.logger.info('WINDOWS: simulating updating GPIO pin %d to %d', self.pin, sacnData[0])
    else:
      self.logger.debug('Setting pin %d to %d', self.pin, sacnData[0])
      GPIO.output(self.pin, sacnData[0])


class RgbChannel(Channel):
  def __init__(self, config):
    super(RgbChannel, self).__init__(config)

    self.logger.info('Initalizing neopixel library')
    if(sys.platform == 'win32'):
      self.logger.info('WINDOWS: simulating setting up NeoPixel')
    else:
      self.pixels = neopixel.NeoPixel(self.pin, config.get('pixelCount'))
      # init rgb values to 0
      for p in self.pixels:
        p = (0, 0, 0)

  def start(self):
    pass

  def update(self, sacnData):
    self.logger.debug('Updating NeoPixel color')
    if(sys.platform == 'win32'):
      self.logger.info('WINDOWS: simulating update')
    else:
      for n in range(sacnData, 3):
        self.pixels = n
