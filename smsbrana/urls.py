# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('.views',
    url(r'^notification/$', 'smsconnect_notification', name='smsconnect_notification'),

)
