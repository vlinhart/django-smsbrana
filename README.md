# About django-smsbrana

This code incompletely  implements api from [smsbrana connect api](http://www.smsbrana.cz/sms-connect.html) 

You can call three commands :

* send_sms - sends sms
* inbox - shows status of your inbox (your sms on server)
* credit_info - how much credit you have left

It also provides notification callback view function. Which will be called upon arrival of new message into your inbox.

##Installation
    pip install git+git://github.com/vlinhart/django-smsbrana.git#egg=smsbrana
    add 'smsbrana' to the INSTALLED_APPS.
    add url(r'^smsbrana/', include('smsbrana.urls', namespace="smsbrana")) to urls.py

##Configuration
It's necessary to set several constants in settings.py:

    SMS_CONNECT_LOGIN = username
    SMS_CONNECT_PASSWORD = passsword

    optional is:
    SMS_CONNECT_SECURE = True #if you want to use plaintext password sending, don't
    SMS_CONNECT_SENDER_ID = 'some sender id' #from smsbrana configuration

