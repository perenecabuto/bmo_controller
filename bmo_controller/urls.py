# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from .views import (
    ScanEventsView, ScanEventsJSONView,
    BmoCommandCreateFormView, BmoCommandUpdateFormView, BmoCommandDeleteFormView, BmoCommandListView,
    ReplayCodeView, ExectuteBmoCommandView, BmoCommandUrlListView
)

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('bmo_command_list')), name='bmo_index'),
    url(r'^scan$', ScanEventsView.as_view(), name='bmo_scan_events'),
    url(r'^scan.json$', ScanEventsJSONView.as_view(), name='bmo_scan_json_events'),
    url(r'^commands/?$', BmoCommandListView.as_view(), name='bmo_command_list'),
    url(r'^commands/urls/?$', BmoCommandUrlListView.as_view(), name='bmo_command_urls'),
    url(r'^commands/new$', BmoCommandCreateFormView.as_view(), name='bmo_command_create'),
    url(r'^commands/(?P<slug>[\w-]+)$', BmoCommandUpdateFormView.as_view(), name='bmo_command_update'),
    url(r'^commands/(?P<slug>[\w-]+)/delete$', BmoCommandDeleteFormView.as_view(), name='bmo_command_delete'),

    url(r'^execute/(?P<slug>[\w-]+)$', ExectuteBmoCommandView.as_view(), name='bmo_command_execute'),
    url(r'^replay/(?P<type>\w+)/(?P<code>\w+)/(?P<bits>\w+)/(?P<protocol>\w+)/?$', ReplayCodeView.as_view(), name='bmo_replay_command'),
)

