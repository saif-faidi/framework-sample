import sys
import time
import logging.config
from src.config_loader import ConfigLoader
from src.network.protocol_factory import ProtocolFactory

#https://stackoverflow.com/questions/50731203/should-i-use-events-semaphores-locks-conditions-or-a-combination-thereof-to

if __name__ == "__main__":
    conf_loader = ConfigLoader()
    config      = conf_loader.read_config_file()
    protocol_conf  = config.get('protocol')
    loggers_conf   = config.get('logging')
    logging.config.dictConfig(loggers_conf)
    logger = logging.getLogger(__name__)


    protocol   = ProtocolFactory.create_instance(protocol_conf)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
            sys.exit(0)



