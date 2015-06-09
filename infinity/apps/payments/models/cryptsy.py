from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CryptsyTransaction(models.Model):
    address = models.ForeignKey(
        'CoinAddress',
        related_name='cryptsy_transaction'
    )
    amount = models.PositiveIntegerField()
    fee = models.PositiveIntegerField()
    timestamp = models.PositiveIntegerField()
    timezone = models.CharField(max_length=3)
    trxid = models.CharField(max_length=255, null=True, blank=True)
    message = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    matched_on = models.DateTimeField(null=True, blank=True)
    completed_on = models.DateTimeField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class CryptsyCredential(models.Model):
    privatekey = models.CharField(max_length=255)
    publickey = models.CharField(max_length=255)
    tradekey = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='credential'
    )
    notificationtoken = models.CharField(max_length=255)
