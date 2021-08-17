# this class is responsible for controlling IO based on the incoming sACN (subset) data
from sys import platform
from typing import List

# Don't try to import RPI modules if running on Windows
if platform != "win32":
  import RPi.GPIO as GPIO
  import board, neopixel
  from adafruit_blinka.microcontroller.bcm283x import pin

import logging, sys

class Channel:
  '''
  Setup logger and GPIO pin
  '''
  def __init__(self, config):
    self.name: str = config.get('name')
    self.pin: int = config.get('pin')
    self.startIndex: int = config.get('startIndex')
    self.logger = logging.getLogger(__name__)
    self.logger.info('Channel \'{}\' initialized with pin {}'.format(self.name, self.pin))
    if(sys.platform == "win32"):
      self.logger.info('WINDOWS: simulating GPIO setup for pin %d', self.pin)
      return
    else:
      self.logger.info('Configuring GPIO pin %d', self.pin)
      GPIO.setup(self.pin, GPIO.OUT)
      GPIO.output(self.pin, False)

  '''
  Set GPIO pin to the commanded state
  '''
  def update(self, state: List[int]):
    if(sys.platform == 'win32'):
      self.logger.info('WINDOWS: simulating updating GPIO pin %d to %d', self.pin, state)
    else:
      s = False if state[0] == 0 else True
      self.logger.debug('Setting pin %d to %d', self.pin, s)
      GPIO.output(self.pin, s)


class RgbChannel(Channel):
  '''
  Setup NeoPixel for controlling RGB leds
  '''
  def __init__(self, config):
    super(RgbChannel, self).__init__(config)

    if(sys.platform == 'win32'):
      self.logger.info('WINDOWS: simulating setting up NeoPixel')
    else:
      self.logger.info('Initalizing neopixel library')
      self.pixels = neopixel.NeoPixel(pin.Pin(self.pin), config.get('pixelCount'))
      # init rgb values to 0
      for p in self.pixels:
        p = (0, 0, 0)

  def split_colors(self, sacnData):
    arrs = []
    size = 3
    while len(sacnData) > size:
      pice = sacnData[:size]
      arrs.append(pice)
      sacnData = sacnData[size:]
    arrs.append(sacnData)
    return arrs

  '''
  Update strand of NeoPixels to commanded color
  '''
  def update(self, sacnData: List[int]):
    self.logger.debug('Updating NeoPixels color')
    if(sys.platform == 'win32'):
      self.logger.info('WINDOWS: simulating update')
    else:
      for i, color in enumerate(self.split_colors(sacnData)):
        self.logger.debug("Setting Pixel %d to %s", i, color)
        self.pixels[i] = color