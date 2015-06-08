# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='address',
            name='platform',
        ),
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='currency',
        ),
        migrations.DeleteModel(
            name='Currency',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='platform',
        ),
        migrations.DeleteModel(
            name='Platform',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
