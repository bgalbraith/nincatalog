# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemImageType'
        db.create_table(u'catalog_itemimagetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['ItemImageType'])

        # Adding model 'ItemImage'
        db.create_table(u'catalog_itemimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Item'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ItemImageType'])),
        ))
        db.send_create_signal(u'catalog', ['ItemImage'])


    def backwards(self, orm):
        # Deleting model 'ItemImageType'
        db.delete_table(u'catalog_itemimagetype')

        # Deleting model 'ItemImage'
        db.delete_table(u'catalog_itemimage')


    models = {
        u'catalog.artist': {
            'Meta': {'object_name': 'Artist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.category': {
            'Meta': {'object_name': 'Category'},
            'halo': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.era': {
            'Meta': {'object_name': 'Era'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.item': {
            'Meta': {'ordering': "('year', 'name', 'media_format', 'country', 'catalog_number')", 'object_name': 'Item'},
            'added_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Artist']"}),
            'catalog_number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Category']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'discogs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'era': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Era']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authorized': ('django.db.models.fields.BooleanField', [], {}),
            'is_promo': ('django.db.models.fields.BooleanField', [], {}),
            'media_format': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.MediaFormat']"}),
            'media_notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'media_package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.MediaPackage']"}),
            'music_labels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalog.MusicLabel']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'old_key': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'rarity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ItemRarity']"}),
            'rarity_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'catalog.itemimage': {
            'Meta': {'object_name': 'ItemImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Item']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ItemImageType']"})
        },
        u'catalog.itemimagetype': {
            'Meta': {'object_name': 'ItemImageType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.itemrarity': {
            'Meta': {'object_name': 'ItemRarity'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scale_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'catalog.mediaformat': {
            'Meta': {'object_name': 'MediaFormat'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.mediapackage': {
            'Meta': {'object_name': 'MediaPackage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.musiclabel': {
            'Meta': {'object_name': 'MusicLabel'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'catalog.track': {
            'Meta': {'object_name': 'Track'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'related_tracks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_tracks_rel_+'", 'to': u"orm['catalog.Track']"})
        }
    }

    complete_apps = ['catalog']