# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('core', '0002_auto_20150608_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='goal',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='idea',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='step',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='task',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='work',
        ),
        migrations.AddField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
