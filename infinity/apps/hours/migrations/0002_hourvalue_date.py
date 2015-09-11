# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hourvalue',
            name='date',
            field=models.CharField(default='2015-09-09', max_length=15),
            preserve_default=False,
        ),
    ]
