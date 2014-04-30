# -*- coding: utf-8 -*-

import subprocess

import json

from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.core.urlresolvers import reverse

from .driver import BmoDriver


class Command(models.Model):
    slug = AutoSlugField(populate_from='label', overwrite='true')
    label = models.CharField(unique=True, max_length=255)
    type = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    bits = models.IntegerField()
    protocol = models.CharField(max_length=32)

    def __unicode__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('bmo_command_execute', kwargs={'slug': self.slug})

    def execute(self):
        driver = BmoDriver()
        driver.send_code(self.type, self.code, self.bits, self.protocol)

        for listener in self.listener_set.all():
            listener.execute()

    class Meta:
        unique_together = ("type", "code", "protocol", "bits")


class Listener(models.Model):
    command = models.ForeignKey(Command)
    system_command = models.CharField(max_length=255, null=True, blank=True)
    trigger_command = models.ForeignKey(Command, related_name="trigger_command", null=True, blank=True)

    def execute(self):
        if self.system_command.strip():
            subprocess.call(self.system_command.split(" "))

        elif self.trigger_command:
            self.trigger_command.execute()

    def save(self, **kwargs):

        if not self.system_command and not self.trigger_command:
            raise ValidationError("system_command or trigger_command should be defined")

        if self.command == self.trigger_command:
            raise ValidationError("trigger command should not be equal to listener default command")

        return super(Listener, self).save(**kwargs)


class Events(models.Model):
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "At %s: %s" % (self.date, self.message)

    def save(self, **kwargs):
        try:
            if not isinstance(json.loads(self.message), dict):
                raise ValueError
        except ValueError:
            raise ValidationError("Skiping malformed message:\n%s\n%s" % (self.message, "-" * 80))

        return super(Events, self).save(**kwargs)


class ListenerStateException(Exception):
    pass
