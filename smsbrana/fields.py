# -*- coding: utf-8 -*-
import re

from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.encoding import smart_unicode
from django.forms.fields import CharField
from django.utils.translation import ugettext as _

class PhoneNumberField(CharField):
    description = _("Phone number")
    default_error_messages = {
        'invalid': _('Phone numbers must be in 777111222 or 777 111 222 or +420 777 111 222 or 00420777111222 format.'),
        }

    def __init__(self, allowed_international=None, *args, **kwargs):
        allowed_international = allowed_international or ('\+420','00420', '\+421', '00421')
        kwargs['max_length'] = 20
        kwargs['min_length'] = 9
        kwargs['label'] = kwargs.get('label',_(u'Phone number'))
        self.phone_re = re.compile(r'^(%s)?\s?(\d{3})\s?(\d{3})\s?(\d{3})$' % '|'.join(allowed_international))
        super(PhoneNumberField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(PhoneNumberField, self).clean(value)
        if value in validators.EMPTY_VALUES and not self.required:
            return

        value = re.sub('\s', '', smart_unicode(value))
        m = self.phone_re.search(value)
        if m:
            international = m.group(1) or '+420'
            international = '+%s' % international[2:] if international.startswith('00') else international
            return u'%s%s%s%s' % (international, m.group(2), m.group(3), m.group(4))
        raise ValidationError(self.error_messages['invalid'])

    def formfield(self, **kwargs):
        defaults = {'form_class': PhoneNumberField}
        defaults.update(kwargs)
        return super(PhoneNumberField, self).formfield(**defaults)

