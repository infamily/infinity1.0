from django.db import models
from django.conf import settings

from core.models import Comment


class CryptsyTransaction(models.Model):
    address = models.ForeignKey(
        'CoinAddress',
        related_name='cryptsy_transaction'
    )
    sender_credential = models.ForeignKey(
        'CryptsyCredential', related_name='cryptsy_transaction'
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
    comment = models.ForeignKey(Comment, related_name='cryptsy_transaction')

    def save(self, *args, **kwargs):
        "Save comment created date to parent object."
        self.comment.compute_money()
        self.comment.content_object.sum_comment_values()
        super(CryptsyTransaction, self).save(*args, **kwargs)


class CryptsyCredential(models.Model):
    privatekey = models.CharField(max_length=255, unique=True)
    publickey = models.CharField(max_length=255)
    tradekey = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='credential'
    )
    default = models.BooleanField(default=False)
