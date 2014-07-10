# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Item.notes_short'
        db.delete_column(u'catalog_item', 'notes_short')

        # Deleting field 'Item.label'
        db.delete_column(u'catalog_item', 'label_id')

        # Adding field 'Item.description'
        db.add_column(u'catalog_item', 'description',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Item.rarity_date'
        db.add_column(u'catalog_item', 'rarity_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.discogs'
        db.add_column(u'catalog_item', 'discogs',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.is_promo'
        db.add_column(u'catalog_item', 'is_promo',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Item.is_authorized'
        db.add_column(u'catalog_item', 'is_authorized',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding M2M table for field music_labels on 'Item'
        m2m_table_name = db.shorten_name(u'catalog_item_music_labels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'catalog.item'], null=False)),
            ('musiclabel', models.ForeignKey(orm[u'catalog.musiclabel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'musiclabel_id'])


        # Changing field 'Item.added_date'
        db.alter_column(u'catalog_item', 'added_date', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Item.notes_short'
        raise RuntimeError("Cannot reverse this migration. 'Item.notes_short' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.notes_short'
        db.add_column(u'catalog_item', 'notes_short',
                      self.gf('django.db.models.fields.CharField')(max_length=200),
                      keep_default=False)

        # Adding field 'Item.label'
        db.add_column(u'catalog_item', 'label',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.MusicLabel'], null=True),
                      keep_default=False)

        # Deleting field 'Item.description'
        db.delete_column(u'catalog_item', 'description')

        # Deleting field 'Item.rarity_date'
        db.delete_column(u'catalog_item', 'rarity_date')

        # Deleting field 'Item.discogs'
        db.delete_column(u'catalog_item', 'discogs')

        # Deleting field 'Item.is_promo'
        db.delete_column(u'catalog_item', 'is_promo')

        # Deleting field 'Item.is_authorized'
        db.delete_column(u'catalog_item', 'is_authorized')

        # Removing M2M table for field music_labels on 'Item'
        db.delete_table(db.shorten_name(u'catalog_item_music_labels'))


        # User chose to not deal with backwards NULL issues for 'Item.added_date'
        raise RuntimeError("Cannot reverse this migration. 'Item.added_date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Item.added_date'
        db.alter_column(u'catalog_item', 'added_date', self.gf('django.db.models.fields.DateField')())

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
            'added_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Artist']"}),
            'catalog_number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Category']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'discogs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_authorized': ('django.db.models.fields.BooleanField', [], {}),
            'is_promo': ('django.db.models.fields.BooleanField', [], {}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Media']"}),
            'media_notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'music_labels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalog.MusicLabel']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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