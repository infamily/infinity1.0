# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150806_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=django_markdown.models.MarkdownField(),
        ),
        migrations.AlterField(
            model_name='goal',
            name='reason',
            field=django_markdown.models.MarkdownField(),
        ),
        migrations.AlterField(
            model_name='idea',
            name='description',
            field=django_markdown.models.MarkdownField(),
        ),
        migrations.AlterField(
            model_name='plan',
            name='deliverable',
            field=django_markdown.models.MarkdownField(),
        ),
        migrations.AlterField(
            model_name='plan',
            name='situation',
            field=django_markdown.models.MarkdownField(),
        ),
        migrations.AlterField(
            model_name='step',
            name='objective',
            field=django_markdown.models.MarkdownField(),
        ),
        migrations.AlterField(
            model_name='work',
            name='description',
            field=django_markdown.models.MarkdownField(),
        ),
    ]
