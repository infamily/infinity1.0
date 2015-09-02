from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from core.models import Language


UserModelName = settings.AUTH_USER_MODEL


class InvitationLetterTemplate(models.Model):
    language = models.OneToOneField(Language)
    body = models.TextField()

    def __unicode__(self):
        return "%s" % self.language


class InvitationOption(models.Model):
    user = models.OneToOneField(UserModelName)

    token = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    invitations_left = models.PositiveIntegerField()


class Invitation(models.Model):
    PENDING = 0
    JOINED = 1
    STATUSES = (
        (PENDING, 'Pending'),
        (JOINED, 'Joined')
    )

    sender = models.ForeignKey(
        UserModelName,
        related_name='sender_invites'
    )
    recipient = models.ForeignKey(
        UserModelName,
        related_name='recipient_invites',
        null=True,
        blank=True
    )
    email = models.EmailField()
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)

    def __unicode__(self):
        return "Sender: %s, Recipient: %s, Status: %s, Email: %s" (
            self.sender,
            self.recipient,
            self.email,
            self.status
        )
