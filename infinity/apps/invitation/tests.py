from django_webtest import WebTest
from model_mommy import mommy
from django.core.urlresolvers import reverse
from allauth.account.models import EmailAddress, EmailConfirmation


class InvitationTest(WebTest):
    def setUp(self):
        self.user_with_invitations = mommy.make('users.User')
        self.user_without_invitations = mommy.make('users.User')

        self.user_with_invitations.set_password('test')
        self.user_with_invitations.save()

        self.user_without_invitations.set_password('test')
        self.user_without_invitations.save()

        self.email_first = mommy.make(EmailAddress, user=self.user_with_invitations, verified=True)
        self.email_second = mommy.make(EmailAddress, user=self.user_without_invitations, verified=True)

        mommy.make(EmailConfirmation, email_address=self.email_first)
        mommy.make(EmailConfirmation, email_address=self.email_second)

        self.user_without_invitations.invitationoption.invitations_left = 0
        self.user_without_invitations.invitationoption.save()

    def login(self, login, password):
        resp = self.app.get(reverse('account_login'))
        form = resp.forms[0]
        form['login'] = login
        form['password'] = password
        res = form.submit()
        return res

    def test_invitation_form_view(self):
        invitation_form_view_url = reverse('invite:send')

        self.login(self.email_first.email, 'test')
        response = self.app.get(invitation_form_view_url)
        import ipdb; ipdb.set_trace()
