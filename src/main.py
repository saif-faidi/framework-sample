import sys
import signal
import importlib.util
import logging.config
from src.config_loader import ConfigLoader
from src.network.protocol_factory import ProtocolFactory



class Message:
    def __init__(self, topic, payload):
        self.payload = '3'
        self.topic = 'Heating/All/HeatingReq'
        self.payload = self.payload.encode()

#https://stackoverflow.com/questions/50731203/should-i-use-events-semaphores-locks-conditions-or-a-combination-thereof-to
# TODO make sure threads are cleaned correctly
# TODO add command line arguments
# TODO use a common message format with { key, payload }

def clean_exit(_signo, _stack_frame):
    """
    2  =>  SIGINT  => CTRL+C - Interrupt from keyboard
    15 =>  SIGTERM => External Exit request - Termination signal
    """
    global functions
    global application_running
    if application_running:
        application_running = False
        if _signo == signal.SIGINT:
            # TODO check original code
            print('\b\b  \b\b\r', end='')
            logger.info('Exit requested by user...')
        elif _signo == signal.SIGTERM:
            logger.warning('Exit requested by system...')
        for function in functions:
            function.on_exit()
    elif _signo == signal.SIGINT:
        for function in functions:
            function.on_exit()
        # Emergency exit if process is blocked
        exit()



if __name__ == "__main__":

    # TODO use  argparse to read this list of options
    module_name     = 'thermal' # -m
    function        = 'Thermal' # -f
    loglevel        = 'DEBUG'   # -v -> access to the dict below and change the level to the input value, (should we change in the root or in the handlers ?
    config_file     = 'path/to/config/file' #-c
    is_service      = 'true or false' # if true use service Formatter, else use default formatter

    #{'version': 1, 'disable_existing_loggers': False, 'formatters': {'service_formatter': {'()': 'src.service_formatter.ServiceFormatter', 'format_str': '{time} - {name} - {levelname} - {message}', 'datefmt': '%Y-%m-%d %H:%M:%S'}, 'default': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}}, 'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'service_formatter', 'stream': 'ext://sys.stdout'}}, 'root': {'level': 'DEBUG', 'handlers': ['console']}}

    application_running = True
    functions = []
    signal.signal(signal.SIGINT, clean_exit)
    signal.signal(signal.SIGTERM, clean_exit)

    # Load configuration from config file
    conf_loader     = ConfigLoader()
    config          = conf_loader.read_config_file("") # pass the config file input here if it's passed as input

    # Config for the Logger
    loggers_conf    = config.get('logging')
    print(loggers_conf)
    logging.config.dictConfig(loggers_conf)
    logger = logging.getLogger(__name__)


    # Config for Thermal
    module_full_path= f'src.functions.{module_name}.app'
    module_conf     = config.get(module_name)
    protocol        = ProtocolFactory.create_instance(module_conf.get('protocol'))

    # Import and instantiate function
    try:
        module = importlib.import_module(module_full_path)
    except ImportError as e:
        logger.error(f"Error importing module '{module_full_path}' : {e}")
        exit()
    try:
        class_   = getattr(module, function)
        instance = class_(module_conf, protocol)
        functions.append(instance)
    except AttributeError as e:
        logger.error(f"Error importing class '{function}' : {e}")
        exit()



    message = Message('Ventilation/All/VentilationReq', '3')
    instance.mqtt_on_message(message)





