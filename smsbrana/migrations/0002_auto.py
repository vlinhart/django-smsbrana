# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'SentSms', fields ['phone_number']
        db.create_index('smsbrana_sentsms', ['phone_number'])

        # Adding index on 'SentSms', fields ['delivered']
        db.create_index('smsbrana_sentsms', ['delivered'])

        # Adding index on 'SentSms', fields ['sent_date']
        db.create_index('smsbrana_sentsms', ['sent_date'])

        # Adding index on 'SentSms', fields ['ip_address']
        db.create_index('smsbrana_sentsms', ['ip_address'])


    def backwards(self, orm):
        # Removing index on 'SentSms', fields ['ip_address']
        db.delete_index('smsbrana_sentsms', ['ip_address'])

        # Removing index on 'SentSms', fields ['sent_date']
        db.delete_index('smsbrana_sentsms', ['sent_date'])

        # Removing index on 'SentSms', fields ['delivered']
        db.delete_index('smsbrana_sentsms', ['delivered'])

        # Removing index on 'SentSms', fields ['phone_number']
        db.delete_index('smsbrana_sentsms', ['phone_number'])


    models = {
        'smsbrana.sentsms': {
            'Meta': {'object_name': 'SentSms'},
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'delivered_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'sent_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'}),
            'sms_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'verification_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['smsbrana']