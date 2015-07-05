# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20150624_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paypaltransaction',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
