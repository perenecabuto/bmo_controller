# -*- coding: utf-8 -*-

import os
from glob import glob
from serial import Serial
from serial.serialposix import SerialException


class BmoDriver(object):

    @property
    def connection(self):
        if not getattr(self, '_connection', None):
            found_devices = (
                glob('/dev/serial/by-id/*Arduino*') or  # Arduino uno
                glob('/dev/serial/by-id/*FTDI*') or  # Old Arduinos
                glob('/dev/tty.usbmodem*')  # Mac OS X
            )

            if not found_devices:
                raise NoBMODeviceFoundException

            port = os.path.realpath(found_devices[0])

            self._connection = Serial(port, 115200)

        return self._connection

    def send_code(self, signal_type, code, bits=0, protocol=""):
        message = "%s %s %s %s\n" % (signal_type, code, bits, protocol)
        try:
            self.connection.write(str(message))
        except SerialException:
            self._connection = None
            self.send_code(signal_type, code, bits, protocol)

    def get_bmo_message(self):
        return self.connection.readline()


class NoBMODeviceFoundException(Exception):
    pass
