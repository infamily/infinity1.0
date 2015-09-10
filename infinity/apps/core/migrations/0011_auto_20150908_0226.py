# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150907_1423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='hours',
            new_name='hours_claimed',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='money',
            new_name='hours_donated',
        ),
        migrations.RenameField(
            model_name='goal',
            old_name='hours',
            new_name='hours_claimed',
        ),
        migrations.RenameField(
            model_name='goal',
            old_name='money',
            new_name='hours_donated',
        ),
        migrations.RenameField(
            model_name='idea',
            old_name='hours',
            new_name='hours_claimed',
        ),
        migrations.RenameField(
            model_name='idea',
            old_name='money',
            new_name='hours_donated',
        ),
        migrations.RenameField(
            model_name='need',
            old_name='hours',
            new_name='hours_claimed',
        ),
        migrations.RenameField(
            model_name='need',
            old_name='money',
            new_name='hours_donated',
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='hours',
            new_name='hours_claimed',
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='money',
            new_name='hours_donated',
        ),
        migrations.RenameField(
            model_name='step',
            old_name='hours',
            new_name='hours_claimed',
        ),
        migrations.RenameField(
            model_name='step',
            old_name='money',
            new_name='hours_donated',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='hours',
            new_name='hours_claimed',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='money',
            new_name='hours_donated',
        ),
        migrations.RenameField(
            model_name='work',
            old_name='hours',
            new_name='hours_claimed',
        ),
        migrations.RenameField(
            model_name='work',
            old_name='money',
            new_name='hours_donated',
        ),
    ]
