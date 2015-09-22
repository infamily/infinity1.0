# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150920_0113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='goal',
        ),
        migrations.AddField(
            model_name='idea',
            name='goal',
            field=models.ManyToManyField(related_name='goal_ideas', to='core.Goal'),
        ),
    ]
