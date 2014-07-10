# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PackageType'
        db.delete_table(u'catalog_packagetype')

        # Deleting model 'MediaFormat'
        db.delete_table(u'catalog_mediaformat')

        # Adding model 'Media'
        db.create_table(u'catalog_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['Media'])

        # Deleting field 'Item.package_type'
        db.delete_column(u'catalog_item', 'package_type_id')

        # Deleting field 'Item.format'
        db.delete_column(u'catalog_item', 'format_id')

        # Deleting field 'Item.package_notes'
        db.delete_column(u'catalog_item', 'package_notes')

        # Adding field 'Item.media'
        db.add_column(u'catalog_item', 'media',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['catalog.Media']),
                      keep_default=False)

        # Adding field 'Item.media_notes'
        db.add_column(u'catalog_item', 'media_notes',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'PackageType'
        db.create_table(u'catalog_packagetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['PackageType'])

        # Adding model 'MediaFormat'
        db.create_table(u'catalog_mediaformat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['MediaFormat'])

        # Deleting model 'Media'
        db.delete_table(u'catalog_media')


        # User chose to not deal with backwards NULL issues for 'Item.package_type'
        raise RuntimeError("Cannot reverse this migration. 'Item.package_type' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.package_type'
        db.add_column(u'catalog_item', 'package_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.PackageType']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Item.format'
        raise RuntimeError("Cannot reverse this migration. 'Item.format' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.format'
        db.add_column(u'catalog_item', 'format',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.MediaFormat']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Item.package_notes'
        raise RuntimeError("Cannot reverse this migration. 'Item.package_notes' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.package_notes'
        db.add_column(u'catalog_item', 'package_notes',
                      self.gf('django.db.models.fields.CharField')(max_length=200),
                      keep_default=False)

        # Deleting field 'Item.media'
        db.delete_column(u'catalog_item', 'media_id')

        # Deleting field 'Item.media_notes'
        db.delete_column(u'catalog_item', 'media_notes')


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
        u'catalog.item': {
            'Meta': {'object_name': 'Item'},
            'added_date': ('django.db.models.fields.DateField', [], {}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Artist']"}),
            'catalog_number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Category']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.MusicLabel']", 'null': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Media']"}),
            'media_notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes_short': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rarity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ItemRarity']"}),
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
        u'catalog.media': {
            'Meta': {'object_name': 'Media'},
            'format': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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