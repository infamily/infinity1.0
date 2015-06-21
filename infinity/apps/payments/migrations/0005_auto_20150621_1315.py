# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20150621_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptsycredential',
            name='user',
            field=models.ForeignKey(related_name=b'credential', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
