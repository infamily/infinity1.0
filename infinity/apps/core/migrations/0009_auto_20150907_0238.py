# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_comment_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='value',
            new_name='money',
        ),
        migrations.AddField(
            model_name='comment',
            name='hours',
            field=models.DecimalField(default=0.0, max_digits=20, decimal_places=5),
        ),
    ]
