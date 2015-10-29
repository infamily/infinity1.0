# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151021_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='user',
            field=models.ForeignKey(related_name='user_goal', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='idea',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='user',
            field=models.ForeignKey(related_name='user_idea', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='plan',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='user',
            field=models.ForeignKey(related_name='user_plan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='step',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='step',
            name='user',
            field=models.ForeignKey(related_name='user_step', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(related_name='user_task', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='work',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='user',
            field=models.ForeignKey(related_name='user_work', to=settings.AUTH_USER_MODEL),
        ),
    ]
