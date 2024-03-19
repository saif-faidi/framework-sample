import sys
import time
import logging.config
from src.config_loader import ConfigLoader
from src.network.protocol_factory import ProtocolFactory
from src.draft.sensor import Sensor as CVBController
from src.thermal.app import Thermal

class Message:
    def __init__(self, topic, payload):
        self.payload = '3'
        self.topic = 'Heating/All/HeatingReq'
        self.payload = self.payload.encode()

#https://stackoverflow.com/questions/50731203/should-i-use-events-semaphores-locks-conditions-or-a-combination-thereof-to
# TODO make sure threads are cleaned correctly
# TODO add command line arguments

# def mqtt_receive_clbk(message):
#     """ callback should be implemented externally not in the class Sensor because class sensor should not know about
#     which protocol is being used """
#     logger.debug(f'New MQTT message:))))))) {message.topic} => {str(message.payload.decode(errors="ignore"))}')
#
# def tcp_receive_clbk(message):
#     """ callback should be implemented externally not in the class Sensor because class sensor should not know about
#     which protocol is being used """
#     logger.debug(f'New TCP messag {message}')


if __name__ == "__main__":
    conf_loader     = ConfigLoader()
    config          = conf_loader.read_config_file()

    # Config for the Logger
    loggers_conf    = config.get('logging')
    logging.config.dictConfig(loggers_conf)
    logger = logging.getLogger(__name__)

    # Config for pneumatic
    # pneumatic_conf  = config.get('pneumatic')
    # protocol_conf   = pneumatic_conf.get('protocol')
    # protocol        = ProtocolFactory.create_instance(protocol_conf)
    # cvb_controller  = CVBController(protocol)
    # cvb_controller.set_receive_func(tcp_receive_clbk)
    # cvb_controller.start()

    # Config for Thermal
    thermal_conf   = config.get('rpi_ventilation')
    protocol       = ProtocolFactory.create_instance(thermal_conf.get('protocol'))
    thermal        = Thermal(thermal_conf, protocol)

    message = Message('Ventilation/All/VentilationReq', '3')
    thermal.mqtt_on_message(message)



    # while True:
    #     try:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #
    #         protocol.disconnect()
    #         sys.exit(0)



