# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SentSms'
        db.create_table('smsbrana_sentsms', (
            ('sms_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('verification_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('sent_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('delivered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delivered_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('smsbrana', ['SentSms'])


    def backwards(self, orm):
        # Deleting model 'SentSms'
        db.delete_table('smsbrana_sentsms')


    models = {
        'smsbrana.sentsms': {
            'Meta': {'object_name': 'SentSms'},
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delivered_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sent_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'sms_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'verification_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['smsbrana']