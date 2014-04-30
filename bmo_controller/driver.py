# -*- coding: utf-8 -*-

import os
from glob import glob
from serial import Serial


class BmoDriver(object):

    def get_connetion(self):
        found_devices = (
            glob('/dev/serial/by-id/*Arduino*') or  # Arduino uno
            glob('/dev/serial/by-id/*FTDI*') or  # Old Arduinos
            glob('/dev/tty.usbmodem*')  # Mac OS X
        )

        if not found_devices:
            raise NoBMODeviceFoundException

        port = os.path.realpath(found_devices[0])

        return Serial(port, 9600)

    def send_code(self, signal_type, code, bits=0, protocol=""):
        connection = self.get_connetion()
        connection.write("%s %s %s %s\n" % (signal_type, code, bits, protocol))

    def get_bmo_message(self):
        connection = self.get_connetion()
        return connection.readline()


class NoBMODeviceFoundException(Exception):
    pass
