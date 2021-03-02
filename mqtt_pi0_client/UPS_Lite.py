#!/usr/bin/env python
import struct
import smbus
import sys
import time
import RPi.GPIO as GPIO

from event import *

LEAST_QUERY_PERIOD_IN_SECONDS = 60
LOW_VOLTAGE_THRESHOLD = 1.1 # 1.1 of 100

class UPSLite():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(4, GPIO.IN)

        self._bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

        self.__PowerOnReset()
        self.__QuickStart()

        self.__old_query_time = 0
        self.__power_low_cnt = 0

        #self.__current_voltage = None
        #self.__current_capacity = None

    def __QuickStart(self):
        address = 0x36
        self._bus.write_word_data(address, 0x06, 0x4000)

    def __PowerOnReset(self):
        address = 0x36
        self._bus.write_word_data(address, 0xfe, 0x0054)

    def update(self, event_queue):
        t = time.time()
        if self.__old_query_time == 0 or (t - self.__old_query_time) > LEAST_QUERY_PERIOD_IN_SECONDS:
            v = self.__get_voltage()
            c = self.__get_capacity()
            event_queue.put_nowait(PowerEvent(v, c))
            self.__old_query_time = t

            # capacity is low, next query do not wait
            if c < LOW_VOLTAGE_THRESHOLD:
                self.__old_query_time = 0
                self.__power_low_cnt += 1
                if self.__power_low_cnt >= 3:
                    event_queue.put_nowait(PowerLowEvent(v, c))
            else:
                self.__power_low_cnt = 0

            #self.__current_voltage = v
            #self.__current_capacity = c

    def __get_voltage(self):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = self._bus.read_word_data(address, 0X02)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 / 1000 / 16
        return voltage

    def __get_capacity(self):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = self._bus.read_word_data(address, 0X04)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped / 256
        return capacity

    #def power_adapter_plug_in(self):
    #    return GPIO.input(4) == GPIO.HIGH

"""
    "Voltage:%5.2fV" % readVoltage(bus)
    "Battery:%5i%%" % readCapacity(bus)
    if (GPIO.input(4) == GPIO.HIGH):
        "Power Adapter Plug In "
    if (GPIO.input(4) == GPIO.LOW):
        "Power Adapter Unplug"
"""
