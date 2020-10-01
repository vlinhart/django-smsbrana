# About django-smsbrana

This code incompletely  implements api from [smsbrana connect api](http://www.smsbrana.cz/sms-connect.html) 

You can call three commands :

* send_sms - sends sms
* inbox - shows status of your inbox (your sms on server) and sms delivery reports
* credit_info - how much credit you have left

It also provides notification callback view function. Which will be called upon arrival of new message into your inbox.

## Installation
    pip install git+git://github.com/vlinhart/django-smsbrana.git#egg=smsbrana
    add 'smsbrana' to the INSTALLED_APPS.
    add url(r'^smsbrana/', include('smsbrana.urls', namespace="smsbrana")) to urls.py

## Configuration
It's necessary to set several constants in settings.py:

    SMS_CONNECT_LOGIN = username
    SMS_CONNECT_PASSWORD = passsword

    optional is:
    SMS_CONNECT_SECURE = True #if you want to use plaintext password sending, don't
    SMS_CONNECT_SENDER_ID = 'some sender id' #from smsbrana configuration

## Usage
Have a look at the tests to see how the class SmsConnect is used. Basically like this:

    sc = SmsConnect()
    result = sc.send_sms(number='777111222', message='msg') #there are more optional params
    #in result is a dict containing this keys - 'err','price','sms_count','credit','sms_id'

All API calls can raise SmsConnectException, you should handle it. 


### Signals
There are two signals provided. 

* smsconnect_notification_received -- caled when view notification function is called, providing request and result of inbox API call
* smsconnect_sms_sent -- called when SMS is sent, provides phone_number, text and result of the API call

### View function
smsconnect_notification will handle notification calls from smsbrana.cz which will be issued upon new message arrival or sms delivery. It will fire the *smsconnect_notification_received* signal. This function is updating state of SentSms model instances, setting their flags, *delivered* and *delivered_date*.

### Model SentSms
You can use this model to track sent SMSes. Some helpful methods on the model are also provided. 

* generate_sms_verification_code(length=6) -- if you want to use model for sending verification codes
* can_send_from_ip(ip, time_allowance=30) -- checks if there were smses sent from IP address in *time_allowance* seconds ago
* sms_to_number_delivered_in_last_hours(hours, phone_number) -- if to specified phone number SMS was delivered *hours* ago up to now


This is not exhaustive documentation, read the code. 

