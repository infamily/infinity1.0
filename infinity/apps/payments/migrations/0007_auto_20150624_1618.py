# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_cryptsycredential_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptsycredential',
            name='user',
            field=models.ForeignKey(related_name=b'credential', to=settings.AUTH_USER_MODEL),
        ),
    ]
