# -*- coding: utf-8 -*-

import json

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse

from django.views.generic import View
from django.views.generic.list import BaseListView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from bmo_controller.models import Command, Listener, Events
from bmo_controller.forms import (
    CommandForm, ListenerFormSet
)

from bmo_controller.driver import BmoDriver

# Command


class BaseCommandMixin(object):
    form_class = CommandForm
    model = Command
    success_url = reverse_lazy('bmo_command_list')

    def get_form(self, form):
        form = super(BaseCommandMixin, self).get_form(form)

        if self.request.method == 'POST':
            self.listener_formset = ListenerFormSet(self.request.POST)
        else:
            qs = self.object.listener_set.all() if self.object else Listener.objects.none()
            self.listener_formset = ListenerFormSet(queryset=qs)
            self.listener_formset.data.update(self.request.GET)

        return form

    def get_context_data(self, **kwargs):
        context_data = super(BaseCommandMixin, self).get_context_data(**kwargs)
        context_data['listener_formset'] = self.listener_formset

        return context_data

    def form_valid(self, form):
        if self.listener_formset.is_valid():
            self.object = form.save()

            for f in self.listener_formset.forms:
                listener = f.save(commit=False)
                listener.command = self.object
                try:
                    listener.save()
                except ValidationError:
                    pass

        return super(BaseCommandMixin, self).form_valid(form)


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


# Replay

class ReplayCodeView(View):

    def get(self, request, *args, **kwargs):
        driver = BmoDriver()
        driver.send_code(kwargs.get('type'), kwargs.get('code'))

        return HttpResponse('ok')
