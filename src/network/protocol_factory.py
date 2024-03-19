from src.network.mqtt import MQTT
from src.network.tcp_client import TCPClient
from src.network.mock_client import MockClient

class ProtocolFactory:
    @staticmethod
    def create_instance(conf:dict):
        _type   = conf.pop('type')
        if _type == 'mqtt':
            return MQTT(conf)
        elif _type == 'tcp':
            return TCPClient(conf)
        elif _type == 'udp':
            raise NotImplementedError(f'Add implementation for {_type}')
        elif _type == 'can':
            raise NotImplementedError(f'Add implementation for {_type}')
        elif _type == 'lin':
            raise NotImplementedError(f'Add implementation for {_type}')
        elif _type == 'mock':
            return MockClient(conf)
        else:
            raise NotImplementedError(f'Add implementation for {_type} Protocol')

