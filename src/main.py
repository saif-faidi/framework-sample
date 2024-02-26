
from src.config_loader import ConfigLoader
from src.network.mqtt import MQTT
from src.network.protocol_factory import ProtocolFactory

if __name__ == "__main__":

    conf_loader = ConfigLoader()
    # getting default configuration
    config      = conf_loader.read_config_file()
    protocol    = ProtocolFactory.create_instance(config.get('protocol'))
    protocol.send('/Sensor', 'DATA',2, False)
    print(protocol)

