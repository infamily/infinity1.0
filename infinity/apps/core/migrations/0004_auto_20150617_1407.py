# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150615_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='personal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plan',
            name='personal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='step',
            name='personal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='personal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='work',
            name='personal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
