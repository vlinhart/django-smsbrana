# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime
import uuid
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import urllib
import hashlib
from django.utils.encoding import force_unicode, smart_str
from smsbrana import const, signals
import requests
import xml.etree.ElementTree as ET
from smsbrana.const import DATETIME_FORMAT

class SmsConnectException(Exception): pass

debug = False

def require_settings(name):
    try:
        return getattr(settings, name)
    except AttributeError:
        raise ImproperlyConfigured("SMS CONNECT: You must set the '%s' in settings file." % name)

require_settings('SMS_CONNECT_LOGIN')
require_settings('SMS_CONNECT_PASSWORD')

SECURE = getattr(settings, 'SMS_CONNECT_SECURE', True)
SENDER_ID = getattr(settings, 'SMS_CONNECT_SENDER_ID', None)

def parse_simple_response_xml_to_dict(xml):
    tree = ET.XML(xml)
    response_dict = {}
    for e in tree:
        response_dict[e.tag] = e.text
    return response_dict


def parse_inbox_xml_to_dict(xml):
    tree = ET.XML(xml)

    def parse_items_in(in_param):
        response_dict = defaultdict(list)
        for item in tree.findall('inbox/%s/item' % in_param):
            item_dict = {}
            for values in item:
                item_dict[values.tag] = values.text
            response_dict[in_param].append(item_dict)
        return response_dict

    response_dict = parse_items_in('delivery_sms')
    response_dict.update(parse_items_in('delivery_report'))
    return response_dict


class SmsConnect(object):
    def __init__(self, login=settings.SMS_CONNECT_LOGIN, password=settings.SMS_CONNECT_PASSWORD, secure=SECURE):
        self.login = login
        self.password = password
        self.secure = secure

    def _auth_url_part(self, time=None, sul=None):
        values = {'login': self.login}
        if self.secure:
            values = dict(values, time=(time or datetime.now()).strftime(DATETIME_FORMAT), sul=sul or uuid.uuid4().hex)
            values['auth'] = hashlib.md5('%s%s%s' % (self.password, values['time'], values['sul'])).hexdigest()
        else:
            values = dict(values, password=self.password)

        return urllib.urlencode(values)

    def _construct_url(self, name, **kwargs):
        if debug:
            print 'construct url kwargs', kwargs
        values = {'action': name}
        for k, v in kwargs.items():
            if v:
                values[k] = smart_str(force_unicode(v))

        url = u'%s?%s&%s' % (const.API_ACCES_POINT, self._auth_url_part(), urllib.urlencode(values))
        if debug:
            print 'construct url kwargs', url
        return url

    def _call_api(self, action, params={}, parse_function=parse_simple_response_xml_to_dict, check_err=True,
                  attempts=5):
        for i in range(1, attempts): #if salt is used twice, make another few attempts #TODO ugly
            url = self._construct_url(action, **params)
            response = requests.get(url)

            if response.status_code != requests.codes.ok:
                raise SmsConnectException('wrong status code returned %s' % response.status_code)
            result = parse_function(response.text)
            #        print result

            if check_err and result['err'] != '0':
                if result['err'] == '7' and i < attempts - 1: #if salt is used twice, do it again
                #                    logger.warning('%s , attempt %s' % (const.ERROR_CODES[result['err']], i))
                    continue
                raise SmsConnectException('Error %s - %s' % (result['err'], const.ERROR_CODES[result['err']]))
            return result

    def send_sms(self, number, message, when=None, delivery_report=1, sender_id=SENDER_ID):
        result = self._call_api('send_sms',
            params=dict(number=number, message=message, when=when, delivery_report=delivery_report,
                sender_id=sender_id))
        signals.smsconnect_sms_sent.send(sender=self, phone_number=number, text=message) #TODO document this
        return result

    def inbox(self, delete=None):
        """
        Returns dict with keys 'delivery_sms' and 'delivery_report' which contains lists of items dicts.
        """
        result = self._call_api('inbox', params=dict(delete=delete), check_err=False,
            parse_function=parse_inbox_xml_to_dict)
        return result

    def credit_info(self):
        result = self._call_api('credit_info')
        return result['credit']
