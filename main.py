import logging
import os

LOGGING_FORMAT  = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logger = logging.getLogger(__file__)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOGGING_FORMAT)
logger.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

from src.config_loader import ConfigLoader
c=  ConfigLoader()
print(c._get_current_directory())