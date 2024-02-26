import os
import yaml
import logging
from typing import Any, Union

from src.enums import ExitCode


class ConfigLoader:

    YAML_EXTENSIONS     = ['yaml', 'yml']
    LOGGING_LEVEL       = logging.DEBUG
    LOGGING_FORMAT      = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DEFAULT_CONFIG_FILE = 'config.yaml'

    def __init__(self):
        self.logger     = logging.getLogger(self.__class__.__name__)
        formatter       = logging.Formatter(ConfigLoader.LOGGING_FORMAT)
        console_handler = logging.StreamHandler()

        console_handler.setLevel(ConfigLoader.LOGGING_LEVEL)
        console_handler.setFormatter(formatter)
        self.logger.setLevel(ConfigLoader.LOGGING_LEVEL)
        self.logger.addHandler(console_handler)


    def _get_current_directory(self) -> str:
        """Get the path of the current directory, same directory as the current file"""
        current_file_path = os.path.abspath(__file__)
        # Extract the directory path
        current_directory = os.path.dirname(current_file_path)
        return current_directory


    def _check_file_exist(self, file_path: str) -> Union[str, None]:
        ''' check if the file exists in the file path or in the current directory
        return: file path if the file exists or the current config.yaml file in the 'src' directory
        '''
        if os.path.exists(file_path):
            return file_path
        else:
            # search in the current directory if the file does not exist
            if file_path != '':
                self.logger.debug(f'File : {file_path} does not exist... looking in default config file')
            current_directory = self._get_current_directory()
            default_conf_path = os.path.abspath(os.path.join(current_directory, ConfigLoader.DEFAULT_CONFIG_FILE))
            return default_conf_path



    def read_config_file(self,file_path : str='') -> Any:
        ''' returnn the configuration from file_path as a dict value'''
        file = self._check_file_exist(file_path)
        try:
            with open(file, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            self.logger.error(f'Default config file:{file} is not found.')
            exit(ExitCode.FILE_NOT_FOUND)
        except Exception as e:
            self.logger.exception(e)
            exit(ExitCode.GENERAL_ERROR)



