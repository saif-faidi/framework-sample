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
            if  received_data:
                self.on_receive(received_data)
            else:
                self._on_disconnect_clbk()

    def disconnect(self):
        self.stop_recv_event.set()
        self.client_socket.close()

    def on_receive(self, message):
        self.logger.info(f'received {message}')


    def send(self, *data):
        if data :
            value = data[0]
            try:
                self.client_socket.sendall(value.encode())
            except socket.error as e:
                self.logger.error(f"Error: Failed to send data, reason : {e}")


    def _on_disconnect_clbk(self):
        self.logger.critical('Unexpected disconnection. Reconnecting...')
        self.__tcp_need_to_connect = True
        self.connect()
