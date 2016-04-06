import httplib
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from model_mommy import mommy
from users.models import User
from core.models import Need
from core.views import GoalCreateView
from core.models import Language


class GoalTest(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.language = Language.objects.create(name='English', language_code='en')

    def test_goal_create_from_anonymous_user(self):

        need_instance = mommy.make(Need, language=self.language)

        urls = {
            'goal_create_url': reverse('goal-create', kwargs={'need_id': need_instance.pk}),
            'account_login_url': reverse('account_login')
        }
        goal_create_url_with_login = "{account_login_url}?next={goal_create_url}".format(**urls)

        request = self.request.get(urls['goal_create_url'])
        request.LANGUAGE_CODE = self.language.language_code
        request.user = AnonymousUser()
        goal_create_view = GoalCreateView.as_view()(request)
        self.assertEqual(goal_create_view.status_code, httplib.FOUND)
        self.assertEqual(goal_create_view.url, goal_create_url_with_login)
