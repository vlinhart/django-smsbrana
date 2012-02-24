# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField

class SentSms(models.Model):
    sms_id = models.IntegerField(primary_key=True)
    phone_number = models.CharField(_(u'phone number'), max_length=20)
    message = models.CharField(_(u'message'), max_length=500)
    sent_date = CreationDateTimeField(_(u'created'))
    delivered = models.BooleanField(_(u'delivered'))
    delivered_date = models.DateTimeField(_(u'delivered time'), blank=True, null=True, editable=False)

    def __unicode__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('Sent SMS')
        verbose_name_plural = _('Sent SMSes')
