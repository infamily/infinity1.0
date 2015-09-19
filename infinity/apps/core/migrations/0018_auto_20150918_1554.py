# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_plan_plan_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='plan_members',
            new_name='members',
        ),
    ]
