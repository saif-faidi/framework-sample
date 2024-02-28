import sys
import time
import logging.config
from src.config_loader import ConfigLoader
from src.network.protocol_factory import ProtocolFactory

#https://stackoverflow.com/questions/50731203/should-i-use-events-semaphores-locks-conditions-or-a-combination-thereof-to

def mqtt_receive_clbk(message):
    """ callback should be implemented externally not in the class Sensor because class sensor should not know about
    which protocl is being used """
    logger.debug(f'New MQTT message:))))))) {message.topic} => {str(message.payload.decode(errors="ignore"))}')

def tcp_receive_clbk(message):
    """ callback should be implemented externally not in the class Sensor because class sensor should not know about
    which protocl is being used """
    logger.debug(f'New MQTT message:))))))) {message.topic} => {str(message.payload.decode(errors="ignore"))}')


if __name__ == "__main__":
    conf_loader = ConfigLoader()
    config      = conf_loader.read_config_file()
    protocol_conf  = config.get('protocol')
    loggers_conf   = config.get('logging')
    logging.config.dictConfig(loggers_conf)
    logger = logging.getLogger(__name__)


    protocol   = ProtocolFactory.create_instance(protocol_conf)


    from sensor import Sensor
    sensor = Sensor(protocol)
    sensor.start()


    sensor.set_receive_func(receive_clbk)


    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sensor.stop()
            protocol.disconnect()

            break
            sys.exit(0)



