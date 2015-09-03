# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0002_remove_invitation_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='invitationoption',
            name='token',
        ),
        migrations.AddField(
            model_name='invitation',
            name='invited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invitation',
            name='token',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
