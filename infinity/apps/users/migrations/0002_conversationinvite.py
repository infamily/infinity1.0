# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=255)),
                ('redirect_url', models.URLField()),
                ('expired', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
