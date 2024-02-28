import sys
import threading
import time
import socket
import logging


from src.network.protocol import Protocol


class TCPClient(Protocol):
    DEFAULT_BUFF_SIZE = 1024
    def __init__(self, conf):
        super().__init__(conf)
        self.buff_size                 = conf.get('buffer_size', TCPClient.DEFAULT_BUFF_SIZE)
        self.client_socket             = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__check_tcp_last_time     = 0
        self.__tcp_need_to_connect     = True
        self.logger                    = logging.getLogger(__name__)
        self.thread                    = threading.Thread(target=self.receive_loop)
        self.stop_recv_event           = threading.Event()

        self.logger = logging.getLogger(__name__)

        self.init_mqtt()
        self.connect()


    def connect(self):
        while self.__tcp_need_to_connect:
            if time.time() > self.__check_tcp_last_time + self.retry_s:
                self.__check_tcp_last_time = time.time()
                if self.host and self.port:
                    try:
                        self.client_socket.connect((self.host, self.port))
                        self.__tcp_need_to_connect = False
                        time.sleep(.1)
                    except Exception:
                        self.logger.warning(f'Failed to connect to TCP Server, retrying in {self.retry_s} second...')
                    else:
                        self.logger.info('Successfully connected to TCP Server')

                else:
                    self.logger.error(f'({self.host}, {self.port}) is not a valid socket, exiting...')
                    self.__tcp_need_to_connect = False
                    sys.exit(1)

    def receive_loop(self):
        while not self.stop_recv_event.is_set():
            received_data = self.client_socket.recv( self.buff_size ).decode()
            if not received_data:
                self.logger.error('Connection closed by server!')
            else:
                self.on_receive(received_data)


    def disconnect(self):
        self.stop_recv_event.set()
        self.client_socket.close()

    def on_receive(self, message):
        self.logger.info(f'received {message}')


    def send(self, *data):
        if data :
            _data = data[0]
            try:
                self.client_socket.sendall(_data.encode())
            except socket.error as e:
                self.logger.error(f"Error: Failed to send data, reason : {e}")


    def init_tcp(self):
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
                userdata.__tcp_need_to_connect = True
                self.connect()
                self.logger.info('Connection is back!')
            else:
                userdata.disconnect()

        def on_message_local_callback(client, userdata, message):
            userdata.receive(message)

        self.mqttc = mqtt.Client(client_id=self.__mqtt_client_id, userdata=self)
        self.mqttc.on_connect = on_connect_local_callback
        self.mqttc.on_disconnect = on_disconnect_local_callback
        self.mqttc.on_message = on_message_local_callback
