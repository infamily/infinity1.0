# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0016_auto_20150917_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='plan_members',
            field=models.ManyToManyField(related_name='user_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
