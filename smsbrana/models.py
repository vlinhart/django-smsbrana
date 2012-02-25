# -*- coding: utf-8 -*-
import datetime
import random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField

class SentSms(models.Model):
    sms_id = models.IntegerField(primary_key=True)
    phone_number = models.CharField(_(u'phone number'), max_length=20)
    message = models.CharField(_(u'message'), max_length=500)
    verification_code = models.CharField(_(u'verification code'), max_length=10, blank=True, null=True)
    sent_date = CreationDateTimeField(_(u'created'))
    delivered = models.BooleanField(_(u'delivered'))
    delivered_date = models.DateTimeField(_(u'delivered time'), blank=True, null=True, editable=False)
    ip_address = models.IPAddressField(blank=True, null=True)

    def __unicode__(self):
        return self.phone_number

    @staticmethod
    def generate_sms_verification_code(length=6):
        choices = range(0, 10)
        result = []
        for i in xrange(0, length):
            result.append(str(random.choice(choices)))
        return ''.join(result)

    @staticmethod
    def can_send_from_ip(ip, time_allowance=30):
        """
        ``time_allowance``
           in seconds, when can be sent another sms from the same IP address
        """
        allow_after = datetime.datetime.now() - datetime.timedelta(seconds=time_allowance)
        return not SentSms.objects.filter(ip_address=ip, sent_date__gt=allow_after).exists()

    class Meta:
        verbose_name = _('Sent SMS')
        verbose_name_plural = _('Sent SMSes')
