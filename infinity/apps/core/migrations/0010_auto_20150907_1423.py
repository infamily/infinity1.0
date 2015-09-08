# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150907_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='hours',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=5),
        ),
        migrations.AddField(
            model_name='goal',
            name='money',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='idea',
            name='hours',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=5),
        ),
        migrations.AddField(
            model_name='idea',
            name='money',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='need',
            name='hours',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=5),
        ),
        migrations.AddField(
            model_name='need',
            name='money',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='plan',
            name='hours',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=5),
        ),
        migrations.AddField(
            model_name='plan',
            name='money',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='step',
            name='hours',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=5),
        ),
        migrations.AddField(
            model_name='step',
            name='money',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='task',
            name='hours',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=5),
        ),
        migrations.AddField(
            model_name='task',
            name='money',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='work',
            name='hours',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=5),
        ),
        migrations.AddField(
            model_name='work',
            name='money',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
    ]
