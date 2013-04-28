# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from bmo_controller import urls as bmo_urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', include(bmo_urls)),
)
