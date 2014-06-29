# -*- coding: utf-8 -*-
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url


urlpatterns = patterns('smsbrana.views',
    url(r'^notification/$', 'smsconnect_notification', name='smsconnect_notification'),

)
