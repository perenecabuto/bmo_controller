# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import modelformset_factory

from .models import Command, Listener


class CommandForm(forms.ModelForm):
    class Meta:
        model = Command


class ListenerForm(forms.ModelForm):

    class Meta:
        model = Listener
        fields = ('system_command', 'trigger_command')


ListenerFormSet = modelformset_factory(Listener, form=ListenerForm, extra=1)

