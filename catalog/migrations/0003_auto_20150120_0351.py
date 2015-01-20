# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20150117_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='old_key',
            field=models.CharField(max_length=8, null=True, blank=True),
            preserve_default=True,
        ),
    ]
