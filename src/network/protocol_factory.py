from src.network.mqtt import MQTT

from enum import Enum

class ProtocolEnum(Enum):
    MQTT                = 'mqtt'
    TCP                 = 'tcp'
    UDP                 = 'udp'
    SOCKET_IO           = 'socket-io'
    CAN                 = 'can'
    LIN                 = 'lin'


class ProtocolFactory:
    @staticmethod
    def create_instance(conf:dict):
        _type   = conf.pop('type')
        if type == 'mqtt':
            return MQTT(conf)
        elif _type == 'tcp':
            raise NotImplementedError(f'Add implementation for {_type}')
        elif _type == 'udp':
            raise NotImplementedError(f'Add implementation for {_type}')
        elif _type == 'can':
            raise NotImplementedError(f'Add implementation for {_type}')
        elif _type == 'lin':
            raise NotImplementedError(f'Add implementation for {_type}')
        else:
            raise NotImplementedError(f'Add implementation for {_type} Protocol')

