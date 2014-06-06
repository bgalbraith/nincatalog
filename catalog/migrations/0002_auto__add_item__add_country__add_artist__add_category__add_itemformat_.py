# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'catalog_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Category'])),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Artist'])),
            ('format', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ItemFormat'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Country'])),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.MusicLabel'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('catalog_number', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('upc', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('packaging', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('release_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('added_date', self.gf('django.db.models.fields.DateField')()),
            ('rarity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'catalog', ['Item'])

        # Adding model 'Country'
        db.create_table(u'catalog_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'catalog', ['Country'])

        # Adding model 'Artist'
        db.create_table(u'catalog_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['Artist'])

        # Adding model 'Category'
        db.create_table(u'catalog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['Category'])

        # Adding model 'ItemFormat'
        db.create_table(u'catalog_itemformat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['ItemFormat'])

        # Adding model 'Track'
        db.create_table(u'catalog_track', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['Track'])

        # Adding M2M table for field related_tracks on 'Track'
        m2m_table_name = db.shorten_name(u'catalog_track_related_tracks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_track', models.ForeignKey(orm[u'catalog.track'], null=False)),
            ('to_track', models.ForeignKey(orm[u'catalog.track'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_track_id', 'to_track_id'])

        # Adding model 'MusicLabel'
        db.create_table(u'catalog_musiclabel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'catalog', ['MusicLabel'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table(u'catalog_item')

        # Deleting model 'Country'
        db.delete_table(u'catalog_country')

        # Deleting model 'Artist'
        db.delete_table(u'catalog_artist')

        # Deleting model 'Category'
        db.delete_table(u'catalog_category')

        # Deleting model 'ItemFormat'
        db.delete_table(u'catalog_itemformat')

        # Deleting model 'Track'
        db.delete_table(u'catalog_track')

        # Removing M2M table for field related_tracks on 'Track'
        db.delete_table(db.shorten_name(u'catalog_track_related_tracks'))

        # Deleting model 'MusicLabel'
        db.delete_table(u'catalog_musiclabel')


    models = {
        u'catalog.artist': {
            'Meta': {'object_name': 'Artist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'catalog.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
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
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ItemFormat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.MusicLabel']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'packaging': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rarity': ('django.db.models.fields.IntegerField', [], {}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'catalog.itemformat': {
            'Meta': {'object_name': 'ItemFormat'},
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