import sys
import os
import time
import signal
import argparse
import logging.config
from src.config_loader import ConfigLoader
from src.network.protocol_factory import ProtocolFactory
from src.draft.sensor import Sensor as CVBController
from src.thermal.app import Thermal
from src.rpi_ventilation.app import RPI_Ventilation

class Message:
    def __init__(self, topic, payload):
        self.payload = '3'
        self.topic = 'Heating/All/HeatingReq'
        self.payload = self.payload.encode()

#https://stackoverflow.com/questions/50731203/should-i-use-events-semaphores-locks-conditions-or-a-combination-thereof-to
# TODO make sure threads are cleaned correctly
# TODO add command line arguments

def clean_exit(_signo, _stack_frame):
    """
    2  =>  SIGINT  => CTRL+C - Interrupt from keyboard
    15 =>  SIGTERM => External Exit request - Termination signal
    """
    global application_running
    if application_running:
        application_running = False
        if _signo == signal.SIGINT:
            # TODO check original code
            print('\b\b  \b\b\r', end='')
            logger.info('Exit requested by user...')
        elif _signo == signal.SIGTERM:
            logger.warning('Exit requested by system...')
    elif _signo == signal.SIGINT:
        # Emergency exit if process is blocked
        exit()


if __name__ == "__main__":

    application_running = True
    signal.signal(signal.SIGINT, clean_exit)
    signal.signal(signal.SIGTERM, clean_exit)

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
    thermal_conf   = config.get('thermal')
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



