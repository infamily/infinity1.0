# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_need'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='content',
            field=models.TextField(null=True, blank=True),
        ),
    ]
