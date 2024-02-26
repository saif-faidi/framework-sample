import paho.mqtt.client as mqtt
from src.network.protocol import Protocol
import socket


class MQTT(Protocol):

    SUCCESS = 0

    def __init__(self, conf):
        super().__init__(conf)
        self.sub_topics                     = []
        self.__mqtt_client_id               = f'{socket.gethostname()}:{self.function}'
        self.__check_mqtt_last_time         = 0
        self.__mqtt_need_to_connect         = True
        self.__mqtt_disconnect_before_exit  = False
        self.init_mqtt()

    def connect(self):
        ''' TODO: make this subscribe method not a connect method'''
        for topic in self.sub_topics:
            self.mqttc.subscribe(topic, 2)

    def disconnect(self):
        pass

    def receive(self, message):
        print(f'New MQTT message: {message.topic} => {str(message.payload.decode(errors="ignore"))}')

    def send(self, *data):
        topic, value, qos, retain = data
        res = self.mqttc.publish(topic, value, qos, retain)
        if res.rc != mqtt.MQTT_ERR_SUCCESS:
            # TODO change with logger, maybe add retry !
            print(f'Failed to send message, Error: {res.rc}')


    def init_mqtt(self):

        def on_connect_local_callback(client, userdata, flags, rc) -> None:
            '''
            :param client       : The mqtt client that triggered the callback
            :param userdata     : parameter that can be used to pass custom user data to the callback itself
             not related to this mqtt client, we passed defined "self" instance to be able to use the defined callbacks
            :param flags        :
            :param rc           : return code of the mqtt operation
            :return:
            '''
            if rc != MQTT.SUCCESS:
                userdata.error(f"failed to connect to MQTT broker, return code '{rc}', exiting...")
                userdata.exit_loop_event.set()
            else:
                userdata.connect()

        def on_disconnect_local_callback(client, userdata, rc):
            userdata.disconnect()

        def on_message_local_callback(client, userdata, message):
            userdata.receive(message)

        self.mqttc                  = mqtt.Client(client_id=self.__mqtt_client_id, userdata=self)
        self.mqttc.on_connect       = on_connect_local_callback
        self.mqttc.on_disconnect    = on_disconnect_local_callback
        self.mqttc.on_message       = on_message_local_callback

    def on_exit(self):
        if self.__mqtt_disconnect_before_exit: self.mqttc.disconnect()

