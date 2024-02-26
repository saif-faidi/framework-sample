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
        type   = conf.pop('type')
        if type == 'mqtt':
            return MQTT(conf)
        elif type == 'tcp':
            raise NotImplementedError(f'Add implementation for {type}')
        elif type == 'udp':
            raise NotImplementedError(f'Add implementation for {type}')
        elif type == 'can':
            raise NotImplementedError(f'Add implementation for {type}')
        elif type == 'lin':
            raise NotImplementedError(f'Add implementation for {type}')
        else:
            raise NotImplementedError(f'Add implementation for {type} Protocol')

