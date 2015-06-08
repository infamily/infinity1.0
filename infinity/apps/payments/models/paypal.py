from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class PayPalTransaction(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    CREATED = 'CREATED'
    COMPLETED = 'COMPLETED'
    INCOMPLETE = 'INCOMPLETE'
    ERROR = 'ERROR'
    REVERSALERROR = 'REVERSALERROR'

    PAYMENT_EXEC_STATUSES = (
        (CREATED, 'Created'),
        (COMPLETED, 'Completed'),
        (INCOMPLETE, 'Incomplete'),
        (ERROR, 'Error'),
        (REVERSALERROR, 'Reversalerror')
    )

    payKey = models.CharField(max_length=255)

    paymentExecStatus = models.CharField(
        choices=PAYMENT_EXEC_STATUSES,
        max_length=255
    )

    @classmethod
    def get_by_related_object(cls, related_object):
        """
        Get Transactions by related object.
        Example:
            In [3]: article = Article.objects.get(pk=1)
            In [4]: Transaction.get_related_object(article)
            Out[4]: [<Transaction: Transaction #1>]
        """
        related_object_type = ContentType.objects.get_for_model(related_object)
        transaction = cls.objects.filter(
            content_type__pk=related_object_type.id,
            object_id=related_object.id
        )

        return transaction

    currency = models.CharField(max_length=3)

    created_at = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
        unique=False,
        null=False,
        blank=False,
    )
    amount = models.DecimalField(
        null=False,
        max_digits=16,
        decimal_places=2,
        blank=False,
    )

    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sender_user_transaction',
        blank=True,
        null=True
    )

    receiver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='receiver_user_transaction',
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u"Transaction #%s" % self.id

    def get_absolute_url(self):
        return "/"
