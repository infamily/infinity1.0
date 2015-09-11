# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150829_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='commented_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 3, 12, 57, 52, 201940, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='idea',
            name='commented_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 3, 12, 57, 55, 994162, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='need',
            name='commented_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 3, 12, 57, 59, 225938, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='commented_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 3, 12, 58, 1, 945936, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='step',
            name='commented_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 3, 12, 58, 5, 450120, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='commented_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 3, 12, 58, 7, 946255, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='work',
            name='commented_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 3, 12, 58, 10, 122203, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
