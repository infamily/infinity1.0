# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150710_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='notify',
            field=models.BooleanField(default=True),
        ),
    ]
