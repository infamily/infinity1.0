from django.views.generic import View
from django.views.generic import FormView
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from .models import Invitation
from .models import InvitationLetterTemplate
from .forms import InvitationForm
from users.decorators import ForbiddenUser


class InviteView(View):
    def get(self, request, *args, **kwargs):
        """
        Set invitation session
        Redirect to the register page
        """
        invitation_object = Invitation.objects.filter(
            token=kwargs.get('token'),
            invited=False
        )
        if invitation_object.exists():
            request.session['invitation'] = True
            invitation_object = invitation_object.first()
            invitation_object.invited = True
            invitation_object.save()

        return redirect(reverse('account_signup'))


@ForbiddenUser(forbidden_usertypes=[u'AnonymousUser'])
class InvitationFormView(FormView):
    form_class = InvitationForm
    template_name = "invitation/invite.html"

    def get_form_kwargs(self):
        kwargs = super(InvitationFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class InvitationLetterTemplateView(DetailView):
    model = InvitationLetterTemplate
    slug_field = "language__omegawiki_language_id"
