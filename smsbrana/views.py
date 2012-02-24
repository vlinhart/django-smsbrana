# -*- coding: utf-8 -*-
from datetime import datetime
from django.http import HttpResponse
from smsconnect import signals, SentSms
import smsconnect
import logging

logger = logging.getLogger(__name__)

def smsconnect_notification(request):
    result = smsconnect.inbox()
    print result
    for delivered in result['delivery_report']:
        sms_id = delivered['idsms']
        try:
            sms = SentSms.objects.get(sms_id=sms_id)
            sms.delivered = True
            sms.delivered_date = datetime.now()
            sms.save()
        except SentSms.DoesNotExist:
            logger.error('sms delivered which wasn\'t sent' + str(delivered))

    signals.smsconnect_notification_received.send(sender=None, inbox=result, request=request)#TODO document this
    return HttpResponse('OK')

