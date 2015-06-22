# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_cryptsytransaction_sender_credential'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptsycredential',
            name='privatekey',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
