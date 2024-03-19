import logging
from src.network.protocol import Protocol


class MockClient(Protocol):

    DEFAULT_QOS = 2

    def __init__(self, conf):
        super().__init__(conf)
        # Example: __mqtt__MQTT[Thermal]
        self.logger = logging.getLogger(f'{__name__}_{__class__.__name__}[{conf.get("function")}]')
        self.connect()

    def connect(self):
        self.logger.debug('connected!')

    def disconnect(self):
        self.logger.debug('disconnected!')

    def on_receive(self, message):
        self.logger.debug(f'New message received: {message}')

    def send(self, *data):
        self.logger.debug(f'send -> {data}')

