from abc import ABC, abstractmethod
from typing import Any


class Protocol(ABC):

    def __init__(self, conf: dict):
        self.function = conf.get('function')
        self.host = conf.get('host')
        self.port = conf.get('port')
        self.retry_s = conf.get('retry_s')
        self.__on_receive = lambda data: data  # Do nothing

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def send(self, data: Any):
        pass

    def on_receive(self, data: Any):
        self.__on_receive(data)


    @abstractmethod
    def disconnect(self):
        pass
