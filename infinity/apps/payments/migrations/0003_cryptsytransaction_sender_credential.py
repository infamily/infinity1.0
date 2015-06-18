# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_remove_cryptsycredential_notificationtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptsytransaction',
            name='sender_credential',
            field=models.ForeignKey(related_name=b'cryptsy_transaction', default=1, to='payments.CryptsyCredential'),
            preserve_default=False,
        ),
    ]
