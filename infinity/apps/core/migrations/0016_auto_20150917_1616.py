# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150911_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='hyper_equity',
            field=models.DecimalField(default=0.0001, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='idea',
            name='super_equity',
            field=models.DecimalField(default=0.01, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='plan',
            name='plain_equity',
            field=models.DecimalField(default=0.1, max_digits=20, decimal_places=8),
        ),
    ]
