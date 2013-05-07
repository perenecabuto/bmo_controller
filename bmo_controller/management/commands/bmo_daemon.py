# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import DatabaseError

from bmo_controller.models import Events
from bmo_controller.driver import BmoDriver


class Command(BaseCommand):
    help = "Bmo daemon"

    def handle(self, *args, **options):
        print " * Starting BMO Daemon\n"
        driver = BmoDriver()

        while True:
            message = driver.get_bmo_message()

            if settings.DEBUG:
                print message

            try:
                event, _ = Events.objects.get_or_create(message=message)
                event.save()
            except DatabaseError:
                pass
