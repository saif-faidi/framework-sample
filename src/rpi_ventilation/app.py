#!/usr/bin/env python3
# coding: utf-8


import os
import time
import pigpio
import logging

class RPI_Ventilation:

    def __init__(self, config, protocol = None):

        self.logger     = logging.getLogger(f'{__name__}{__class__.__name__}')
        self.config     = config
        self.protocol   = protocol
        #can be ignored if we use another protocol than MQTT
        self.sub_topics = self.config.get('protocol').get('sub_topics')
        self.pub_topics = self.config.get('protocol').get('pub_topics')
        self.protocol.set_on_receive_callback(self.mqtt_on_message)
        # Set GPIOs to output and reset duty cycle
        os.system('sudo pigpiod')
        time.sleep(2)
        self.gpio_backrest  = self.config.get('gpio_backrest')
        self.gpio_cushion   = self.config.get('gpio_cushion')
        frequency           = self.config.get('frequency')
        self.pi             = pigpio.pi()
        self._init_gpio(self.gpio_backrest, frequency)
        self._init_gpio(self.gpio_cushion, frequency)

        ventilation_levels  = self.config.get('ventilation_levels')
        self.max_vent_level = ventilation_levels[len(ventilation_levels)-1]
        self.min_vent_level = ventilation_levels[0]


    def _init_gpio(self, gpio_pin, frequency):
        self.set_GPIO(gpio_pin, 'out', 1)
        self.pi.set_mode(gpio_pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(gpio_pin, frequency)
        self.pi.set_PWM_dutycycle(gpio_pin, 0)


    def on_exit(self):
        self.protocol.disconnect()
        self.pi.set_PWM_dutycycle(self.gpio_backrest, 0)
        self.pi.set_PWM_dutycycle(self.gpio_cushion, 0)
        self.pi.stop()  # disconnect the pigpio

    def set_GPIO(self, GPIO, Dir, Value):
        os.system(f'echo {GPIO} > /sys/class/gpio/export')              # request access to GPIO (activate)
        os.system(f'echo {Dir} > /sys/class/gpio/gpio{GPIO}/direction') # set GPIO direction ( input or output)
        os.system(f'echo {Value} > /sys/class/gpio/gpio{GPIO}/value')   # set the vaue of the GPIO ( in our case set to 1 since LIN bus recessif state is 1)

    def unset_GPIO(self, GPIO, Dir, Value):
        os.system('echo {Value} > /sys/class/gpio/gpio{GPIO}/value')    # put signal to "value", in our case to 0 which is the default value of the pin
        os.system('echo {Dir} > /sys/class/gpio/gpio{GPIO}/direction')  # set direction(in or out), in our case put it to 'in' which is the default value for gpio pin
        os.system('echo {GPIO} > /sys/class/gpio/unexport')             # deactivate GPIO (unexport)


    def mqtt_on_message(self, message):
        topic = message.topic
        try:
            received_message = int(message.payload.decode(errors='ignore'))
            if received_message > self.max_vent_level: received_message = self.max_vent_level
            if received_message < self.min_vent_level: received_message = self.min_vent_level
            # 1 -> 10, 2-> 50, 3 ->90
            duty_cycle = (40 * received_message - 30) if received_message != 0 else 0
            # duty cycle is between 0-255
            duty_cycle = int((duty_cycle * 0.01) * 255)
        except Exception as e:
            self.logger.warning(f'value error for topic value, expected int but got {message.payload.decode(errors="ignore")}')
            return
        if topic == self.sub_topics.get('vent_all_sub'):
            self.protocol.send(received_message,self.pub_topics.get('vent_all_pub'),2, False)
            self.pi.set_PWM_dutycycle(self.gpio_backrest, duty_cycle)
            self.pi.set_PWM_dutycycle(self.gpio_cushion, duty_cycle)
        if message.topic == self.sub_topics.get('vent_backrest_sub'):
            self.protocol.send(received_message, self.pub_topics.get('vent_backrest_pub'), 2,False)
            self.pi.set_PWM_dutycycle(self.gpio_backrest, duty_cycle)
            # self.pwm_backrest.ChangeDutyCycle(duty_cycle)
        if message.topic == self.sub_topics.get('heat_cushion_sub'):
            self.protocol.send(received_message, self.pub_topics.get('vent_cushion_pub'), 2,False)
            self.pi.set_PWM_dutycycle(self.gpio_cushion, duty_cycle)
            # self.pwm_backrest.ChangeDutyCycle(duty_cycle)



