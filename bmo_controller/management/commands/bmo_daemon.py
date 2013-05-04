# -*- coding: utf-8 -*-

import os
from glob import glob
import logging

from serial import Serial, SerialException
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from bmo_controller.models import Events


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Bmo daemon"

    def handle(self, *args, **options):
        port = '/dev/ttyUSB0'
        found_devices = glob('/dev/serial/by-id/*FTDI*')

        if found_devices:
            port = os.path.realpath(found_devices[0])

        arduino = Serial(port, 9600)

        while True:
            try:
                message = arduino.readline()

                try:
                    if not isinstance(json.loads(message), dict):
                        raise ValueError
                except ValueError:
                    print "Skiping malformed message:\n\t%s\n" % message
                    continue

                if getattr(settings, 'DEBUG', False):
                    print message
                    logger.debug(message)

                event = Events(message=message)
                event.save()

            except SerialException:
                arduino = Serial(port, 9600)
