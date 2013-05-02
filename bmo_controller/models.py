# -*- coding: utf-8 -*-

import subprocess

from django.core.exceptions import ValidationError
from django.db import models

from .driver import BmoDriver


class Command(models.Model):
    label = models.CharField(unique=True, max_length=255)
    type = models.CharField(max_length=64)
    code = models.CharField(max_length=64)

    def __unicode__(self):
        return self.label

    def execute(self):
        driver = BmoDriver()
        driver.send_code(self.type, self.code)

        for listener in self.listener_set.all():
            listener.execute()

    class Meta:
        unique_together = ("type", "code")


class Listener(models.Model):
    command = models.ForeignKey(Command)
    system_command = models.CharField(max_length=255, null=True, blank=True)
    trigger_command = models.ForeignKey(Command, related_name="trigger_command", null=True, blank=True)

    def execute(self):
        if self.system_command.strip():
            subprocess.call(self.system_command.split(" "))
        elif self.trigger_command:
            print "other"
            driver = BmoDriver()
            driver.send_code(self.trigger_command.type, self.trigger_command.code)

    def save(self, **kwargs):

        if not self.system_command and not self.trigger_command:
            raise ValidationError("system_command or trigger_command should be defined")

        return super(Listener, self).save(**kwargs)


class Events(models.Model):
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "At %s: %s" % (self.date, self.message)


class ListenerStateException(Exception):
    pass
