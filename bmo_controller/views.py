# -*- coding: utf-8 -*-

import json

from django.views.generic.list import BaseListView, ListView
from django.http import HttpResponse

from bmo_controller.models import Events


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
