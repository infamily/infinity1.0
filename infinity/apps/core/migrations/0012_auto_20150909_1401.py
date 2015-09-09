# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150908_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='hours_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='goal',
            name='hours_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='idea',
            name='hours_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='need',
            name='hours_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='plan',
            name='hours_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='step',
            name='hours_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='task',
            name='hours_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='work',
            name='hours_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
    ]
