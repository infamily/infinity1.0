# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_comment_notify'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='unit',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='personal',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='idea',
            name='personal',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='plan',
            name='personal',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='step',
            name='personal',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='personal',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='work',
            name='personal',
            field=models.BooleanField(default=False),
        ),
    ]
