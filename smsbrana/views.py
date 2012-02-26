# -*- coding: utf-8 -*-
from datetime import datetime
from django.http import HttpResponse
from smsbrana import SmsConnect
from smsbrana import signals
from smsbrana.const import DELIVERY_STATUS_DELIVERED, DATETIME_FORMAT
from smsbrana.models import SentSms

def smsconnect_notification(request):
    sc = SmsConnect()
    result = sc.inbox() #TODO delete inbox?
    print result
    for delivered in result['delivery_report']:
        sms_id = delivered['idsms']
        if delivered['status'] != DELIVERY_STATUS_DELIVERED:
            continue
        try:
            sms = SentSms.objects.get(sms_id=sms_id)
            sms.delivered = True
            sms.delivered_date = datetime.strptime(delivered['time'], DATETIME_FORMAT)
            sms.save()
        except SentSms.DoesNotExist:
#            logger.error('sms delivered which wasn\'t sent' + str(delivered))
            pass

    signals.smsconnect_notification_received.send(sender=None, inbox=result, request=request)#TODO document this
    return HttpResponse('OK')

