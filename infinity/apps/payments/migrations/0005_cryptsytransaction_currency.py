# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20150610_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptsytransaction',
            name='currency',
            field=models.CharField(default=1, max_length=6),
            preserve_default=False,
        ),
    ]
