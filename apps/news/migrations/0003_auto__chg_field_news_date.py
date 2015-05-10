# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'News.date'
        db.alter_column(u'news_news', 'date', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # Changing field 'News.date'
        db.alter_column(u'news_news', 'date', self.gf('django.db.models.fields.DateTimeField')(null=True))

    models = {
        u'news.news': {
            'Meta': {'object_name': 'News'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 10, 14, 0, 0)', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'meta_desc': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['news']