# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20150918_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='total_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='goal',
            name='total_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='goal',
            name='total_donated',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='goal',
            name='total_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='idea',
            name='total_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='idea',
            name='total_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='idea',
            name='total_donated',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='idea',
            name='total_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='need',
            name='total_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='need',
            name='total_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='need',
            name='total_donated',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='need',
            name='total_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='plan',
            name='total_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='plan',
            name='total_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='plan',
            name='total_donated',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='plan',
            name='total_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='step',
            name='total_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='step',
            name='total_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='step',
            name='total_donated',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='step',
            name='total_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='task',
            name='total_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='task',
            name='total_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='task',
            name='total_donated',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='task',
            name='total_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
    ]
