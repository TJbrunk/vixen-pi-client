import sys, os, sacn, time, json
import logging, logging.handlers


class VixenClient(object):

    def __init__(self):
        self.logger = logging.getLogger('VixenClient')
        self.receiver = sacn.sACNreceiver()

    def loadConfig(self):
        configFile = os.path.join('config.local.json')
        if(not os.path.exists(configFile)):
            self.logger.warning('Local config file not found. Using defaults')
            configFile = os.path.join('config.json')
        with open(configFile) as c:
            self.config = json.load(c)
            self.logger.info('Configuration loaded')
            #print(self.config)

    def begin(self):
        # start the sacn receiver
        self.receiver.start()
        # register the callback to handle incoming sacn data
        self.receiver.register_listener('universe',
                self.parseData,
                universe = self.config['universe'])
        # set sacn client to use multicast
        self.receiver.join_multicast(self.config['universe'])

    def parseData(self, packet):
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

    client = VixenClient()
    client.loadConfig()
    client.begin()
