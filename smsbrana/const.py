# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

ERROR_CODES = {
    '0': _(u'OK'),
    '1': _(u'neznámá chyba'),
    '2': _(u'neplatný login'),
    '3': _(u'neplatný hash nebo password (podle varianty zabezpecení prihlášení)'),
    '4': _(u'neplatný time, vetší odchylka casu mezi servery než maximální akceptovaná v nastavení služby SMS Connect'),
    '5': _(u'nepovolená IP, viz nastavení služby SMS Connect'),
    '6': _(u'neplatný název akce'),
    '7': _(u'tato sůl byla již jednou za daný den použita'),
    '8': _(u'nebylo navázáno spojení s databází'),
    '9': _(u'nedostatecný kredit'),
    '10': _(u'neplatné císlo príjemce SMS'),
    '11': _(u'prázdný text zprávy'),
    '12': _(u'SMS je delší než povolených 459 znaků'),
    }

API_ACCES_POINT = 'http://api.smsbrana.cz/smsconnect/http.php'


