# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20150908_0734'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypaltransaction',
            name='hours_matched',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=8),
        ),
        migrations.AlterField(
            model_name='paypaltransaction',
            name='hours',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=8),
        ),
    ]
