# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-30 01:45
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_populate_item_image_order(apps, schema_editor):
    Item = apps.get_model("catalog", "Item")
    db_alias = schema_editor.connection.alias
    for item in Item.objects.using(db_alias):
        i = 1
        for image_type in ('Front', 'Back', 'Details', 'Media'):
            for image in item.itemimage_set.filter(type__name=image_type):
                image.order = i
                image.save()
                i += 1


def reverse_populate_item_image_order(apps, schema_editor):
    ItemImage = apps.get_model("catalog", "ItemImage")
    db_alias = schema_editor.connection.alias
    ItemImage.objects.using(db_alias).update(order=0)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_mediaformat_tag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',), 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='itemimage',
            options={'ordering': ('order',), 'verbose_name_plural': 'Item Images'},
        ),
        migrations.AlterModelOptions(
            name='itemimagetype',
            options={'ordering': ('name',), 'verbose_name_plural': 'Item Image Types'},
        ),
        migrations.AlterModelOptions(
            name='itemrarity',
            options={'ordering': ('id',), 'verbose_name_plural': 'Item Rarities'},
        ),
        migrations.AlterModelOptions(
            name='mediaformat',
            options={'ordering': ('name',), 'verbose_name_plural': 'Media Formats'},
        ),
        migrations.AlterModelOptions(
            name='mediapackage',
            options={'ordering': ('name',), 'verbose_name_plural': 'Media Packages'},
        ),
        migrations.AlterModelOptions(
            name='musiclabel',
            options={'ordering': ('name',), 'verbose_name_plural': 'Music Labels'},
        ),
        migrations.AddField(
            model_name='itemimage',
            name='order',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.RunPython(forwards_populate_item_image_order,
                             reverse_populate_item_image_order),
    ]
