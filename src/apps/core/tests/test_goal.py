import json
import httplib
from random import randint
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from model_mommy import mommy
from users.models import User
from core.models import Need
from core.models import Type
from core.models import Goal
from core.models import Definition
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
        type_ = mommy.make(Type)
        definition = mommy.make(Definition)
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

        goal = Goal.objects.first()
        self.assertFalse(goal)

        data = {
            'reason': str(randint(1, 100)),
            'type': type_.pk,
            'name': str(randint(1, 2000)),
            'language': self.language.pk,
            'definition': definition.pk
        }

        response = response.client.post(reverse('goal-create'), data)

        goal = Goal.objects.filter()

        # Goal has been created
        self.assertTrue(goal.exists())

        kwargs = {
            'goal_url': reverse('goal-detail', kwargs={'slug': goal.first().pk}),
            'language_code': self.language.language_code
        }

        goal_detail_url = "{goal_url}?lang={language_code}".format(**kwargs)

        self.assertEqual(response.status_code, httplib.FOUND)
        self.assertEqual(goal_detail_url, response.url)

        # Check personal goal
        data.update({'personal': True})
        response = response.client.post(reverse('goal-create'), data)

        self.assertTrue(goal.count() == 2)
        self.assertEqual(response.url, reverse('inbox'))
        self.assertEqual(response.status_code, httplib.FOUND)

        definition_data = {
            "definition": "computer program",
            "defined_meaning_id": "131303",
            "name": "Hello"
        }

        data = {
            'reason': str(randint(1, 100)),
            'type': type_.pk,
            'name': str(randint(1, 2000)),
            'language': self.language.pk,
            'select_definition': json.dumps(definition_data)
        }

        response = response.client.post(reverse('goal-create'), data)

        definition = Definition.objects.filter(**definition_data)

        # Check goal created
        self.assertTrue(goal.count() == 3)

        # Check if definition was created
        self.assertTrue(definition.exists())
