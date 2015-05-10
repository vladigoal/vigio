# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collection'
        db.create_table(u'product_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'product', ['Collection'])

        # Adding model 'Category'
        db.create_table(u'product_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'children', null=True, to=orm['product.Category'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'product', ['Category'])

        # Adding model 'Size'
        db.create_table(u'product_size', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'product', ['Size'])

        # Adding M2M table for field category on 'Size'
        m2m_table_name = db.shorten_name(u'product_size_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('size', models.ForeignKey(orm[u'product.size'], null=False)),
            ('category', models.ForeignKey(orm[u'product.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['size_id', 'category_id'])

        # Adding model 'Color'
        db.create_table(u'product_color', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'product', ['Color'])

        # Adding model 'Care'
        db.create_table(u'product_care', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Care'])

        # Adding M2M table for field category on 'Care'
        m2m_table_name = db.shorten_name(u'product_care_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('care', models.ForeignKey(orm[u'product.care'], null=False)),
            ('category', models.ForeignKey(orm[u'product.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['care_id', 'category_id'])

        # Adding model 'Status'
        db.create_table(u'product_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'product', ['Status'])

        # Adding model 'Product'
        db.create_table(u'product_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Collection'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Status'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['product.Category'], null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fabric', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('price', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'product', ['Product'])

        # Adding M2M table for field parent on 'Product'
        m2m_table_name = db.shorten_name(u'product_product_parent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_product', models.ForeignKey(orm[u'product.product'], null=False)),
            ('to_product', models.ForeignKey(orm[u'product.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_product_id', 'to_product_id'])

        # Adding M2M table for field care on 'Product'
        m2m_table_name = db.shorten_name(u'product_product_care')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'product.product'], null=False)),
            ('care', models.ForeignKey(orm[u'product.care'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'care_id'])

        # Adding M2M table for field size on 'Product'
        m2m_table_name = db.shorten_name(u'product_product_size')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'product.product'], null=False)),
            ('size', models.ForeignKey(orm[u'product.size'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'size_id'])

        # Adding model 'ProductImage'
        db.create_table(u'product_productimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'images', to=orm['product.Product'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Color'], null=True, blank=True)),
            ('catalog', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'product', ['ProductImage'])

        # Adding model 'Lookbook'
        db.create_table(u'product_lookbook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'product', ['Lookbook'])

        # Adding model 'LookbookImage'
        db.create_table(u'product_lookbookimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lookbook', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'Lookbook', to=orm['product.Lookbook'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'product', ['LookbookImage'])

        # Adding M2M table for field product on 'LookbookImage'
        m2m_table_name = db.shorten_name(u'product_lookbookimage_product')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lookbookimage', models.ForeignKey(orm[u'product.lookbookimage'], null=False)),
            ('product', models.ForeignKey(orm[u'product.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['lookbookimage_id', 'product_id'])


    def backwards(self, orm):
        # Deleting model 'Collection'
        db.delete_table(u'product_collection')

        # Deleting model 'Category'
        db.delete_table(u'product_category')

        # Deleting model 'Size'
        db.delete_table(u'product_size')

        # Removing M2M table for field category on 'Size'
        db.delete_table(db.shorten_name(u'product_size_category'))

        # Deleting model 'Color'
        db.delete_table(u'product_color')

        # Deleting model 'Care'
        db.delete_table(u'product_care')

        # Removing M2M table for field category on 'Care'
        db.delete_table(db.shorten_name(u'product_care_category'))

        # Deleting model 'Status'
        db.delete_table(u'product_status')

        # Deleting model 'Product'
        db.delete_table(u'product_product')

        # Removing M2M table for field parent on 'Product'
        db.delete_table(db.shorten_name(u'product_product_parent'))

        # Removing M2M table for field care on 'Product'
        db.delete_table(db.shorten_name(u'product_product_care'))

        # Removing M2M table for field size on 'Product'
        db.delete_table(db.shorten_name(u'product_product_size'))

        # Deleting model 'ProductImage'
        db.delete_table(u'product_productimage')

        # Deleting model 'Lookbook'
        db.delete_table(u'product_lookbook')

        # Deleting model 'LookbookImage'
        db.delete_table(u'product_lookbookimage')

        # Removing M2M table for field product on 'LookbookImage'
        db.delete_table(db.shorten_name(u'product_lookbookimage_product'))


    models = {
        u'product.care': {
            'Meta': {'object_name': 'Care'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.Category']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'product.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['product.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'product.collection': {
            'Meta': {'object_name': 'Collection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'product.color': {
            'Meta': {'object_name': 'Color'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'product.lookbook': {
            'Meta': {'object_name': 'Lookbook'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'product.lookbookimage': {
            'Meta': {'object_name': 'LookbookImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'lookbook': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'Lookbook'", 'to': u"orm['product.Lookbook']"}),
            'product': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['product.Product']", 'null': 'True', 'blank': 'True'})
        },
        u'product.product': {
            'Meta': {'object_name': 'Product'},
            'care': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['product.Care']", 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['product.Category']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Collection']"}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fabric': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parent_rel_+'", 'null': 'True', 'to': u"orm['product.Product']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'size': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['product.Size']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Status']"})
        },
        u'product.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'catalog': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Color']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'images'", 'to': u"orm['product.Product']"})
        },
        u'product.size': {
            'Meta': {'object_name': 'Size'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.Category']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'product.status': {
            'Meta': {'object_name': 'Status'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['product']