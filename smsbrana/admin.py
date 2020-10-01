# -*- coding: utf-8 -*-

from django.contrib import admin
from smsbrana.models import SentSms


class SentSmsAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'verification_code', 'sent_date', 'delivered', 'delivered_date')
    search_fields = ('phone_number',)
    ordering = ['-sent_date']


admin.site.register(SentSms, SentSmsAdmin)
