from abc import ABC, abstractmethod
from typing import Any

class Protocol(ABC):

    def __init__(self, conf:dict):
        self.function = conf.get('function')
        self.host     = conf.get('host')
        self.port     = conf.get('port')

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def send(self, data: Any):
        pass

    @abstractmethod
    def receive(self, data: Any):
        pass

    @abstractmethod
    def disconnect(self):
        pass