import sys, os, sacn, json
import logging, logging.config

from typing import List
from channel import Channel, RgbChannel
from config import Config

class VixenClient(object):

  def __init__(self):
    self.logger = logging.getLogger('VixenClient')
    self.config: Config
    self.channels: List[Channel]


  '''
  Load configuration and start sACN receiver
  '''
  def configure(self, config: Config):
    config.load()
    if(sys.platform == 'win32'):
      self.receiver = sacn.sACNreceiver(bind_address=config.windowsIPAddress)
    else:
      self.receiver = sacn.sACNreceiver()


  '''
  Create list to know where to slice incominng sACN data
  based off of the loaded configuration file
  '''
  def setupParser(self, config: Config):
    self.idxArray = []
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

  '''
  Create the 'channel' objects that are responsible for sending
  sACN data to hardware
  '''
  def initChannels(self, config: Config):
    self.channels = []
    for ch in config.channels:
      self.logger.info('Preparing channel init {}'.format(ch))
      if(ch.get('isRGB')):
        self.channels.append(RgbChannel(ch))
      else:
        self.channels.append(Channel(ch))


  '''
  Start receiving sACN data and control lights
  '''
  def begin(self, config: Config):
    # start the sacn receiver
    self.logger.info("Starting sACN data receiver")
    self.receiver.start()

    # register the callback to handle incoming sacn data
    self.receiver.register_listener('universe',
        self.parseData,
        universe = config.universe)

    self.receiver.register_listener('availability',
        self.availability_changed)

    # set sacn client to use multicast
    if(sys.platform == 'win32'):
      self.logger.warning('Unable to join mulicast on Windows')
    else:
      self.receiver.join_multicast(config.universe)

  def availability_changed(self, universe: int, changed: str):
    self.logger.info("Availability changed event " + changed)
    if(changed == 'timeout'):
      self.begin()

  '''
  Callback handler to parse sACN data and send to lights
  '''
  def parseData(self, packet):
    self.logger.info('New Packet. Universe: %d Sequence: %d',
                    packet.universe, packet.sequence)
    # self.logger.debug('Full Packet: %s', packet.dmxData)

    for idx, ch in enumerate(self.idxArray):
      p = packet.dmxData[ch['start']:ch['end']]
      # self.logger.info('Ch data %d', p)
      self.channels[idx].update(p)



if __name__ == '__main__':
  logFile = '../logs/debug.log'

  if not os.path.exists('../logs'):
    os.makedirs('../logs')
    with open(logFile, 'a'): pass

  with open(os.path.join('logging.json'),'rt') as f:
        config=json.load(f)
        f.close()
        logging.config.dictConfig(config)

  logger=logging.getLogger(__name__)

  rootLogger = logging.getLogger(__name__)

  logging.info('Application started')

  configuration = Config()
  client = VixenClient()
  client.configure(configuration)
  client.initChannels(configuration)
  client.setupParser(configuration)
  client.begin(configuration)
