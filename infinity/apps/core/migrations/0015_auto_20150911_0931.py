# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='hours_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='goal',
            name='hours_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='idea',
            name='hours_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='need',
            name='hours_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='plan',
            name='hours_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='step',
            name='hours_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='task',
            name='hours_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='work',
            name='hours_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
    ]
