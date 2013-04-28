# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (
    ScanEventsView, ScanEventsJSONView
)

urlpatterns = patterns(
    '',
    url(r'^scan$', ScanEventsView.as_view(), name='bmo_scan_events'),
    url(r'^scan.json$', ScanEventsJSONView.as_view(), name='bmo_scan_json_events'),
)

