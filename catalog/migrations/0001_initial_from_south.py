# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('tag', models.CharField(max_length=200)),
                ('halo', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('icon', models.ImageField(upload_to=b'categories')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=2)),
                ('icon', models.ImageField(upload_to=b'countries')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Era',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('icon', models.ImageField(upload_to=b'eras')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('media_notes', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('rarity_date', models.DateField(null=True, blank=True)),
                ('notes', models.CharField(max_length=200)),
                ('catalog_number', models.CharField(max_length=200)),
                ('upc', models.CharField(max_length=200)),
                ('discogs', models.IntegerField(null=True, blank=True)),
                ('is_promo', models.BooleanField()),
                ('is_authorized', models.BooleanField()),
                ('release_date', models.DateField(null=True, blank=True)),
                ('added_date', models.DateField(null=True, blank=True)),
                ('old_key', models.CharField(max_length=8)),
                ('artist', models.ForeignKey(to='catalog.Artist')),
                ('category', models.ForeignKey(to='catalog.Category')),
                ('country', models.ForeignKey(to='catalog.Country')),
                ('era', models.ForeignKey(to='catalog.Era', null=True)),
            ],
            options={
                'ordering': ('year', 'name', 'media_format', 'country', 'catalog_number'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'item_images')),
                ('item', models.ForeignKey(to='catalog.Item')),
            ],
            options={
                'ordering': ('type',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemImageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemRarity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=1)),
                ('description', models.CharField(max_length=200)),
                ('icon', models.ImageField(upload_to=b'rarity')),
                ('scale_icon', models.ImageField(upload_to=b'rarity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MediaPackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MusicLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('icon', models.ImageField(null=True, upload_to=b'music_labels')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('tag', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=200)),
                ('field', models.CharField(max_length=200)),
                ('icon', models.ImageField(upload_to=b'reports')),
                ('n_columns', models.PositiveSmallIntegerField(default=3)),
                ('column_width', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('related_tracks', models.ManyToManyField(related_name='related_tracks_rel_+', to='catalog.Track')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='type',
            field=models.ForeignKey(to='catalog.ItemImageType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='media_format',
            field=models.ForeignKey(to='catalog.MediaFormat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='media_package',
            field=models.ForeignKey(to='catalog.MediaPackage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='music_labels',
            field=models.ManyToManyField(to='catalog.MusicLabel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='rarity',
            field=models.ForeignKey(to='catalog.ItemRarity'),
            preserve_default=True,
        ),
    ]
