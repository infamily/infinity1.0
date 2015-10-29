# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151029_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
