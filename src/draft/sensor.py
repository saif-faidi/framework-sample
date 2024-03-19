import threading
import random
import time
import logging


class Sensor:

    def __init__(self, protocol):
        self.logger = logging.getLogger(__name__)
        self.protocol = protocol
        self.thread = threading.Thread(target=self.run)
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            random_value = random.randint(0, 100)
            random_value = str(random_value)
            self.protocol.send(random_value, 'Topic', 2, False)
            time.sleep(1)

    def set_receive_func(self, func):
        self.protocol.receive = func

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
