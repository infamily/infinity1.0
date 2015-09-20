# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20150919_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='total_assumed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='work',
            name='total_claimed',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='work',
            name='total_donated',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AddField(
            model_name='work',
            name='total_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
    ]
