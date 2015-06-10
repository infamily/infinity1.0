# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150609_2222'),
        ('payments', '0002_auto_20150609_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cryptsytransaction',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='cryptsytransaction',
            name='object_id',
        ),
        migrations.AddField(
            model_name='cryptsytransaction',
            name='comment',
            field=models.ForeignKey(related_name=b'cryptsy_transaction', default=1, to='core.Comment'),
            preserve_default=False,
        ),
    ]
