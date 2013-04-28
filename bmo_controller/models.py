# -*- coding: utf-8 -*-

from django.db import models


class Command(models.Model):
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
    code = models.CharField(max_length=64)


class Listener(models.Model):
    command = models.ForeignKey(Command)
    system_command = models.CharField(max_length=255, null=True, blank=True)
    trigger_command = models.ForeignKey(Command, related_name="trigger_command", null=True, blank=True)

    def save(self, **kwargs):

        if not self.system_command and not self.trigger_command:
            raise ListenerStateException("system_command or trigger_command should be defined")

        self.save(**kwargs)


class Events(models.Model):
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "At %s: %s" % (self.date, self.message)


class ListenerStateException(Exception):
    pass
