# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-02 16:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20151206_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='sharewith',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]