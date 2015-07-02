# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_need_personal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('http_accept_language', models.CharField(max_length=255, null=True, blank=True)),
                ('omegawiki_language_id', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='goal',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idea',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='need',
            name='defined_meaning_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='need',
            name='definition',
            field=models.CharField(default='A need', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='need',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='plan',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='step',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='work',
            name='language',
            field=models.ForeignKey(blank=True, to='core.Language', null=True),
            preserve_default=True,
        ),
    ]
