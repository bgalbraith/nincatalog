# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Media'
        db.delete_table(u'catalog_media')

        # Adding model 'MediaFormat'
        db.create_table(u'catalog_mediaformat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['MediaFormat'])

        # Adding model 'MediaPackage'
        db.create_table(u'catalog_mediapackage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['MediaPackage'])

        # Deleting field 'Item.media'
        db.delete_column(u'catalog_item', 'media_id')

        # Adding field 'Item.media_format'
        db.add_column(u'catalog_item', 'media_format',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['catalog.MediaFormat']),
                      keep_default=False)

        # Adding field 'Item.media_package'
        db.add_column(u'catalog_item', 'media_package',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['catalog.MediaPackage']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Media'
        db.create_table(u'catalog_media', (
            ('package', self.gf('django.db.models.fields.CharField')(max_length=200)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['Media'])

        # Deleting model 'MediaFormat'
        db.delete_table(u'catalog_mediaformat')

        # Deleting model 'MediaPackage'
        db.delete_table(u'catalog_mediapackage')


        # User chose to not deal with backwards NULL issues for 'Item.media'
        raise RuntimeError("Cannot reverse this migration. 'Item.media' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.media'
        db.add_column(u'catalog_item', 'media',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Media']),
                      keep_default=False)

        # Deleting field 'Item.media_format'
        db.delete_column(u'catalog_item', 'media_format_id')

        # Deleting field 'Item.media_package'
        db.delete_column(u'catalog_item', 'media_package_id')


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
            'Meta': {'object_name': 'Item'},
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
        u'catalog.itemrarity': {
            'Meta': {'object_name': 'ItemRarity'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
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