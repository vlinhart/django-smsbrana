# -*- coding: utf-8 -*-
from django.dispatch import Signal

# A new user has registered.
smsconnect_notification_received = Signal(providing_args=['inbox', 'request'])
smsconnect_sms_sent = Signal(providing_args=['phone_number', 'text'])
