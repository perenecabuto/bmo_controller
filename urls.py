# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from bmo_controller import urls as bmo_urls

from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'bmo_controller/', include(bmo_urls)),
    url(r'^$', RedirectView.as_view(url='bmo_controller/scan', permanent=False)),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
