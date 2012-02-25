# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.dispatch.dispatcher import receiver
from django.test.testcases import TestCase
import smsbrana
from smsbrana import SmsConnect, SmsConnectException, parse_inbox_xml_to_dict
from smsbrana import signals
from smsbrana.fields import CZPhoneNumberField
from smsbrana.models import SentSms

PASSW = 'test'
LOGIN = 'test'

INBOX_XML = """<result>
 <inbox>
  <delivery_sms>
   <item>
    <number>+420774884136</number>
    <time>20091020T164508</time>
    <message>test</message>
   </item>
  </delivery_sms>
  <delivery_report>
   <item>
    <idsms>377339</idsms>
    <number>+420774884136</number>
    <time>20091020T132528</time>
    <status>1</status>
   </item>
   <item>
    <idsms>377340</idsms>
    <number>+420774884136</number>
    <time>20091020T181102</time>
    <status>1</status>
   </item>
  </delivery_report>
 </inbox>
</result>
"""

smsbrana.debug = True


class TestSmsConnect(TestCase):
    def test_auth(self):
        sc = SmsConnect(login=LOGIN, password=PASSW, secure=False)
        self.assertEqual(sc._auth_url_part(), 'login=test&password=test')

        sc = SmsConnect(login=LOGIN, password=PASSW, secure=True)
        self.assertEqual(
            sc._auth_url_part(time=datetime.datetime(2012, 2, 23, 11, 13, 13), sul='73952a8e84f14b4caaf1e38f81f14e0a'),
            'login=test&sul=73952a8e84f14b4caaf1e38f81f14e0a&auth=34204a8d27474431b585e3dff75db101&time=20120223T111313')

    def test_credit_info(self):
        sc = SmsConnect(login=settings.SMS_CONNECT_LOGIN, password=PASSW, secure=True)
        self.assertRaises(SmsConnectException, sc.credit_info) #wrong passwd

        sc = SmsConnect(login=settings.SMS_CONNECT_LOGIN, password=settings.SMS_CONNECT_PASSWORD, secure=True)
        self.assertTrue(sc.credit_info()) #check that we have somethin

    def dtest_inbox(self):
        sc = SmsConnect(login=settings.SMS_CONNECT_LOGIN, password=settings.SMS_CONNECT_PASSWORD, secure=True)
        print sc.inbox()


    def dtest_send_sms(self):
        sc = SmsConnect(login=settings.SMS_CONNECT_LOGIN, password=settings.SMS_CONNECT_PASSWORD, secure=True)
        self.assertRaises(SmsConnectException, sc.send_sms, 'neplatne cislo', 'test message')

    def test_inbox_xml_parsing(self):
        result = parse_inbox_xml_to_dict(INBOX_XML)
        self.assertEqual(result['delivery_report'][0]['number'], '+420774884136')
        self.assertEqual(result['delivery_sms'][0]['number'], '+420774884136')


    def test_notification_signal(self):
        @receiver(signals.smsconnect_notification_received)
        def handle_signal(sender, **kwargs):
            self.assertEqual(kwargs['inbox'], 'hello result')

        signals.smsconnect_notification_received.send(sender=None, inbox="hello result", request='request')

    def test_cz_phone_field(self):
        good_test_cases = ['777111222', '777 111 222', '777  111 222', '+420777111222', '+420 777111222',
                           ' +420 777 111 222  ', '+420777   111 222', '00420777111222', '00420 777 111 222']
        bad_test_cases = ['a 777111222  ', '4777 111 222', '777 a 111 222', '420777111222', '+421 777111222',
                          '420 777 111 222', '0+420777   111 222', '000420777111222', '+00420 777 111 222']
        field = CZPhoneNumberField()
        for test_case in good_test_cases:
            self.assertEqual(field.clean(test_case), '+420777111222')

        for test_case in bad_test_cases:
            self.assertRaises(ValidationError, field.clean, test_case)

    def test_ip_time_allowance(self):
        object = SentSms.objects.create(sms_id=10, phone_number='777777777', message='msg', verification_code='c',
            ip_address='1.1.1.1')
        self.assertFalse(SentSms.can_send_from_ip('1.1.1.1'))
        self.assertTrue(SentSms.can_send_from_ip('1.1.1.2'))
        object.sent_date = datetime.datetime.now() - datetime.timedelta(seconds=30)
        object.save()
        self.assertTrue(SentSms.can_send_from_ip('1.1.1.1', time_allowance=30))
