# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table(u'news_news', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 10, 13, 0, 0), null=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('meta_desc', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal(u'news', ['News'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table(u'news_news')


    models = {
        u'news.news': {
            'Meta': {'object_name': 'News'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 13, 0, 0)', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_desc': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['news']