# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (
    ScanEventsView, ScanEventsJSONView,
    CommandCreateFormView, CommandUpdateFormView, CommandDeleteFormView, CommandListView,
)

urlpatterns = patterns(
    '',
    url(r'^scan$', ScanEventsView.as_view(), name='bmo_scan_events'),
    url(r'^scan.json$', ScanEventsJSONView.as_view(), name='bmo_scan_json_events'),
    url(r'^command/new$', CommandCreateFormView.as_view(), name='bmo_command_create'),
    url(r'^command/(?P<pk>\d+)$', CommandUpdateFormView.as_view(), name='bmo_command_update'),
    url(r'^command/(?P<pk>\d+)/delete$', CommandDeleteFormView.as_view(), name='bmo_command_delete'),
    url(r'^commands/?$', CommandListView.as_view(), name='bmo_command_list'),
)

