# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('smsconnect.views',
    url(r'^notification/$', 'smsconnect_notification', name='smsconnect_notification'),

)
