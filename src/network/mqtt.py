import sys
import time
import socket
import logging
import paho.mqtt.client as mqtt

from src.network.protocol import Protocol


class MQTT(Protocol):

    def __init__(self, conf):
        super().__init__(conf)
        self.mqttc                      = None
        self.sub_topics                 = conf.get('sub_topics') or []
        self.__mqtt_client_id           = f'{socket.gethostname()}:{self.function}'
        self.__check_mqtt_last_time     = 0
        self.__mqtt_need_to_connect     = True
        self.logger                     = logging.getLogger(__name__)

        self.init_mqtt()
        self.connect()
        self.subscribe()

    def connect(self):
        while self.__mqtt_need_to_connect:

            if time.time() > self.__check_mqtt_last_time + self.retry_s:
                self.__check_mqtt_last_time = time.time()
                if self.host and self.port:
                    try:
                        self.mqttc.connect(self.host, self.port)
                        self.__mqtt_need_to_connect = False
                        self.mqttc.loop_start()
                        time.sleep(.1)
                    except Exception:
                        self.logger.warning(f'Failed to connect to MQTT broker, retrying in {self.retry_s} second...')
                    else:
                        self.logger.info('Successfully connected to MQTT Broker')

                else:
                    self.logger.error(f'({self.host}, {self.port}) is not a valid socket, exiting...')
                    self.__mqtt_need_to_connect = False
                    sys.exit(1)

    def subscribe(self):
        """ Subscribe to all topics from config file"""
        for topic in self.sub_topics:
            self.mqttc.subscribe(topic, 2)

    def disconnect(self):
        self.mqttc.disconnect()

    def receive(self, message):
        self.logger.debug(f'New MQTT message: {message.topic} => {str(message.payload.decode(errors="ignore"))}')

    def send(self, *data):
        topic, value, qos, retain = data
        res = self.mqttc.publish(topic, value, qos, retain)
        if res.rc != mqtt.MQTT_ERR_SUCCESS:
            if res.rc == mqtt.MQTT_ERR_NO_CONN:
                self.logger.error('Failed to send message, Broker closed the TCP connection! error code : (4 = MQTT_ERR_NO_CONN)')
            else:
                self.logger.error(f'Failed to send message, Error code: {res.rc}')

    def init_mqtt(self):
        def on_connect_local_callback(client, userdata, flags, rc) -> None:
            """
            :param client       : The mqtt client that triggered the callback
            :param userdata     : parameter that can be used to pass custom user data to the callback itself that's
             not related to this mqtt client, we passed defined "self" instance to be able to use the defined callbacks
            :param flags        : used to handle qos, retain..
            :param rc           : return code of the mqtt operation
            :return:
            """
            if rc != mqtt.MQTT_ERR_SUCCESS:
                userdata.error(f'failed to connect to MQTT broker, return code "{rc}", exiting...')
                # userdata.exit_loop_event.set()
            else:
                userdata.connect()

        def on_disconnect_local_callback(client, userdata, rc):
            if rc != 0:
                self.logger.critical('Unexpected disconnection. Reconnecting...')
                userdata.__mqtt_need_to_connect = True
                self.connect()
                self.logger.info('Connection is back!')
            userdata.disconnect()

        def on_message_local_callback(client, userdata, message):
            userdata.receive(message)

        self.mqttc = mqtt.Client(client_id=self.__mqtt_client_id, userdata=self)
        self.mqttc.on_connect = on_connect_local_callback
        self.mqttc.on_disconnect = on_disconnect_local_callback
        self.mqttc.on_message = on_message_local_callback
C:\Users\saif\Documents\software\ces_24-aio_last\ces_24-aio_last\functions\tcpip_gateway