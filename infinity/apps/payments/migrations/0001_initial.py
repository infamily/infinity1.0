# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoinAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('currency_code', models.CharField(max_length=6)),
                ('address', models.CharField(max_length=255)),
                ('user', models.ForeignKey(related_name=b'address', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CryptsyCredential',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privatekey', models.CharField(max_length=255)),
                ('publickey', models.CharField(max_length=255)),
                ('tradekey', models.CharField(max_length=255)),
                ('notificationtoken', models.CharField(max_length=255)),
                ('user', models.ForeignKey(related_name=b'credential', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CryptsyTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField()),
                ('fee', models.PositiveIntegerField()),
                ('timestamp', models.PositiveIntegerField()),
                ('timezone', models.CharField(max_length=3)),
                ('trxid', models.CharField(max_length=255, null=True, blank=True)),
                ('message', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('matched_on', models.DateTimeField(null=True, blank=True)),
                ('completed_on', models.DateTimeField(null=True, blank=True)),
                ('address', models.ForeignKey(related_name=b'cryptsy_transaction', to='payments.CoinAddress')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PayPalTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('payKey', models.CharField(max_length=255)),
                ('paymentExecStatus', models.CharField(max_length=255, choices=[(b'CREATED', b'Created'), (b'COMPLETED', b'Completed'), (b'INCOMPLETE', b'Incomplete'), (b'ERROR', b'Error'), (b'REVERSALERROR', b'Reversalerror')])),
                ('currency', models.CharField(max_length=3)),
                ('created_at', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('amount', models.DecimalField(max_digits=16, decimal_places=2)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('receiver_user', models.ForeignKey(related_name=b'receiver_user_transaction', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('sender_user', models.ForeignKey(related_name=b'sender_user_transaction', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='coinaddress',
            unique_together=set([('currency_code', 'address')]),
        ),
    ]
