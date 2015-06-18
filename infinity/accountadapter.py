from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from invitation.models import InvitationKey
from allauth.account.signals import user_signed_up

from django.conf import settings
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.shortcuts import render


class AccountAdapter(DefaultAccountAdapter):
    """
    Checks whether or not the site is open for signups.
    Next to simply returning True/False you can also intervene the
    regular flow by raising an ImmediateHttpResponse
    """
    def is_open_for_signup(self, request):
        #print 'is open for sign up session keys', request.session.keys()
        if getattr(settings, 'ALLOW_NEW_REGISTRATIONS', False):
            if getattr(settings, 'INVITE_MODE', False):
                invitation_key = request.session.get('invitation_key', False)
                if invitation_key:
                    if InvitationKey.objects.is_key_valid(invitation_key.key):
                        invitation_recipient = request.session.get('invitation_recipient', False)
                        self.stash_verified_email(request, invitation_recipient[0])
                        return True
                    else:
                        extra_context = request.session.get('invitation_context', {})
                        template_name = 'invitation/wrong_invitation_key.html'
                        raise ImmediateHttpResponse(render(request,template_name, extra_context))
            else:
                return True
        return False

    @receiver (user_signed_up)
    def complete_signup(sender, **kwargs):
        user = kwargs.pop('user')
        request = kwargs.pop('request')
        #sociallogin = request.session.get('socialaccount_sociallogin', None)

        # Handle user permissions
        user.groups.add(Group.objects.get(name=settings.DEFAULT_USER_GROUP))
        user.save()

        # Handle invitation if required
        if 'invitation_key' in request.session.keys():
            invitation_key = request.session.get('invitation_key', False)
            invitation_key.mark_used(user)
            del request.session['invitation_key']
            del request.session['invitation_recipient']
            del request.session['invitation_context']
