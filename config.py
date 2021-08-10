import os, json, logging
from channel import Channel
from typing import List

class Config():

  def __init__(self):
    self.logger = logging.getLogger('Config')
    self.windowsIPAddress: str
    self.channels: List[Channel]
    self.universe: int


  def load(self):
    configFile = os.path.join('config.local.json')
    if(not os.path.exists(configFile)):
      self.logger.warning('Local config file not found. Using defaults')
      configFile = os.path.join('config.json')

    with open(configFile) as c:
      config = json.load(c)
      self.logger.info('Configuration loaded')
      self.universe = config['universe']
      print('Universe: ', self.universe)
      self.channels = config['channels']
      # if(config['windowsIPAddress']):
      self.windowsIPAddress = config['windowsIPAddress']
      print('Windows IPAddress: ', self.windowsIPAddress)
      # else:
        # self.windowsIPAddress = None