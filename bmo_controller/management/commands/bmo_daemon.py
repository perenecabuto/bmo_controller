# -*- coding: utf-8 -*-

import logging
import time
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import DatabaseError

from bmo_controller.models import Events, BmoCommand, driver


class Command(BaseCommand):
    help = "Bmo daemon"

    def handle(self, *args, **options):
        print " * Starting BMO Daemon\n"

        while True:
            try:
                message = driver.get_bmo_message()

                #if settings.DEBUG:
                    #print message
                self.find_and_run_command_by_message(message)

                try:
                    event, _ = Events.objects.get_or_create(message=message)

                    event.save()
                except DatabaseError:
                    pass

            except Exception as e:
                logging.exception(e)
                time.sleep(2)

    def find_and_run_command_by_message(self, message):
        message = json.loads(message)

        if BmoCommand.objects.filter(**message).exists():
            command = BmoCommand.objects.get(**message)
            print "Executing command (%s) hooks" % command.label

            for listener in command.listener_set.all():
                listener.execute()
