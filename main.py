import sys, os, sacn, time
import logging, logging.handlers

from channel import Channel, RgbChannel
from config import Config

class VixenClient(object):

  def __init__(self):
    self.logger = logging.getLogger('VixenClient')
    self.config: Config


  def configure(self, config: Config):
    config.load()
    if(sys.platform == 'win32'):
      self.receiver = sacn.sACNreceiver(bind_address=config.windowsIPAddress)
    else:
      self.receiver = sacn.sACNreceiver()


  ### Configures list of where to slice incoming sACN data
  ### based on the config file
  def setupParser(self, config: Config):
    self.idxArray = []
    i = 0
    for ch in config.channels:
      if(ch['isRGB']):
        self.idxArray.append(
          dict(
            start=ch['startIndex'],
              #RGB requires 3 bytes
              end=(ch['pixelCount']*3+ch['startIndex'])
            ) 
        )
      else:
        self.idxArray.append(
          dict(
            start=ch['startIndex'],
            end=ch['pixelCount']+ch['startIndex']
          )
        )
        i = i+1

  ### Create the 'channel' objects that are responsible for sending sACN data to hardware
  def initChannels(self, config: Config):
    self.channels = []
    for ch in config.channels:
      self.logger.info('Preparing channel init {}'.format(ch))
      if(ch.get('isRGB')):
        self.channels.append(RgbChannel(ch))
      else:
        self.channels.append(Channel(ch))


  ### Start receiving sACN data and control lights
  def begin(self, config: Config):
    # start the sacn receiver
    self.logger.info("Starting sACN data receiver")
    self.receiver.start()

    # register the callback to handle incoming sacn data
    self.receiver.register_listener('universe',
        self.parseData,
        universe = config.universe)

    # set sacn client to use multicast
    if(sys.platform == 'win32'):
      self.logger.warning('Unable to join mulicast on Windows')
    else:
      self.receiver.join_multicast(config.universe)

  ### Callback handler to parse sACN data and send to lights
  def parseData(self, packet):
    for ch in self.idxArray:
      p=packet.dmxData[ch['start']:ch['end']]
      print(p)
    print(packet.dmxData)


if __name__ == '__main__':
  logFile = './logs/debug.log'

  if not os.path.exists('./logs'):
    os.makedirs('./logs')
    with open(logFile, 'a'): pass

  # Create a rotation handler to rotate logging between 20 files
  handler = logging.handlers.RotatingFileHandler(
              logFile, maxBytes=2000000, backupCount=20)

  # format the message logging
  formatter = logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s')
  # register the formatter
  handler.setFormatter(formatter)

  rootLogger = logging.getLogger()
  # set the log level
  rootLogger.setLevel(logging.DEBUG)
  # register the rotation handler with the logger
  rootLogger.addHandler(handler)

  # define a Handler to write INFO messages to sys.stderr
  console = logging.StreamHandler()
  console.setLevel(logging.INFO)


  # set a different format for console messages
  formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

  # tell the handler to use the simple format
  console.setFormatter(formatter)

  # add the handler to the root logger
  rootLogger.addHandler(console)

  logging.info('Application started')

  configuration = Config()
  client = VixenClient()
  client.configure(configuration)
  client.initChannels(configuration)
  client.setupParser(configuration)
  client.begin(configuration)
