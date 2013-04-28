# -*- coding: utf-8 -*-

import os
from glob import glob
from serial import Serial

port = '/dev/ttyUSB0'
found_devices = glob('/dev/serial/by-id/*FTDI*')

if found_devices:
    port = os.path.realpath(found_devices[0])

arduino = Serial(port, 9600)

arduino.write('Covo')
