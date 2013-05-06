# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from .views import (
    ScanEventsView, ScanEventsJSONView,
    CommandCreateFormView, CommandUpdateFormView, CommandDeleteFormView, CommandListView,
    ReplayCodeView, ExectuteCommandView,
)

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('bmo_command_list')), name='bmo_index'),
    url(r'^scan$', ScanEventsView.as_view(), name='bmo_scan_events'),
    url(r'^scan.json$', ScanEventsJSONView.as_view(), name='bmo_scan_json_events'),
    url(r'^command/new$', CommandCreateFormView.as_view(), name='bmo_command_create'),
    url(r'^command/(?P<pk>\d+)$', CommandUpdateFormView.as_view(), name='bmo_command_update'),
    url(r'^command/(?P<pk>\d+)/delete$', CommandDeleteFormView.as_view(), name='bmo_command_delete'),
    url(r'^commands/?$', CommandListView.as_view(), name='bmo_command_list'),

    url(r'^replay/(?P<type>\w+)/(?P<code>\w+)/(?P<bits>\w+)/(?P<protocol>\w+)/?$', ReplayCodeView.as_view(), name='bmo_replay_command'),
    url(r'^execute/(?P<command_id>\d+)$', ExectuteCommandView.as_view(), name='bmo_execute_command'),
)

