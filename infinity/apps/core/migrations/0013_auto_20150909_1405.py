# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150909_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='goal',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='idea',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='need',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='plan',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='step',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='task',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='work',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
    ]
