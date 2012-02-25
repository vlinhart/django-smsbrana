# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_unicode
import re
from django.forms.fields import CharField
from django.utils.translation import ugettext as _

cz_phone_re = re.compile(r'^(\+420|00420)?\s?(\d{3})\s?(\d{3})\s?(\d{3})$')

class CZPhoneNumberField(CharField):
    description = _("CZ Phone number")
    default_error_messages = {
        'invalid': _('Phone numbers must be in 777111222 or 777 111 222 or +420 777 111 222 or 00420777111222 format.'),
        }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        kwargs['min_length'] = 9
        kwargs['label'] = kwargs.get('label',_(u'Phone number'))
        super(CZPhoneNumberField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(CZPhoneNumberField, self).clean(value)

        value = re.sub('\s', '', smart_unicode(value))
        m = cz_phone_re.search(value)
        if m:
            return u'+420%s%s%s' % (m.group(2), m.group(3), m.group(4))
        raise ValidationError(self.error_messages['invalid'])

    def formfield(self, **kwargs):
        defaults = {'form_class': CZPhoneNumberField}
        defaults.update(kwargs)
        return super(CZPhoneNumberField, self).formfield(**defaults)
