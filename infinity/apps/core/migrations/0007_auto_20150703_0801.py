# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command


def loadfixture(apps, schema_editor):
    call_command('loaddata', 'languages.json')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150630_0332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='need',
            name='personal',
        ),
        migrations.AlterUniqueTogether(
            name='need',
            unique_together=set([('language', 'name', 'definition')]),
        ),
        migrations.RunPython(loadfixture),
    ]
