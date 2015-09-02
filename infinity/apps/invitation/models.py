from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from users.models import User
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

    invitations_left = models.PositiveIntegerField(default=3)


class Invitation(models.Model):
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

    def check_user_invited(self, email):
        try:
            User.objects.get(email=email)
        except User.ObjectsDoesNotExist:
            return False
        else:
            return True

    def has_accepted_invitation(self):
        if self.recipient:
            return True
        else:
            return False

    has_accepted_invitation.boolean = True

    def __unicode__(self):
        return "Sender: %s, Recipient: %s, Email: %s" % (
            self.sender,
            self.recipient,
            self.email
        )


def _user_created(sender, instance, created, *args, **kwargs):
    from uuid import uuid4
    if created:
        invitation = InvitationOption.objects.create(
            user=instance,
            token=uuid4().hex
        )
        invitation.save()

post_save.connect(_user_created, sender=User)
