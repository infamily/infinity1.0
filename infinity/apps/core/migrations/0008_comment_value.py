# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150903_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='value',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
    ]
