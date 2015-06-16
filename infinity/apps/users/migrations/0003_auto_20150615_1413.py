# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150615_0559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='introduction',
            new_name='about',
        ),
    ]
