#!/usr/bin/env python3
# coding: utf-8

# function Thermal

import os
import logging


class Thermal:

    def __init__(self, config, protocol = None):
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        super().__init__()
        self.logger     = logging.getLogger(f'{__name__}_{__class__.__name__}')
        self.config     = config
        self.protocol   = protocol
        #can be ignored if we use another protocol than MQTT
        self.sub_topics = self.config.get('protocol').get('sub_topics')
        self.pub_topics = self.config.get('protocol').get('pub_topics')
        self.protocol.set_on_receive_callback(self.mqtt_on_message)

        ventilation_levels  = self.config.get('ventilation_levels')
        self.max_vent_level = ventilation_levels[len(ventilation_levels)-1]
        self.min_vent_level = ventilation_levels[0]

        heating_levels      = self.config.get('heating_levels')
        self.max_heat_level = ventilation_levels[len(heating_levels) - 1]
        self.min_heat_level = ventilation_levels[0]


    def mqtt_on_message(self, message):
        topic = message.topic
        try:
            received_message = int(message.payload.decode(errors='ignore'))
            if received_message > self.max_vent_level: received_message = self.max_vent_level
            if received_message < self.min_vent_level: received_message = self.min_vent_level
        except Exception as e:
            self.logger.warning(f'value error for topic value, expected int but got {message.payload.decode(errors="ignore")}')
            return
        if message.topic == self.sub_topics.get('heat_all_sub'):
            self.protocol.send(received_message, self.pub_topics.get('heat_all_pub'), 2, False)
        if message.topic == self.sub_topics.get('heat_backrest_sub'):
            self.protocol.send(received_message, self.pub_topics.get('heat_backrest_pub'), 2, False)
        if message.topic == self.sub_topics.get('heat_cushion_sub'):
            self.protocol.send(received_message, self.pub_topics.get('heat_cushion_pub'), 2, False)
        # call the LIN interface to Control the TFIT.
        self.logger.info(f'send message {"3"} over LIN to ECU...')

    def on_exit(self):
        self.protocol.disconnect()


