import httplib
from random import randint
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from model_mommy import mommy
from users.models import User
from core.models import Need
from core.models import Type
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

    def test_goal_create(self):
        mommy.make(Type)
        password = str(randint(1, 100))
        user = mommy.make(User)
        user.set_password(password)
        user.save()

        user_logged_in = self.client.login(username=user.email, password=password)

        self.assertTrue(user_logged_in)

        response = self.client.get(reverse('goal-create'), follow=True)

        # Check status code
        self.assertTrue(response.status_code, httplib.OK)

        # Test form with invalid data
        response = response.client.post(reverse('goal-create'))

        # Get form from context
        form = response.context['form']

        # Form should returns validation error
        self.assertFalse(form.is_valid())
