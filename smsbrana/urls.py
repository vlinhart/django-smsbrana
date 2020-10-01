# -*- coding: utf-8 -*-
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from . import views

urlpatterns = [
    url(r'^notification/$', views.smsconnect_notification, name='smsconnect_notification'),
]
