# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial_from_south'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='is_authorized',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='is_promo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
