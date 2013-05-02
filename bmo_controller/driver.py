# -*- coding: utf-8 -*-

import os
from glob import glob
from serial import Serial


class BmoDriver(object):

    def get_connetion(self):
        port = '/dev/ttyUSB0'
        found_devices = glob('/dev/serial/by-id/*FTDI*')

        if found_devices:
            port = os.path.realpath(found_devices[0])

        return Serial(port, 9600)

    def send_code(self, signal_type, code):
        connection = self.get_connetion()
        connection.write("%s\n" % code)
