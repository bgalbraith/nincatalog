# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20150120_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaformat',
            name='tag',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
    ]
