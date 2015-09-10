# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_paypaltransaction_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paypaltransaction',
            name='hours',
            field=models.DecimalField(default=0, max_digits=16, decimal_places=2),
        ),
    ]
