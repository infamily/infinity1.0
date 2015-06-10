# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_cryptsytransaction_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cryptsytransaction',
            name='currency',
        ),
    ]
