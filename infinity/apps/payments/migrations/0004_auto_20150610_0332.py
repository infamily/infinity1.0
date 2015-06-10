# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150609_2222'),
        ('payments', '0003_auto_20150610_0331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paypaltransaction',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='paypaltransaction',
            name='object_id',
        ),
        migrations.AddField(
            model_name='paypaltransaction',
            name='comment',
            field=models.ForeignKey(related_name=b'paypal_transaction', default=1, to='core.Comment'),
            preserve_default=False,
        ),
    ]
