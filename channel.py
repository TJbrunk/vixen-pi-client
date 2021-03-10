# this class is responsible for controlling IO based on the incoming sACN (subset) data
import RPi.GPIO as GPIO
import logging, board, neopixel

class Channel:
    def __init__(self, config):
        self.name = config.get('name')
        self.pin = config.get('pin')
        self.logger = logging.getLogger(self.name)
        self.logger.info('Channel \'{}\' initialized with pin {}'.format(self.name, self.pin))

    def start(self):
        self.logger.info('Checking hardware access for relay control')
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)

    def update(self, sacnData):
        GPIO.output(self.pin, sacnData[0])
            


class RgbChannel(Channel):
    def __init__(self, config):
        super(RgbChannel, self).__init__(config)

        self.logger.info('Initalizing neopixel library')
        self.pixels = neopixel.NeoPixel(self.pin, config.get('pixelCount'))
        for p in self.pixels:
            p = (0, 0, 0)
    def start(self):
        pass

    def update(self, sacnData):
        for n in range(scanData, 3):
            self.pixels = n
