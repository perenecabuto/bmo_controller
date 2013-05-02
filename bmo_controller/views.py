# -*- coding: utf-8 -*-

import json

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic.list import BaseListView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from bmo_controller.models import Command, Events
from bmo_controller.forms import CommandForm

# Command


class BaseCommandMixin(object):
    form_class = CommandForm
    model = Command
    success_url = reverse_lazy('bmo_command_list')


class CommandCreateFormView(BaseCommandMixin, CreateView):
    template_name = "bmo_controller/command_form.html"

    def get_initial(self):
        if self.request.method == 'GET':
            return {k: str(v) for k, v in self.request.GET.items()}


class CommandUpdateFormView(BaseCommandMixin, UpdateView):
    template_name = "bmo_controller/command_form.html"


class CommandDeleteFormView(BaseCommandMixin, DeleteView):
    pass


class CommandListView(ListView):
    template_name = "bmo_controller/command_list.html"
    model = Command


# Events


class EventsMixin(object):

    def get_queryset(self):
        return Events.objects.all().order_by('-date')


class ScanEventsView(EventsMixin, ListView):
    template_name = 'bmo_controller/scan_events.html'

    def get_queryset(self):
        return super(ScanEventsView, self).get_queryset()[:10]


class ScanEventsJSONView(EventsMixin, BaseListView):

    def get(self, request, *args, **kwargs):
        events = self.get_queryset()

        if 'after' in request.GET:
            events = events.filter(date__gt=request.GET['after'])

        messages = [
            {'date': str(event.date), 'message': json.loads(event.message)}
            for event in events[:10]
        ]

        return HttpResponse(json.dumps(messages, ))
