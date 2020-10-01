# -*- coding: utf-8 -*-
import datetime
import random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.fields import CreationDateTimeField


@python_2_unicode_compatible
class SentSms(models.Model):
    sms_id = models.IntegerField(primary_key=True)
    phone_number = models.CharField(_(u'phone number'), max_length=20, db_index=True)
    message = models.CharField(_(u'message'), max_length=500)
    verification_code = models.CharField(_(u'verification code'), max_length=10, blank=True, null=True)
    sent_date = CreationDateTimeField(_(u'created'), db_index=True)
    delivered = models.BooleanField(_(u'delivered'), default=False, db_index=True)
    delivered_date = models.DateTimeField(_(u'delivered time'), blank=True, null=True, editable=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True, db_index=True)

    def __str__(self):
        return self.phone_number

    @staticmethod
    def generate_sms_verification_code(length=6):
        choices = list(range(0, 10))
        result = []
        for i in range(0, length):
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

    @staticmethod
    def sms_to_number_delivered_in_last_hours(hours, phone_number):
        day_ago = datetime.datetime.now() - datetime.timedelta(hours=hours)
        return SentSms.objects.filter(phone_number=phone_number, sent_date__gt=day_ago, delivered=True).exists()

    @staticmethod
    def too_many_sms_to_number_sent_in_last_hours(hours, phone_number, max_sms_count=5):
        since = datetime.datetime.now() - datetime.timedelta(hours=hours)
        return SentSms.objects.filter(phone_number=phone_number, sent_date__gt=since).count() >= max_sms_count

    @staticmethod
    def too_many_sms_from_ip_sent_in_last_hours(hours, ip, max_sms_count=20):
        since = datetime.datetime.now() - datetime.timedelta(hours=hours)
        return SentSms.objects.filter(ip_address=ip, sent_date__gt=since).count() >= max_sms_count

    class Meta:
        verbose_name = _('Sent SMS')
        verbose_name_plural = _('Sent SMSes')
