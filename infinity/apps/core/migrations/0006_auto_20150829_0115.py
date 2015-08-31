# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150824_2259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='goal',
            name='unit',
        ),
        migrations.AddField(
            model_name='goal',
            name='type',
            field=models.ForeignKey(default=1, to='core.Type'),
            preserve_default=False,
        ),
    ]
